import json
from datetime import datetime
from pathlib import Path

NOTES_FILE = Path("notes.json")


def load_notes() -> dict:
    """Load notes from ``NOTES_FILE``.

    Returns a dictionary with ``monthly`` and ``quarterly`` keys.
    """
    if NOTES_FILE.is_file():
        with NOTES_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"monthly": {}, "quarterly": {}}


def save_notes(data: dict) -> None:
    """Write *data* back to ``NOTES_FILE``."""
    with NOTES_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def get_current_notes(contact_type: str) -> str:
    """Return the stored notes for ``contact_type`` or an empty string."""
    data = load_notes()
    entry = data.get(contact_type, {})
    return entry.get("current", "")


def update_notes(contact_type: str, new_text: str) -> None:
    """Replace the notes for ``contact_type`` with ``new_text`` and log history."""
    data = load_notes()
    entry = data.setdefault(contact_type, {})
    entry["current"] = new_text
    history = entry.setdefault("history", [])
    history.append({
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "text": new_text,
    })
    save_notes(data)


def prompt_for_update(contact_type: str) -> None:
    """Interactively prompt the user to revise notes for ``contact_type``."""
    current = get_current_notes(contact_type)
    if current:
        print(f"Current {contact_type} notes:\n{current}\n")
    else:
        print(f"No existing {contact_type} notes.\n")

    choice = input("Update these notes? (y/n) ").strip().lower()
    if choice != "y":
        return

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
        return
    update_notes(contact_type, new_text)
    print("Notes updated.")
