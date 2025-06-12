from datetime import datetime
from notes import prompt_for_update


def main() -> None:
    """Prompt the user to update notes based on the day of the week."""
    weekday = datetime.today().weekday()  # Monday is 0
    if weekday in (0, 1):
        prompt_for_update("monthly")
    elif weekday == 2:
        prompt_for_update("quarterly")
    else:
        print("No contact notes scheduled today.")


if __name__ == "__main__":
    main()
