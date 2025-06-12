# ☀️ Morning Routine Assistant

This is a customizable Python script that helps streamline your morning routine by automating access to Bible study tools, writing prompts, weather updates, and creative tasks like AI image generation.

---

## 📌 Features

- 📖 Fetches links to **Daily Dose of Hebrew and Greek** and retrieves the verse text from RapidAPI
- 🛠 Opens Bible study tools and documents
- ⏲ Runs countdown timers with a UI progress bar for prayer, language practice, study, and creative sessions, and includes a **Skip** button
- ☁️ Gets real-time **weather updates**
- ✍️ Prompts you to write scenes for your novel
- 🎨 Prompts you to generate AI-based images
- 📜 Displays a daily Bible verse (optional)
- 🗂 Generates a to-do list (optional)

---

## 🚀 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/morning-routine-assistant.git
   cd morning-routine-assistant
   ```

2. **Set environment variables** (`.env` file works):
   - `YOUTUBE_TOKEN` – token for YouTube Data API
   - `RAPIDAPI_KEY` – key for iq-bible API
   - `RAPIDAPI_HOST` – host value for iq-bible API
   - `HEBREW_TRANSLATION_FILE` – path to today's Hebrew translation spreadsheet
   - `GREEK_TRANSLATION_FILE` – path to today's Greek translation spreadsheet

## 📇 Contact Data Persistence

This repository now includes `contact_storage.py`, a utility module for
loading and saving your recurring contact lists. Contacts are stored in a
simple JSON file (`contacts.json`) with fields like `name`, `notes`, and
`next_call_due`. Use the helper functions to read the list on startup and
persist any updates back to disk.
