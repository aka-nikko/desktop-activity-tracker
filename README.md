# Desktop Activity Tracker
## Overview
A privacy-conscious productivity tracker for Windows that logs app usage, keystrokes (with sensitive input redaction), idle time, and generates daily summaries using OpenAI GPT.

---

## Features

- **Window Tracking:** Logs active window changes and durations.
- **Keystroke Logging:** Tracks keystrokes, batches logs, and redacts sensitive input (e.g., passwords).
- **Idle Detection:** Detects and logs periods of user inactivity.
- **Daily Summaries:** Uses OpenAI GPT to generate a summary of your day based on tracked data.
- **Credential Security:** Encrypts and stores sensitive credentials using Fernet symmetric encryption.
- **Hotkey Trigger:** Press a defined hotkey anytime to generate a summary on demand.
- **Nightly Automation:** Automatically generates a summary at 23:59 each day.
- **System Tray Control:** Minimal UI with a tray icon to start/stop tracking, trigger summaries, and access config files.

---

## Getting Started

### Prerequisites

- Python 3.9+
- Windows OS
- [OpenAI API Key](https://platform.openai.com/account/api-keys)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/desktop-activity-tracker.git
    cd desktop-activity-tracker
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv myenv
    myenv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your `.env` file:**
    ```
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

5. **Configure app settings:**

    Edit config/settings.json to customize log paths, summary time, batch size, and GPT model. See the Configuration section for details.

---

## Usage

Start the tracker directly with:

```sh
python main.py
```

- The app will run in the background, logging activity and generating summaries.
- Press `Ctrl+Shift+S` to manually generate a summary.
- Summaries are saved in the `logs/` directory.

Or, use the system tray interface with:

```sh
python launcher.py
```

- Adds a tray icon with controls to start/stop tracking, trigger summaries, and open config files.
- Clean, minimal UI for quick access and control.

---

## Configuration
All runtime settings are stored in a settings.json file. Below is a description of each key:
| Key                  | Description                                                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `LOG_DIR`            | Directory where log files are stored.                                                                                  |
| `DB_PATH`            | Directory where the SQLite database is located.                                                                        |
| `DB_FILE`            | Name of the SQLite database file that stores activity data.                                                            |
| `FERNET_KEY_PATH`    | Directory containing the encryption key used for secure data (Fernet).                                                 |
| `CREDS_FILE_PATH`    | Path to files containing sensitive credentials (e.g., username, passwords).                                            |
| `SENSITIVE_KEYWORDS` | List of keywords that are considered sensitive (e.g., login, password, auth). Used to mask or ignore certain activity. |
| `BATCH_SIZE`         | Number of keystroke entries to collect before writing to the database.                                                 |
| `FLUSH_INTERVAL`     | Interval in seconds to flush the collected activity data to the database.                                              |
| `SUMMARY_TRIGGER`    | Hotkey combination to manually trigger activity summary. Example: `<ctrl>+<shift>+s`                                   |
| `SUMMARY_HOUR`       | Hour (24-hour format) to automatically generate daily summary.                                                         |
| `SUMMARY_MINUTE`     | Minute of the hour when the daily summary is triggered.                                                                |
| `GPT_MODEL`          | OpenAI model used for summarization (e.g., `gpt-3.5-turbo`).                                                           |


## Project Structure

```
.
├── main.py
├── launcher.txt
├── requirements.txt
├── .env
├── logs/
├── config/
│   └── settings.py
├── logging_utils/
│   └── logger.py
├── storage/
│   ├── db.py
│   └── security.py
├── summarizer/
│   └── gpt_summary.py
└── tracker/
    ├── idle_detector.py
    ├── keystroke_tracker.py
    └── window_tracker.py
```

---

## Security & Privacy

- Sensitive keystrokes (e.g., passwords) are redacted and never stored in plain text.
- Credentials are encrypted using Fernet and stored in `assets/creds.bin`.
- Your OpenAI API key is loaded from the `.env` file and never logged.

---

## Screenshots
### Logging
![Logging](https://github.com/aka-nikko/desktop-activity-tracker/blob/main/screenshots/logging.png)
### Summary
![Summary](https://github.com/aka-nikko/desktop-activity-tracker/blob/main/screenshots/gpt-summary.png)
### Tray UI
![Tray_icon](https://github.com/aka-nikko/desktop-activity-tracker/blob/main/screenshots/tray_icon.png)

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Credits

- Built with [python-dotenv](https://github.com/theskumar/python-dotenv), [pynput](https://github.com/moses-palmer/pynput), [cryptography](https://cryptography.io/),
