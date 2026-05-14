import json
import logging
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

legger = logging.getLogger(__name__)

_ROOT = Path(__file__).parent.parent
_NEETCODE_MAP = _ROOT / "utils" / "neetcode250.json"
_README = _ROOT / "README.md"
_DOCS_INDEX = _ROOT / "docs" / "index.md"

_README_MARKERS = ("<!-- PROGRESS:START -->", "<!-- PROGRESS:END -->")
_DOCS_MARKERS = ("<!-- DASHBOARD:START -->", "<!-- DASHBOARD:END -->")

_DIFFICULTIES = ("Easy", "Medium", "Hard")
_DIFF_EMOJI = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}

_NC250_PATTERN_ORDER = (
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
)


class _SolvedFile(NamedTuple):
    number: int
    slug: str
    path: Path
    difficulty: str


def _scan() -> list[_SolvedFile]:
    files: list[_SolvedFile] = []
    for diff in _DIFFICULTIES:
        for f in sorted((_ROOT / "leetcode" / diff).glob("*.py")):
            if f.name == "__init__.py":
                continue
            parts = f.stem.split("_", 1)
            if len(parts) == 2 and parts[0].isdigit():
                files.append(_SolvedFile(int(parts[0]), parts[1], f, diff))
    return files


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def _slug_to_name(slug: str) -> str:
    return slug.replace("_", " ").title()


def _ascii_bar(solved: int, total: int, width: int = 12) -> str:
    filled = round(solved / total * width) if total else 0
    return "█" * filled + "░" * (width - filled)


def _inject(text: str, start: str, end: str, content: str) -> str:
    pat = re.compile(rf"({re.escape(start)})(.*?)({re.escape(end)})", re.DOTALL)
    result, n = pat.subn(rf"\1\n{content}\n\3", text)
    if n == 0:
        raise ValueError(f"Markers not found: {start!r} / {end!r}")
    return result


def _classify(
    files: list[_SolvedFile],
    mapping: dict[str, str],
) -> tuple[dict[str, int], dict[str, list[str]], list[_SolvedFile]]:
    lookup = {_normalize(k): v for k, v in mapping.items()}
    counts = {d: sum(1 for f in files if f.difficulty == d) for d in _DIFFICULTIES}
    pattern_solved: dict[str, list[str]] = defaultdict(list)
    unmatched: list[_SolvedFile] = []

    for file in files:
        name = _slug_to_name(file.slug)
        pattern = lookup.get(_normalize(name))
        if pattern:
            pattern_solved[pattern].append(_normalize(name))
        else:
            unmatched.append(file)

    return counts, dict(pattern_solved), unmatched


def _render_readme(
    counts: dict[str, int],
    pattern_solved: dict[str, list[str]],
    totals: dict[str, int],
) -> str:
    nc250_count = sum(len(v) for v in pattern_solved.values())
    header = " | ".join(f"{_DIFF_EMOJI[d]} {d}" for d in _DIFFICULTIES)
    solved_row = " | ".join(f"**{counts[d]}**" for d in _DIFFICULTIES)

    lines = [
        f"| | {header} |",
        "|:--:|:--:|:--:|:--:|",
        f"| **Solved** | {solved_row} |",
        "",
        f"> **NeetCode 250** &nbsp;·&nbsp; {nc250_count} / 250 problems tracked",
        "",
        "| Pattern | Solved | Total | Progress |",
        "|---------|-------:|------:|:---------|",
    ]
    for pattern in _NC250_PATTERN_ORDER:
        s = len(pattern_solved.get(pattern, []))
        t = totals.get(pattern, 0)
        pct = round(s / t * 100) if t else 0
        lines.append(f"| {pattern} | {s} | {t} | `{_ascii_bar(s, t)}` {pct}% |")
    return "\n".join(lines)


def _render_docs(
    counts: dict[str, int],
    pattern_solved: dict[str, list[str]],
    totals: dict[str, int],
    mapping: dict[str, str],
    unmatched: list[_SolvedFile],
) -> str:
    nc250_count = sum(len(v) for v in pattern_solved.values())

    by_pattern: dict[str, list[str]] = defaultdict(list)
    for name, pattern in mapping.items():
        by_pattern[pattern].append(name)
    for problems in by_pattern.values():
        problems.sort(key=str.lower)

    lines: list[str] = [
        '<div class="lc-stats">',
        *(
            f'<div class="lc-stat lc-{d.lower()}"><span class="lc-num">{counts[d]}</span>'
            f'<span class="lc-label">{d}</span></div>'
            for d in _DIFFICULTIES
        ),
        "</div>",
        "",
        f"## NeetCode 250 &nbsp;·&nbsp; {nc250_count} / 250",
        "",
    ]

    for pattern in _NC250_PATTERN_ORDER:
        solved_set = set(pattern_solved.get(pattern, []))
        problems = by_pattern.get(pattern, [])
        s, t = len(solved_set), totals.get(pattern, len(problems))
        pct = round(s / t * 100) if t else 0
        admonition = "success" if s == t > 0 else "note"

        lines += [
            f'??? {admonition} "{pattern} &nbsp;·&nbsp; {s} / {t} ({pct}%)"',
            f'    <div class="lc-progress-bar">'
            f'<div class="lc-progress-fill" style="width:{pct}%"></div></div>',
            "",
            *(
                f"    - [{'x' if _normalize(name) in solved_set else ' '}] {name}"
                for name in problems
            ),
            "",
        ]

    if unmatched:
        lines += [
            f"## Other Solutions &nbsp;·&nbsp; {len(unmatched)}",
            "",
            f'??? note "Show {len(unmatched)} solutions"',
            "    | File | Difficulty | Inferred name |",
            "    |------|:----------:|---------------|",
            *(
                f"    | `{f.path.name}` | {f.difficulty} | {_slug_to_name(f.slug)} |"
                for f in sorted(unmatched, key=lambda f: f.number)
            ),
            "",
        ]

    return "\n".join(lines)


def main() -> None:
    """Regenerate progress dashboards and stage the updated files."""
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    nc250 = json.loads(_NEETCODE_MAP.read_text())
    mapping: dict[str, str] = nc250["mapping"]
    totals: dict[str, int] = nc250["patterns"]

    files = _scan()
    counts, pattern_solved, unmatched = _classify(files, mapping)

    readme = _render_readme(counts, pattern_solved, totals)
    docs = _render_docs(counts, pattern_solved, totals, mapping, unmatched)

    _README.write_text(_inject(_README.read_text(), *_README_MARKERS, readme))
    _DOCS_INDEX.write_text(_inject(_DOCS_INDEX.read_text(), *_DOCS_MARKERS, docs))

    subprocess.run(["git", "add", str(_README), str(_DOCS_INDEX)], check=True, cwd=_ROOT)

    nc250_count = sum(len(v) for v in pattern_solved.values())
    legger.info(
        "Progress updated — Easy: %d, Medium: %d, Hard: %d, NC250: %d/250",
        counts["Easy"],
        counts["Medium"],
        counts["Hard"],
        nc250_count,
    )


if __name__ == "__main__":
    main()
