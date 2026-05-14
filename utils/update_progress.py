"""Update progress dashboard in README.md and docs/index.md.

Run automatically via pre-commit, or manually: uv run python utils/update_progress.py
"""

import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
LEETCODE_DIR = ROOT / "leetcode"
NEETCODE_MAP = ROOT / "utils" / "neetcode250.json"
README = ROOT / "README.md"
DOCS_INDEX = ROOT / "docs" / "index.md"

DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Canonical order matching the Neetcode roadmap
NC250_PATTERN_ORDER = [
    "Arrays & Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Linked List",
    "Trees",
    "Tries",
    "Heap / Priority Queue",
    "Intervals",
    "Greedy",
    "Graphs",
    "Advanced Graphs",
    "Backtracking",
    "1-D Dynamic Programming",
    "2-D Dynamic Programming",
    "Bit Manipulation",
    "Math & Geometry",
]


def get_solved_files() -> dict[str, list[tuple[int, str, Path]]]:
    """Scan difficulty folders and return {difficulty: [(number, slug, path)]}."""
    solved: dict[str, list[tuple[int, str, Path]]] = {}
    for diff in DIFFICULTIES:
        folder = LEETCODE_DIR / diff
        files: list[tuple[int, str, Path]] = []
        if folder.exists():
            for f in sorted(folder.glob("*.py")):
                if f.name == "__init__.py":
                    continue
                parts = f.stem.split("_", 1)
                if len(parts) == 2 and parts[0].isdigit():
                    files.append((int(parts[0]), parts[1], f))
        solved[diff] = files
    return solved


def slug_to_name(slug: str) -> str:
    """Convert a snake_case filename slug to a displayable title."""
    return slug.replace("_", " ").title()


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def progress_bar_ascii(solved: int, total: int, width: int = 12) -> str:
    filled = round(solved / total * width) if total else 0
    return "█" * filled + "░" * (width - filled)


def replace_between_markers(text: str, start: str, end: str, content: str) -> str:
    pattern = re.compile(
        rf"({re.escape(start)})(.*?)({re.escape(end)})",
        re.DOTALL,
    )
    result, n = pattern.subn(rf"\1\n{content}\n\3", text)
    if n == 0:
        raise ValueError(f"Markers '{start}' / '{end}' not found in file")
    return result


def build_progress_data(
    solved: dict[str, list[tuple[int, str, Path]]],
    mapping: dict[str, str],
    nc250_totals: dict[str, int],
) -> tuple[dict[str, int], dict[str, list[str]]]:
    """Return (counts_by_diff, solved_names_by_pattern)."""
    counts = {diff: len(files) for diff, files in solved.items()}
    lookup = {normalize(k): v for k, v in mapping.items()}

    pattern_solved: dict[str, list[str]] = defaultdict(list)
    for diff, files in solved.items():
        for _num, slug, _path in files:
            pretty = slug_to_name(slug)
            pattern = lookup.get(normalize(pretty))
            if pattern:
                pattern_solved[pattern].append(normalize(pretty))

    return counts, dict(pattern_solved)


# ─── README section ───────────────────────────────────────────────────────────


def render_readme_section(
    counts: dict[str, int],
    pattern_solved: dict[str, list[str]],
    nc250_totals: dict[str, int],
) -> str:
    nc250_count = sum(len(v) for v in pattern_solved.values())
    lines = [
        "| | 🟢 Easy | 🟡 Medium | 🔴 Hard |",
        "|:--:|:--:|:--:|:--:|",
        f"| **Solved** | **{counts['Easy']}** | **{counts['Medium']}** | **{counts['Hard']}** |",
        "",
        f"> **NeetCode 250** &nbsp;·&nbsp; {nc250_count} / 250 problems tracked",
        "",
        "| Pattern | Solved | Total | Progress |",
        "|---------|-------:|------:|:---------|",
    ]
    for pattern in NC250_PATTERN_ORDER:
        s = len(pattern_solved.get(pattern, []))
        t = nc250_totals.get(pattern, 0)
        bar = progress_bar_ascii(s, t)
        lines.append(f"| {pattern} | {s} | {t} | `{bar}` |")
    return "\n".join(lines)


