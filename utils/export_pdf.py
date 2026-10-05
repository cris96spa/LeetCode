"""Export the cheat sheet and common patterns docs to a single PDF.

Requires pandoc and a TeX Live install providing xelatex. Styling lives in
utils/pdf/ (LaTeX header and pandoc Lua filter). The default output is served
by the docs site, where the download button links to it.

Usage:
    uv run python utils/export_pdf.py [--output docs/assets/leetcode_notes.pdf]
"""

import argparse
import datetime
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STYLE = Path(__file__).resolve().parent / "pdf"

PAGES = [DOCS / "LeetCodeCheatSheet.md", *sorted((DOCS / "common_patterns").glob("*.md"))]
REFERENCES_RE = re.compile(r"^## References\n(.*?)(?=^## |\Z)", re.M | re.S)

ADMONITION_RE = re.compile(r'^(?:!!!|\?\?\?\+?)\s+(\w+)(?:\s+"([^"]*)")?\s*$')
# Fonts shipped with TeX Live, loaded by file name so local and CI builds match.
FONTS = [
    "--variable=mainfont:XCharter-Roman.otf",
    "--variable=mainfontoptions:BoldFont=XCharter-Bold.otf",
    "--variable=mainfontoptions:ItalicFont=XCharter-Italic.otf",
    "--variable=mainfontoptions:BoldItalicFont=XCharter-BoldItalic.otf",
    "--variable=sansfont:FiraSans-Regular.otf",
    "--variable=sansfontoptions:BoldFont=FiraSans-SemiBold.otf",
    "--variable=sansfontoptions:ItalicFont=FiraSans-Italic.otf",
    "--variable=sansfontoptions:BoldItalicFont=FiraSans-SemiBoldItalic.otf",
    "--variable=monofont:FiraMono-Regular.otf",
    "--variable=monofontoptions:BoldFont=FiraMono-Bold.otf",
    "--variable=monofontoptions:Scale=0.88",
    "--variable=monofontoptions:HyphenChar=None",
    "--variable=mathfont:STIXTwoMath-Regular.otf",
]
LINK_RE = re.compile(r"\]\((?!https?:)([^)#]*\.md)(#[^)]*)?\)")
TITLE_RE = re.compile(r"^# (.+)$", re.M)


def convert_admonitions(text: str) -> str:
    """Turn `!!! kind "Title"` blocks (indented body) into pandoc fenced divs."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        match = ADMONITION_RE.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        kind, title = match.groups()
        body = []
        i += 1
        while i < len(lines) and (not lines[i].strip() or lines[i].startswith("    ")):
            body.append(lines[i][4:])
            i += 1
        title_attr = f' title="{title}"' if title else ""
        out += [
            f"::: {{.admonition .{kind}{title_attr}}}",
            convert_admonitions("\n".join(body)).strip(),
            ":::",
            "",
        ]
    return "\n".join(out)


def page_anchor(name: str) -> str:
    """Anchor of an exported page's title, derived from its file name."""
    return f"page-{Path(name).stem}"


def anchor_title(text: str, page: Path) -> str:
    """Give the page's title a stable anchor that whole-page links can target."""
    return TITLE_RE.sub(lambda m: f"# {m.group(1)} {{#{page_anchor(page.name)}}}", text, count=1)


def rewrite_links(text: str) -> str:
    """Point cross-page links at in-document anchors: the section, or the page's title."""
    exported = {page.name for page in PAGES}

    def target(match: re.Match) -> str:
        page, section = match.groups()
        if section:
            return f"]({section})"
        return f"](#{page_anchor(page)})" if Path(page).name in exported else "]()"

    return LINK_RE.sub(target, text)


def references() -> str:
    """The home page's References section, as the PDF's closing chapter."""
    match = REFERENCES_RE.search((DOCS / "index.md").read_text(encoding="utf-8"))
    return f"# References\n{match.group(1)}" if match else ""


def markdown_source() -> str:
    """Concatenate the exported pages, rewritten into pandoc-friendly markdown."""
    pages = [anchor_title(convert_admonitions(page.read_text(encoding="utf-8")), page) for page in PAGES]
    return "\n\n".join(rewrite_links(text) for text in [*pages, references()])


def pandoc_command(output: Path) -> list[str]:
    """Build the pandoc invocation; the output extension selects the format."""
    return [
        "pandoc",
        "--from=markdown+tex_math_dollars+gfm_auto_identifiers-yaml_metadata_block",
        "--pdf-engine=xelatex",
        "--top-level-division=chapter",
        "--toc",
        "--toc-depth=1",
        "--syntax-highlighting=tango",
        f"--lua-filter={STYLE / 'filters.lua'}",
        f"--include-in-header={STYLE / 'header.tex'}",
        "--metadata=title:LeetCode Notes",
        f"--metadata=date:{datetime.date.today():%B %Y}",
        "--variable=documentclass:report",
        "--variable=fontsize:10pt",
        "--variable=geometry:a4paper,margin=2.3cm,headheight=14pt",
        "--variable=linestretch:1.15",
        *FONTS,
        "--variable=colorlinks:true",
        "--variable=toccolor:ink",
        f"--output={output}",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=DOCS / "assets" / "leetcode_notes.pdf")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(pandoc_command(args.output), input=markdown_source(), text=True, check=True)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
