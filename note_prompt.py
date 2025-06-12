from datetime import datetime

from contact_scheduler import (
    get_this_weeks_monthly_contact,
    get_this_months_quarterly_contact,
)
from contact_storage import load_contacts, save_contacts, update_contact, find_contact
from notes import prompt_for_update


def main() -> None:
    """Prompt the user to update notes for today's scheduled contact."""
    weekday = datetime.today().weekday()  # Monday is 0
    if weekday in (0, 1):
        contact_name = get_this_weeks_monthly_contact()
    elif weekday == 2:
        contact_name = get_this_months_quarterly_contact()
    else:
        contact_name = None

    if not contact_name:
        print("No contact notes scheduled today.")
        return

    contacts = load_contacts()
    contact = find_contact(contacts, contact_name)
    if contact:
        print(f"Existing notes for {contact_name}:\n{contact.get('notes', '')}\n")
    else:
        print(f"Contact {contact_name} not found. It will be added.")

    new_notes = prompt_for_update(contact_name)
    if new_notes is not None:
        update_contact(contacts, contact_name, notes=new_notes)
        save_contacts(contacts)


if __name__ == "__main__":
    main()
