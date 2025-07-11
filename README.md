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
- **Hotkey Trigger:** Press `Ctrl+Shift+S` anytime to generate a summary on demand.
- **Nightly Automation:** Automatically generates a summary at 23:59 each day.

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

---

## Usage

Start the tracker with:

```sh
python main.py
```

- The app will run in the background, logging activity and generating summaries.
- Press `Ctrl+Shift+S` to manually generate a summary.
- Summaries are saved in the `logs/` directory.

---

## Project Structure

```
.
├── main.py
├── requirements.txt
├── .env
├── logs/
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
- Credentials are encrypted using Fernet and stored in `logs/creds.bin`.
- Your OpenAI API key is loaded from the `.env` file and never logged.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Credits

- Built with [python-dotenv](https://github.com/theskumar/python-dotenv), [pynput](https://github.com/moses-palmer/pynput), [cryptography](https://cryptography.io/),