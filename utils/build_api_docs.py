"""Generate per-solution API pages and a SUMMARY.md for literate-nav."""

from collections import defaultdict
from pathlib import Path

import mkdocs_gen_files

_SOURCE_ROOT = Path("leetcode")
_API_DIR = Path("api")
_SKIP = {"__init__.py", "__main__.py"}


def _sort_key(p: Path) -> tuple[int, str]:
    num = p.stem.split("_")[0]
    return (int(num) if num.isdigit() else -1, p.stem)


def _page_title(stem: str) -> str:
    """Return a human-readable title from a solution stem.

    Example: ``'1_two_sum'`` → ``'1. Two Sum'``
    """
    parts = stem.split("_", 1)
    if len(parts) == 2 and parts[0].isdigit():
        return f"{parts[0]}. {parts[1].replace('_', ' ').title()}"
    return stem.replace("_", " ").title()


def main() -> None:
    by_dir: dict[Path, list[Path]] = defaultdict(list)
    for path in sorted(_SOURCE_ROOT.rglob("*.py"), key=_sort_key):
        if path.name not in _SKIP:
            by_dir[path.parent.relative_to(_SOURCE_ROOT)].append(path)

    summary: list[str] = []
    for subdir, paths in sorted(by_dir.items()):
        summary.append(f"* {subdir}\n")
        for path in paths:
            rel = path.relative_to(_SOURCE_ROOT)
            doc_path = _API_DIR / rel.with_suffix(".md")
            title = _page_title(path.stem)

            with mkdocs_gen_files.open(doc_path, "w") as f:
                f.write(f"# {title}\n\n```python\n{path.read_text(encoding='utf-8')}```\n")

            summary.append(f"    * [{title}]({rel.with_suffix('.md')})\n")

    with mkdocs_gen_files.open(_API_DIR / "SUMMARY.md", "w") as f:
        f.writelines(summary)


main()
