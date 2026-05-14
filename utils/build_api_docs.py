from collections import defaultdict
from pathlib import Path

import mkdocs_gen_files

PROJECT_NAME = "leetcode"

SOURCE_ROOT = Path(PROJECT_NAME)
API_DIR = Path("api")

SKIP_FILENAMES: set[str] = {
    "__init__.py",
    "__main__.py",
}

SKIP_PATHS: set[str] = set()


def _sort_key(p: Path) -> tuple[int, str]:
    num = p.stem.split("_")[0]
    return (int(num) if num.isdigit() else -1, p.stem)


def _page_title(stem: str) -> str:
    """Return a human-readable title from a solution file stem.

    Example: '1_two_sum' -> '1. Two Sum'
    """
    parts = stem.split("_", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return f"{parts[0]}. {parts[1].replace('_', ' ').title()}"
    return stem.replace("_", " ").title()


def main() -> None:
    # Collect pages per sub-directory, sorted numerically
    by_dir: dict[Path, list[Path]] = defaultdict(list)
    for path in sorted(SOURCE_ROOT.rglob("*.py"), key=_sort_key):
        if path.name in SKIP_FILENAMES:
            continue
        if any(path.is_relative_to(Path(p)) for p in SKIP_PATHS):
            continue
        by_dir[path.parent.relative_to(SOURCE_ROOT)].append(path)

    # Write source pages and build a single top-level SUMMARY.md for literate-nav
    top_summary: list[str] = []
    for subdir, paths in sorted(by_dir.items()):
        top_summary.append(f"* {subdir}\n")
        for path in paths:
            rel = path.relative_to(SOURCE_ROOT)
            doc_path = API_DIR / rel.with_suffix(".md")
            title = _page_title(path.stem)
            source_code = path.read_text(encoding="utf-8")

            with mkdocs_gen_files.open(doc_path, "w") as f:
                f.write(f"# {title}\n\n")
                f.write(f"```python\n{source_code}```\n")

            top_summary.append(f"    * [{title}]({rel.with_suffix('.md')})\n")

    with mkdocs_gen_files.open(API_DIR / "SUMMARY.md", "w") as f:
        f.writelines(top_summary)


main()
