"""Post-checkout hook that flags dependency drift after a branch switch."""

import os
import subprocess
import sys
from collections.abc import Sequence

from utils.console import STYLE_HEADER, console

DEPENDENCY_FILES = ("pyproject.toml", "uv.lock")
BRANCH_CHECKOUT_FLAG = "1"


def dependency_files_changed(previous: str, current: str) -> list[str]:
    """List the dependency files that differ between two revisions.

    Args:
        previous: Revision checked out before the switch.
        current: Revision checked out after the switch.

    Returns:
        The changed dependency file paths, empty when nothing relevant changed.
    """
    completed = subprocess.run(
        ["git", "diff", "--name-only", previous, current, "--", *DEPENDENCY_FILES],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in completed.stdout.splitlines() if line]


def _hook_arguments(argv: Sequence[str]) -> tuple[str, str, str] | None:
    """Resolve the previous revision, the new revision and the checkout flag.

    pre-commit does not forward git's positional arguments to hooks. It consumes
    them and re-exposes them as ``PRE_COMMIT_*`` environment variables, so both
    sources have to be read.

    Args:
        argv: Positional arguments, as git passes them to a raw hook.

    Returns:
        The three values, or ``None`` when neither source supplies them.
    """
    if len(argv) >= 3:
        return argv[0], argv[1], argv[2]
    previous = os.environ.get("PRE_COMMIT_FROM_REF")
    current = os.environ.get("PRE_COMMIT_TO_REF")
    checkout_type = os.environ.get("PRE_COMMIT_CHECKOUT_TYPE")
    if previous and current and checkout_type:
        return previous, current, checkout_type
    return None


def main(argv: Sequence[str]) -> int:
    """Print a notice when a branch switch changed the dependency files.

    Reads the previous revision, the new revision, and the branch-checkout flag
    from argv when given, falling back to the ``PRE_COMMIT_FROM_REF`` /
    ``PRE_COMMIT_TO_REF`` / ``PRE_COMMIT_CHECKOUT_TYPE`` environment variables
    pre-commit sets, since pre-commit never forwards them as positional arguments.

    Args:
        argv: The previous revision, the new revision, and git's branch-checkout flag.

    Returns:
        Always zero, so a checkout never looks broken because of this hook.
    """
    arguments = _hook_arguments(argv)
    if arguments is None:
        return 0

    previous, current, checkout_type = arguments
    if checkout_type != BRANCH_CHECKOUT_FLAG:
        return 0

    try:
        changed = dependency_files_changed(previous, current)
    except (subprocess.CalledProcessError, OSError):
        return 0

    if changed:
        console.print(
            f"[bold {STYLE_HEADER}]{', '.join(changed)} changed on this branch — "
            f"run `make dev` to resync dependencies.[/]"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
