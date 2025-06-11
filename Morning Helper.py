# === 1. Imports and Configuration ===
import os
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
def load_config():
    """Load user settings and environment variables."""
    load_dotenv()

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
    except Exception as err:
        print(f"Failed to retrieve Daily Dose of Greek video: {err}")

def open_bible_study_tools():
    """Open Bible tools, translation websites, and LibreOffice study doc."""
    pass

# === 3. Timers for Language and Study ===
def start_timer(name, minutes):
    """Start a named countdown timer for a given duration."""
    pass

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
    
    # --- Fetch and open Bible content ---
    fetch_daily_dose_hebrew()
    fetch_daily_dose_greek()
    open_bible_study_tools()
    
    # --- Run study timers ---
    run_study_timers()
    
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

