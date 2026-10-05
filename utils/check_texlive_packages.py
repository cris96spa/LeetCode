"""Check that .github/texlive.packages covers everything the PDF export needs.

CI installs only the TeX Live packages listed in that file, so a package used
locally but missing there breaks the deploy. This builds the document once with
`xelatex -recorder`, maps every file it reads (plus the fonts, which XeTeX does
not record) to its TeX Live package using the local package database, and fails
if any package is neither listed nor pulled in by a listed scheme or collection.

Skips (exit 0) when pandoc or a TeX Live install is not available locally.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from utils.export_pdf import ROOT, STYLE, markdown_source, pandoc_command

PACKAGE_FILE = ROOT / ".github" / "texlive.packages"
FONT_SOURCES = (ROOT / "utils" / "export_pdf.py", STYLE / "header.tex")
FONT_RE = re.compile(r"[\w-]+\.(?:otf|ttf)\b")
ALWAYS_REQUIRED = {"xetex"}


def listed_packages() -> set[str]:
    """Read the package names from the package file, ignoring comments."""
    text = PACKAGE_FILE.read_text(encoding="utf-8")
    return {name for line in text.splitlines() for name in line.split("#", 1)[0].split()}


def read_tlpdb(texlive_root: Path) -> tuple[dict[str, str], dict[str, set[str]]]:
    """Parse the TeX Live database into file -> package and package -> dependencies."""
    owner: dict[str, str] = {}
    depends: dict[str, set[str]] = {}
    package = ""
    tlpdb = texlive_root / "tlpkg" / "texlive.tlpdb"
    for line in tlpdb.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("name "):
            package = line[5:].strip()
            depends[package] = set()
        elif line.startswith("depend "):
            depends[package].add(line[7:].strip())
        elif line.startswith(" texmf-dist/"):
            owner[line.split()[0]] = package
    return owner, depends


def expand(packages: set[str], depends: dict[str, set[str]]) -> set[str]:
    """Add everything the listed schemes and collections install, recursively."""
    covered, stack = set(), list(packages)
    while stack:
        package = stack.pop()
        if package in covered:
            continue
        covered.add(package)
        if package.startswith(("scheme-", "collection-")):
            stack.extend(depends.get(package, ()))
    return covered


def recorded_files(workdir: Path) -> set[Path]:
    """Compile the document once and return every input file xelatex opened."""
    tex = workdir / "notes.tex"
    subprocess.run([*pandoc_command(tex), "--standalone"], input=markdown_source(), text=True, check=True)
    result = subprocess.run(
        ["xelatex", "-recorder", "-no-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name],
        cwd=workdir,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        sys.exit(f"xelatex failed:\n{result.stdout[-3000:]}")
    fls = (workdir / "notes.fls").read_text(encoding="utf-8")
    return {Path(line[6:]) for line in fls.splitlines() if line.startswith("INPUT ")}


def font_files() -> set[Path]:
    """Resolve the font files referenced by name in the export script and header."""
    names = {name for source in FONT_SOURCES for name in FONT_RE.findall(source.read_text())}
    found = set()
    for name in sorted(names):
        path = subprocess.run(["kpsewhich", name], capture_output=True, text=True).stdout.strip()
        if not path:
            sys.exit(f"Font {name} is not in the local TeX Live tree.")
        found.add(Path(path))
    return found


def main() -> None:
    if not shutil.which("pandoc") or not shutil.which("kpsewhich"):
        print("Skipping TeX Live package check: pandoc or TeX Live not installed.")
        return
    texlive_root = Path(
        subprocess.run(
            ["kpsewhich", "-var-value=SELFAUTOPARENT"], capture_output=True, text=True
        ).stdout.strip()
    )
    owner, depends = read_tlpdb(texlive_root)

    with tempfile.TemporaryDirectory() as tmp:
        files = recorded_files(Path(tmp)) | font_files()

    required = set(ALWAYS_REQUIRED)
    for path in files:
        relative = path.resolve().as_posix().split("/texmf-dist/", 1)
        if len(relative) == 2 and f"texmf-dist/{relative[1]}" in owner:
            required.add(owner[f"texmf-dist/{relative[1]}"])

    listed = listed_packages()
    missing = sorted(required - expand(listed, depends))
    if missing:
        print(f"{PACKAGE_FILE.relative_to(ROOT)} is missing TeX Live packages used by the PDF:")
        print("\n".join(f"  {package}" for package in missing))
        sys.exit(1)
    unknown = sorted(name for name in listed if name not in depends)
    if unknown:
        print(f"Note: not in the local TeX Live database (renamed upstream?): {', '.join(unknown)}")
    print(f"All {len(required)} TeX Live packages used by the PDF are listed.")


if __name__ == "__main__":
    main()
