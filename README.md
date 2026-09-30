# Voice-Based Timetable Assistant

An **ASR (Automatic Speech Recognition)** project that lets a student ask a timetable question using their voice.

### Example

> 🎤 "What class do I have at 10 AM?"

The application converts the spoken question into text, extracts the requested time, searches the stored timetable, and responds with the class and room.

## Features

- Voice input through a microphone
- Automatic Speech Recognition using `SpeechRecognition`
- Natural-language time extraction
- Timetable stored in a simple JSON file
- Class and room lookup
- Text response
- Optional voice response using `pyttsx3`
- Test cases using `pytest`

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| SpeechRecognition | Converts speech into text |
| Google Web Speech API | ASR service used by SpeechRecognition |
| PyAudio | Microphone/audio input |
| pyttsx3 | Converts the response to speech |
| JSON | Stores timetable data |
| pytest | Testing |

## Project Structure

```text
voice-based-timetable-assistant/
│
├── app.py
├── timetable.json
├── requirements.txt
├── requirements-dev.txt
├── test_app.py
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or newer
- Working microphone
- Internet connection for Google Web Speech recognition
- Windows/macOS/Linux

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/voice-based-timetable-assistant.git
cd voice-based-timetable-assistant
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For testing:

```bash
pip install -r requirements-dev.txt
```

### PyAudio installation note

If `pip install -r requirements.txt` fails specifically while installing `PyAudio` on Windows, try:

```bash
pip install pipwin
pipwin install pyaudio
```

Then run:

```bash
pip install SpeechRecognition pyttsx3
```

## Run the Project

```bash
python app.py
```

You will see:

```text
VOICE-BASED TIMETABLE ASSISTANT
Example: What class do I have at 10 AM?
```

Speak a question such as:

```text
What class do I have at 10 AM?
```

The application will convert your voice to text and search the timetable.

## Testing

Run:

```bash
pytest -q
```

The tests check:

- Time conversion
- Time extraction from questions
- Timetable lookup
- Missing-class handling
- Generated answers

The automated tests do not require a microphone because they test the timetable and query-processing logic separately from live ASR.

## Customizing the Timetable

Open:

```text
timetable.json
```

Each class follows this format:

```json
{
    "day": "Monday",
    "start_time": "10:00",
    "end_time": "11:00",
    "subject": "Database Management Systems",
    "room": "Room 204"
}
```

You can replace the sample timetable with your own college timetable.

## How It Works

```text
User speaks
     ↓
Microphone
     ↓
SpeechRecognition
     ↓
Google Web Speech API
     ↓
Speech converted to text
     ↓
Time extracted from question
     ↓
timetable.json searched
     ↓
Class + room found
     ↓
Answer displayed and spoken
```

## Example

Input:

```text
What class do I have at 10 AM?
```

If Monday is selected/current day and the timetable contains a Monday 10:00 class:

```text
You have Database Management Systems from 10:00 AM to 11:00 AM in Room 204.
```

## Limitations

- Google Web Speech recognition requires an internet connection.
- Recognition accuracy depends on microphone quality and speech clarity.
- The timetable is stored locally in JSON and must be updated manually.
- The current version searches the current day unless a day is supplied to the Python function.
- Live microphone testing requires a computer with a working microphone.

## Future Improvements

- Add a graphical web interface.
- Add voice commands for different days.
- Add "next class" functionality.
- Add timetable upload through CSV/Excel.
- Store timetable data in MySQL.
- Add an offline ASR model such as Vosk or Whisper.
- Add reminders for upcoming classes.

## Team Members

| S. No. | Name | Register Number |
|---:|---|---|
| 1 | Shreyas | 12345678 |
| 2 | Iyer | 2333 |

## License

This project is intended for educational and academic use.
