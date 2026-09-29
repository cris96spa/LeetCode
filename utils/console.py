"""Shared Rich console and the presentation helpers built on it."""

import os
from collections.abc import Mapping
from typing import Any

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

DEFAULT_CONSOLE_WIDTH = 180
SCIENTIFIC_NOTATION_THRESHOLD = 1e-3

STYLE_HEADER = "cyan"
STYLE_INFO = "magenta"
STYLE_METRIC = "green"
STYLE_MUTED = "dim"

console = Console(width=int(os.environ.get("COLUMNS", DEFAULT_CONSOLE_WIDTH)))


def _resolve(override: Console | None) -> Console:
    return override if override is not None else console


def format_metric(value: Any) -> str:
    """Render a metric value, falling back to scientific notation for tiny floats."""
    if isinstance(value, float):
        if 0 < abs(value) < SCIENTIFIC_NOTATION_THRESHOLD:
            return f"{value:.2e}"
        return f"{value:.4f}"
    return str(value)


def highlight_markers(text: str, styles: Mapping[str, str]) -> str:
    """Escape text as literal content, then style each mapped substring.

    Escaping before styling is what stops square brackets inside ``text`` from
    being interpreted as Rich markup.

    Args:
        text: Text to render literally, including any square brackets.
        styles: Mapping of literal substring to the Rich style to wrap it in.

    Returns:
        Markup-safe text with every mapped substring styled.
    """
    result = escape(text)
    for marker, style in styles.items():
        escaped_marker = escape(marker)
        result = result.replace(escaped_marker, f"[{style}]{escaped_marker}[/{style}]")
    return result


def section_header(
    title: str,
    *,
    style: str = STYLE_HEADER,
    console: Console | None = None,
) -> None:
    """Print a full-width rule introducing a new phase of output."""
    _resolve(console).rule(f"[bold {style}]{title}[/]", style=style)


def summary_panel(
    fields: Mapping[str, Any],
    *,
    title: str,
    style: str = STYLE_INFO,
    console: Console | None = None,
) -> None:
    """Print a panel of compact ``label: value`` lines."""
    body = "\n".join(f"[{STYLE_MUTED}]{label}:[/] {value}" for label, value in fields.items())
    _resolve(console).print(Panel(body, title=f"[bold {style}]{title}[/]", border_style=style))


def metrics_panel(
    metrics: Mapping[str, Any],
    *,
    title: str = "Metrics",
    style: str = STYLE_HEADER,
    console: Console | None = None,
) -> None:
    """Print a single-line panel of formatted metric values."""
    body = "    ".join(
        f"[bold {STYLE_METRIC}]{name}:[/] {format_metric(value)}" for name, value in metrics.items()
    )
    _resolve(console).print(Panel(body, title=f"[bold {style}]{title}[/]", border_style=style))


def two_column_panel(
    rows: Mapping[str, str],
    *,
    title: str,
    label_width: int = 12,
    style: str = STYLE_MUTED,
    console: Console | None = None,
) -> None:
    """Print a panel whose rows share a fixed-width label column."""
    table = Table(show_header=False, box=None, padding=(0, 1), show_edge=False)
    table.add_column("label", style=STYLE_MUTED, width=label_width)
    table.add_column("value")
    for label, value in rows.items():
        table.add_row(f"{label}:", value)
    _resolve(console).print(
        Panel(table, title=f"[bold {STYLE_HEADER}]{title}[/]", border_style=style)
    )


def new_progress_bar(
    *,
    console: Console | None = None,
    transient: bool = False,
) -> Progress:
    """Create a progress bar with a spinner, bar, completed count and elapsed time."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=_resolve(console),
        transient=transient,
    )
