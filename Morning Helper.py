# === 1. Imports and Configuration ===
import os
import re
import requests
import time
import shutil
import subprocess
import webbrowser
from pathlib import Path

try:
    import uno  # LibreOffice UNO API for Calc automation
except ImportError:  # noqa: W0707
    uno = None
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Mapping of Bible books to numerical codes used by the IQ Bible API
BOOK_CODES = {
    "Genesis": 1,
    "Exodus": 2,
    "Leviticus": 3,
    "Numbers": 4,
    "Deuteronomy": 5,
    "Joshua": 6,
    "Judges": 7,
    "Ruth": 8,
    "1 Samuel": 9,
    "2 Samuel": 9,
    "Samuel": 9,
    "1 Kings": 10,
    "2 Kings": 10,
    "Kings": 10,
    "1 Chronicles": 11,
    "2 Chronicles": 11,
    "Chronicles": 11,
    "Ezra": 12,
    "Nehemiah": 12,
    "Ezra-Nehemiah": 12,
    "Esther": 13,
    "Job": 14,
    "Psalms": 15,
    "Proverbs": 16,
    "Ecclesiastes": 17,
    "Song of Songs": 18,
    "Song of Solomon": 18,
    "Isaiah": 19,
    "Jeremiah": 20,
    "Lamentations": 21,
    "Ezekiel": 22,
    "Daniel": 23,
    "Hosea": 24,
    "Joel": 25,
    "Amos": 26,
    "Obadiah": 27,
    "Jonah": 28,
    "Micah": 29,
    "Nahum": 30,
    "Habakkuk": 31,
    "Zephaniah": 32,
    "Haggai": 33,
    "Zechariah": 34,
    "Malachi": 35,
    "Matthew": 36,
    "Mark": 37,
    "Luke": 38,
    "John": 39,
    "Acts": 40,
    "Romans": 41,
    "1 Corinthians": 42,
    "2 Corinthians": 43,
    "Galatians": 44,
    "Ephesians": 45,
    "Philippians": 46,
    "Colossians": 47,
    "1 Thessalonians": 48,
    "2 Thessalonians": 49,
    "1 Timothy": 50,
    "2 Timothy": 51,
    "Titus": 52,
    "Philemon": 53,
    "Hebrews": 54,
    "James": 55,
    "1 Peter": 56,
    "2 Peter": 57,
    "1 John": 58,
    "2 John": 59,
    "3 John": 60,
    "Jude": 61,
    "Revelation": 62,
}

def parse_reference(title):
    """Extract verse information from a video title."""
    pattern = r"([1-3]?\s?[A-Za-z ]+?)\s+(\d+):(\d+)"
    match = re.search(pattern, title)
    if not match:
        return None

    book_name = match.group(1).strip()
    # Normalize spacing and capitalization for lookup
    book_key = " ".join(word.capitalize() for word in book_name.split())
    book_id = BOOK_CODES.get(book_key)
    if book_id is None:
        return None
    chapter = int(match.group(2))
    verse = int(match.group(3))
    return f"{book_id:02d}{chapter:03d}{verse:03d}"

def load_config():
    """Load user settings and environment variables."""
    load_dotenv()


def open_translation_spreadsheet(env_var):
    """Copy the spreadsheet referenced by env_var to the Desktop and open it."""
    path = os.getenv(env_var)
    if not path:
        print(f"{env_var} not configured in .env")
        return
    src = Path(path).expanduser()
    if not src.is_file():
        print(f"Translation file not found: {src}")
        return
    desktop = Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    dest = desktop / src.name
    try:
        shutil.copy(src, dest)
    except Exception as err:
        print(f"Failed to copy translation file: {err}")
        return

    # Attempt to use LibreOffice UNO to open the spreadsheet
    if uno is not None:
        try:
            local_ctx = uno.getComponentContext()
            resolver = local_ctx.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", local_ctx
            )
            ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
            )
            desktop_srv = ctx.ServiceManager.createInstanceWithContext(
                "com.sun.star.frame.Desktop", ctx
            )
            desktop_srv.loadComponentFromURL(dest.as_uri(), "_blank", 0, tuple())
            return
        except Exception as err:
            print(f"UNO open failed: {err}")

    # Fallback to launching LibreOffice directly
    try:
        subprocess.Popen(["libreoffice", "--calc", str(dest)])
    except Exception as err:
        print(f"Failed to open translation file {dest}: {err}")

