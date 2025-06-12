import json
import os
from datetime import datetime

DATA_FILE = "contacts_state.json"


def _load_state():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return {
        "monthly_contacts": [],
        "quarterly_contacts": [],
        "current_monthly_index": -1,
        "current_quarterly_index": -1,
        "week_start": None,
        "month_start": None,
        "called_this_week": False,
        "called_this_month": False,
    }


def _save_state(state):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
    except Exception:
        pass


def _current_week_key():
    today = datetime.now().isocalendar()
    return f"{today.year}-W{today.week}"


def _current_month_key():
    today = datetime.now()
    return f"{today.year}-{today.month:02d}"


def get_this_weeks_monthly_contact():
    """Return this week's contact from the monthly list and rotate if needed."""
    state = _load_state()
    week_key = _current_week_key()
    if state.get("week_start") != week_key:
        state["week_start"] = week_key
        state["current_monthly_index"] = (state.get("current_monthly_index", -1) + 1) % max(len(state["monthly_contacts"]), 1)
        state["called_this_week"] = False
        _save_state(state)
    idx = state.get("current_monthly_index", -1)
    if idx == -1 or not state["monthly_contacts"]:
        return None
    return state["monthly_contacts"][idx]


def get_this_months_quarterly_contact():
    """Return this month's contact from the quarterly list and rotate if needed."""
    state = _load_state()
    month_key = _current_month_key()
    if state.get("month_start") != month_key:
        state["month_start"] = month_key
        state["current_quarterly_index"] = (state.get("current_quarterly_index", -1) + 1) % max(len(state["quarterly_contacts"]), 1)
        state["called_this_month"] = False
        _save_state(state)
    idx = state.get("current_quarterly_index", -1)
    if idx == -1 or not state["quarterly_contacts"]:
        return None
    return state["quarterly_contacts"][idx]


def has_called_this_week():
    state = _load_state()
    return state.get("called_this_week", False)


def has_called_this_month():
    state = _load_state()
    return state.get("called_this_month", False)


def mark_called_this_week():
    state = _load_state()
    state["called_this_week"] = True
    _save_state(state)


def mark_called_this_month():
    state = _load_state()
    state["called_this_month"] = True
    _save_state(state)


def set_contact_lists(
    monthly: list[str] | None = None, quarterly: list[str] | None = None
) -> None:
    """Replace the stored contact name lists."""
    state = _load_state()
    if monthly is not None:
        state["monthly_contacts"] = list(monthly)
        state["current_monthly_index"] = -1
    if quarterly is not None:
        state["quarterly_contacts"] = list(quarterly)
        state["current_quarterly_index"] = -1
    _save_state(state)

def daily_prompt():
    """Print reminders for the current monthly and quarterly contacts."""
    monthly_contact = get_this_weeks_monthly_contact()
    quarterly_contact = get_this_months_quarterly_contact()
    if monthly_contact and not has_called_this_week():
        print(f"📞 Have you called {monthly_contact} this week?")
    if quarterly_contact and not has_called_this_month():
        print(f"📞 Have you called {quarterly_contact} this month?")

