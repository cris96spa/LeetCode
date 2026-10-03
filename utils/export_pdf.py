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
LINK_RE = re.compile(r"\]\((?!https?:)[^)#]*\.md(#[^)]*)?\)")


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


def rewrite_links(text: str) -> str:
    """Point cross-page links at in-document anchors; drop whole-page links."""
    return LINK_RE.sub(lambda m: f"]({m.group(1)})" if m.group(1) else "]()", text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=DOCS / "assets" / "leetcode_notes.pdf")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    source = "\n\n".join(
        rewrite_links(convert_admonitions(page.read_text(encoding="utf-8"))) for page in PAGES
    )
    subprocess.run(
        [
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
            f"--output={args.output}",
        ],
        input=source,
        text=True,
        check=True,
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