# ─── docs/index.md section ────────────────────────────────────────────────────


def render_docs_section(
    counts: dict[str, int],
    pattern_solved: dict[str, list[str]],
    nc250_totals: dict[str, int],
    mapping: dict[str, str],
) -> str:
    nc250_count = sum(len(v) for v in pattern_solved.values())

    # Build pattern → sorted problem name list
    pattern_problems: dict[str, list[str]] = defaultdict(list)
    for name, pattern in mapping.items():
        pattern_problems[pattern].append(name)
    for p in pattern_problems:
        pattern_problems[p].sort(key=str.lower)

    lines: list[str] = [
        '<div class="lc-stats">',
        f'<div class="lc-stat lc-easy"><span class="lc-num">{counts["Easy"]}</span>'
        '<span class="lc-label">Easy</span></div>',
        f'<div class="lc-stat lc-medium"><span class="lc-num">{counts["Medium"]}</span>'
        '<span class="lc-label">Medium</span></div>',
        f'<div class="lc-stat lc-hard"><span class="lc-num">{counts["Hard"]}</span>'
        '<span class="lc-label">Hard</span></div>',
        "</div>",
        "",
        f"## NeetCode 250 &nbsp;·&nbsp; {nc250_count} / 250",
        "",
    ]

    for pattern in NC250_PATTERN_ORDER:
        solved_set = set(pattern_solved.get(pattern, []))
        problems = pattern_problems.get(pattern, [])
        s = len(solved_set)
        t = nc250_totals.get(pattern, len(problems))
        pct = round(s / t * 100) if t else 0

        admonition = "success" if s == t and t > 0 else "note"
        lines.append(
            f'??? {admonition} "{pattern} &nbsp;·&nbsp; {s} / {t} ({pct}%)"'
        )
        lines.append(
            f'    <div class="lc-progress-bar">'
            f'<div class="lc-progress-fill" style="width:{pct}%"></div></div>'
        )
        lines.append("")
        for name in problems:
            if normalize(name) in solved_set:
                lines.append(f"    - [x] {name}")
            else:
                lines.append(f"    - [ ] {name}")
        lines.append("")

    return "\n".join(lines)


# ─── Entry point ─────────────────────────────────────────────────────────────


def main() -> None:
    """Update README.md and docs/index.md with current progress."""
    with open(NEETCODE_MAP) as f:
        nc250 = json.load(f)

    mapping: dict[str, str] = nc250["mapping"]
    nc250_totals: dict[str, int] = nc250["patterns"]

    solved = get_solved_files()
    counts, pattern_solved = build_progress_data(solved, mapping, nc250_totals)

    # README
    readme_text = README.read_text()
    readme_text = replace_between_markers(
        readme_text,
        "<!-- PROGRESS:START -->",
        "<!-- PROGRESS:END -->",
        render_readme_section(counts, pattern_solved, nc250_totals),
    )
    README.write_text(readme_text)

    # docs/index.md
    docs_text = DOCS_INDEX.read_text()
    docs_text = replace_between_markers(
        docs_text,
        "<!-- DASHBOARD:START -->",
        "<!-- DASHBOARD:END -->",
        render_docs_section(counts, pattern_solved, nc250_totals, mapping),
    )
    DOCS_INDEX.write_text(docs_text)

    # Stage both files so the commit includes updated dashboards
    subprocess.run(
        ["git", "add", str(README), str(DOCS_INDEX)],
        check=True,
        cwd=ROOT,
    )

    nc250_count = sum(len(v) for v in pattern_solved.values())
    print(
        f"✓ Progress updated — "
        f"Easy: {counts['Easy']}, Medium: {counts['Medium']}, Hard: {counts['Hard']}, "
        f"NC250: {nc250_count}/250"
    )


if __name__ == "__main__":
    main()
