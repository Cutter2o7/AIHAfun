"""Contact data persistence utilities."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

__all__ = ["load_contacts", "save_contacts", "update_contact"]

DEFAULT_FILE = Path("contacts.json")


def load_contacts(path: Path | str = DEFAULT_FILE) -> List[Dict[str, Any]]:
    """Load contact data from a JSON file.

    Parameters
    ----------
    path:
        File path to read from. Defaults to ``contacts.json``.

    Returns
    -------
    list
        List of contact dictionaries. If the file doesn't exist, an empty
        list is returned.
    """
    file_path = Path(path)
    if not file_path.is_file():
        return []
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_contacts(
    contacts: List[Dict[str, Any]],
    path: Path | str = DEFAULT_FILE,
    *,
    backup: bool = True,
) -> None:
    """Save contact data to a JSON file, optionally creating a backup.

    Parameters
    ----------
    contacts:
        Iterable of contact dictionaries to save.
    path:
        Destination file path. Defaults to ``contacts.json``.
    backup:
        If ``True`` and the destination file exists, create a timestamped
        backup alongside it before overwriting.
    """
    file_path = Path(path)
    if backup and file_path.is_file():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.with_name(f"{file_path.stem}_{timestamp}{file_path.suffix}.bak")
        file_path.rename(backup_path)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)


def update_contact(
    contacts: List[Dict[str, Any]],
    name: str,
    **fields: Any,
) -> None:
    """Update a single contact's fields in-place.

    If the contact does not exist it will be created with the provided name.
    Remaining unspecified fields are left untouched.
    """
    for contact in contacts:
        if contact.get("name") == name:
            contact.update(fields)
            break
    else:
        new_contact = {"name": name}
        new_contact.update(fields)
        contacts.append(new_contact)

