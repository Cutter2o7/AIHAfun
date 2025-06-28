# === 1. Imports and Configuration ===
import os
import requests
import subprocess
import webbrowser

try:
    import uno  # LibreOffice UNO API for Calc automation
except ImportError:  # noqa: W0707
    uno = None
from dotenv import load_dotenv
from daily_dose import fetch_daily_dose
load_dotenv()


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

    # --- Timed study routine ---
    #start_timer("Prayer Timer", 5)

    # Daily Dose of Hebrew followed by practice
    fetch_daily_dose("hebrew")
    start_timer("Daily Hebrew Practice", 10)

    # Daily Dose of Greek followed by practice
    fetch_daily_dose("greek")
    start_timer("Daily Greek Practice", 10)

    # Open study tools then timed study session
    open_bible_study_tools()
    start_timer("Daily study", 10)
    
    # --- Post-study weather check ---
    fetch_weather()
    
    # --- Writing task ---
    #prompt_novel_scene_writing()
    
    # --- Art task ---
    #prompt_image_generation()
    
    # --- Optional extras (if enabled) ---
    #display_daily_verse()
    #generate_todo_list()

if __name__ == "__main__":
    main()