# === 2. Fetch Content ===
def fetch_daily_dose_hebrew():
    """Fetch and display the latest Daily Dose of Hebrew video."""
    # Load API token from .env
    load_dotenv()
    api_key = os.getenv("YOUTUBE_TOKEN")
    if not api_key:
        print("YOUTUBE_TOKEN is not set in the environment")
        return

    # Initialize YouTube client
    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        # Determine channel ID for Daily Dose of Hebrew
        channel_search = (
            youtube.search()
            .list(q="Daily Dose of Hebrew", type="channel", part="id", maxResults=1)
            .execute()
        )
        channel_id = channel_search["items"][0]["id"]["channelId"]

        # Get the most recent video from the channel
        video_search = (
            youtube.search()
            .list(
                channelId=channel_id,
                part="id,snippet",
                order="date",
                maxResults=1,
                type="video",
            )
            .execute()
        )

        item = video_search["items"][0]
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"Daily Dose of Hebrew: {title}\n{url}")

        # Open today's translation spreadsheet
        open_translation_spreadsheet("HEBREW_TRANSLATION_FILE")

        verse_id = parse_reference(title)
        if verse_id:
            api_key_rapid = os.getenv("RAPIDAPI_KEY")
            api_host = os.getenv("RAPIDAPI_HOST")
            if api_key_rapid and api_host:
                headers = {
                    "x-rapidapi-key": api_key_rapid,
                    "x-rapidapi-host": api_host,
                }
                try:
                    resp = requests.get(
                        "https://iq-bible.p.rapidapi.com/GetOriginalText",
                        headers=headers,
                        params={"verseId": verse_id},
                        timeout=10,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    print(data)
                except Exception as err:
                    print(f"Failed to fetch verse text: {err}")
            else:
                print("RAPIDAPI credentials not set in environment")
        else:
            print("Unable to parse verse reference from title")

        webbrowser.open(url)
    except Exception as err:
        print(f"Failed to retrieve Daily Dose of Hebrew video: {err}")

def fetch_daily_dose_greek():
    """Fetch and display the latest Daily Dose of Greek video."""
    # Load API token from .env
    load_dotenv()
    api_key = os.getenv("YOUTUBE_TOKEN")
    if not api_key:
        print("YOUTUBE_TOKEN is not set in the environment")
        return

    # Initialize YouTube client
    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        # Determine channel ID for Daily Dose of Greek
        channel_search = (
            youtube.search()
            .list(q="Daily Dose of Greek", type="channel", part="id", maxResults=1)
            .execute()
        )
        channel_id = channel_search["items"][0]["id"]["channelId"]

        # Get the most recent video from the channel
        video_search = (
            youtube.search()
            .list(
                channelId=channel_id,
                part="id,snippet",
                order="date",
                maxResults=1,
                type="video",
            )
            .execute()
        )

        item = video_search["items"][0]
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"Daily Dose of Greek: {title}\n{url}")

        # Open today's translation spreadsheet
        open_translation_spreadsheet("GREEK_TRANSLATION_FILE")
        webbrowser.open(url)
    except Exception as err:
        print(f"Failed to retrieve Daily Dose of Greek video: {err}")

def open_bible_study_tools():
    """Open Bible tools, translation websites, and LibreOffice study doc."""
    pass

# === 3. Timers for Language and Study ===
def start_timer(name, minutes):
    """Start a named countdown timer with a Tkinter progress bar."""
    import tkinter as tk
    from tkinter import ttk

    total_seconds = int(minutes * 60)

    root = tk.Tk()
    root.title(f"{name} Timer")

    progress_var = tk.DoubleVar(value=0)
    progress = ttk.Progressbar(
        root,
        maximum=total_seconds,
        length=300,
        variable=progress_var,
    )
    progress.pack(padx=20, pady=10)

    label = tk.Label(root, text=f"Time remaining: {minutes:02d}:00")
    label.pack()

    def update():
        nonlocal total_seconds
        mins, secs = divmod(total_seconds, 60)
        label.config(text=f"Time remaining: {mins:02d}:{secs:02d}")
        progress_var.set((minutes * 60) - total_seconds)
        if total_seconds > 0:
            total_seconds -= 1
            root.after(1000, update)
        else:
            label.config(text=f"{name} complete!")
            progress_var.set(minutes * 60)
            root.after(2000, root.destroy)

    def skip_timer():
        nonlocal total_seconds
        total_seconds = 0
        update()

    skip_button = tk.Button(root, text="Skip", command=skip_timer)
    skip_button.pack(pady=5)

    update()
    root.mainloop()

