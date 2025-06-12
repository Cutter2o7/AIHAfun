import json
from datetime import datetime
from pathlib import Path

NOTES_FILE = Path("notes.json")


def load_notes() -> dict:
    """Load notes from ``NOTES_FILE``.

    The file stores a mapping of contact names to their note entries. If the
    file doesn't exist, an empty mapping is returned.
    """
    if NOTES_FILE.is_file():
        with NOTES_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_notes(data: dict) -> None:
    """Write *data* back to ``NOTES_FILE``."""
    with NOTES_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def get_current_notes(key: str) -> str:
    """Return the stored notes for ``key`` or an empty string."""
    data = load_notes()
    entry = data.get(key, {})
    return entry.get("current", "")


def update_notes(key: str, new_text: str) -> None:
    """Replace the notes for ``key`` with ``new_text`` and log history."""
    data = load_notes()
    entry = data.setdefault(key, {})
    entry["current"] = new_text
    history = entry.setdefault("history", [])
    history.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "text": new_text,
    })
    save_notes(data)


def prompt_for_update(key: str) -> str | None:
    """Interactively prompt the user to revise notes for ``key``."""
    current = get_current_notes(key)
    if current:
        print(f"Current notes for {key}:\n{current}\n")
    else:
        print(f"No existing notes for {key}.\n")

    choice = input("Update these notes? (y/n) ").strip().lower()
    if choice != "y":
        return None

    print("Enter new notes. Finish with a blank line:")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    new_text = "\n".join(lines)
    if not new_text:
        print("No changes made.")
        return None
    update_notes(key, new_text)
    print("Notes updated.")
    return new_text
