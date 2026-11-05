"""Progress skill: manage the paper-reading progress tracker."""

import json
from pathlib import Path

_PROGRESS_FILE = Path(__file__).parent.parent / "data" / "progress.json"


def fetch_pending_paper(progress_file: Path | None = None) -> list[str]:
    """Fetch one pending paper from the progress tracker and return its citation key.

    Args:
        progress_file: Optional path to the progress JSON file.
                       Defaults to ``data/progress.json`` at the repo root.

    Returns:
        A single-element list containing the citation key of the first pending
        paper, or an empty list when no pending papers remain.

    Raises:
        FileNotFoundError: If the progress JSON file does not exist.
        ValueError: If the progress JSON file contains invalid JSON.
    """
    path = Path(progress_file) if progress_file is not None else _PROGRESS_FILE
    try:
        with open(path) as f:
            progress: dict[str, str] = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Progress file not found: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in progress file {path}: {exc}") from exc

    for citation_key, status in progress.items():
        if status == "pending":
            return [citation_key]

    return []