def run_study_timers():
    """Run timers for Hebrew, Greek, and Bible study sessions."""
    start_timer("Hebrew", 10)
    start_timer("Greek", 10)
    start_timer("Bible Study", 30)

# === 4. Weather ===
def fetch_weather():
    """Fetch and display the hourly weather forecast for the next two days."""
    from datetime import datetime, timezone, timedelta

    # Coordinates for 32°41'00.8"N 97°24'51.2"W
    latitude = 32.683556
    longitude = -97.414222

    # Step 1: Get the hourly forecast URL from the /points endpoint
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    try:
        response = requests.get(points_url, timeout=10)
        response.raise_for_status()
        forecast_url = response.json()["properties"]["forecastHourly"]
    except (requests.RequestException, KeyError) as err:
        print(f"Unable to determine hourly forecast URL: {err}")
        return

    # Step 2: Retrieve the hourly forecast
    try:
        forecast_resp = requests.get(forecast_url, timeout=10)
        forecast_resp.raise_for_status()
        periods = forecast_resp.json()["properties"]["periods"]
    except (requests.RequestException, KeyError) as err:
        print(f"Unable to fetch forecast data: {err}")
        return

    # Filter to the next two days
    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=2)

    print("\nHourly Forecast (next 48 hours):")
    for period in periods:
        start_time_str = period.get("startTime")
        if not start_time_str:
            continue
        try:
            start_time = datetime.fromisoformat(start_time_str)
        except ValueError:
            # If timezone info is missing, assume UTC
            start_time = datetime.fromisoformat(start_time_str + "+00:00")
        if start_time >= cutoff:
            break

        name = period.get("name") or start_time.strftime("%a %I %p")
        short = period.get("shortForecast")
        temp = period.get("temperature")
        unit = period.get("temperatureUnit", "")
        print(f"{name}: {temp}{unit}, {short}")

# === 5. Novel Writing Prompt ===
def prompt_novel_scene_writing():
    """Display prompt and open tools for novel writing."""
    print("📝 Write 2 scenes for your novel today!")
    open_novel_resources()
    start_timer("Scene Writing", 15)

def open_novel_resources():
    """Open writing website and LibreOffice document for scene writing."""
    pass

# === 6. Image Generation Prompt ===
def prompt_image_generation():
    """Display prompt and open tools for AI art generation."""
    print("🎨 Generate 2 images based on your scenes or ideas!")
    open_image_resources()
    start_timer("Image Generation", 15)

def open_image_resources():
    """Open AI art website or local tool and image save folder."""
    pass

# === 7. Optional Extras ===
def display_daily_verse():
    """Fetch and display a daily Bible verse."""
    pass

def generate_todo_list():
    """Generate or display the day’s to-do list."""
    pass

# === 8. Main Routine ===
def main():
    load_config()

    # --- Timed study routine ---
    start_timer("Prayer Timer", 5)

    # Daily Dose of Hebrew followed by practice
    fetch_daily_dose_hebrew()
    start_timer("Daily Hebrew Practice", 10)

    # Daily Dose of Greek followed by practice
    fetch_daily_dose_greek()
    start_timer("Daily Greek Practice", 10)

    # Open study tools then timed study session
    open_bible_study_tools()
    start_timer("Daily study", 10)
    
    # --- Post-study weather check ---
    fetch_weather()
    
    # --- Writing task ---
    prompt_novel_scene_writing()
    
    # --- Art task ---
    prompt_image_generation()
    
    # --- Optional extras (if enabled) ---
    display_daily_verse()
    generate_todo_list()

if __name__ == "__main__":
    main()

