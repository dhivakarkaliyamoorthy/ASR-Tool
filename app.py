"""
Voice-Based Timetable Assistant
ASR (Automatic Speech Recognition) project.

The user speaks a timetable question such as:
"What class do I have at 10 AM?"

The application:
1. Captures speech from the microphone.
2. Converts speech to text using SpeechRecognition.
3. Extracts the requested time.
4. Searches timetable.json.
5. Displays and speaks the answer.
"""

import json
import re
from datetime import datetime
from pathlib import Path

import speech_recognition as sr

TIMETABLE_FILE = Path(__file__).parent / "timetable.json"


def load_timetable():
    """Load timetable data from timetable.json."""
    with open(TIMETABLE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_time(time_text):
    """Convert common time formats to HH:MM, e.g. '10 AM' -> '10:00'."""
    cleaned = time_text.strip().lower().replace(".", "")
    cleaned = re.sub(r"\s+", " ", cleaned)

    patterns = [
        (r"^(\d{1,2})\s*(am|pm)$", "%I %p"),
        (r"^(\d{1,2}):(\d{2})\s*(am|pm)$", "%I:%M %p"),
        (r"^(\d{1,2}):(\d{2})$", "%H:%M"),
        (r"^(\d{1,2})\s*(am|pm)\s*$", "%I %p"),
    ]

    for pattern, fmt in patterns:
        match = re.match(pattern, cleaned)
        if match:
            try:
                value = datetime.strptime(cleaned, fmt)
                return value.strftime("%H:%M")
            except ValueError:
                pass

    return None


def extract_time(query):
    """Extract a time from a natural-language timetable question."""
    text = query.lower().replace(".", "")

    # 10:30 AM / 10:30PM
    match = re.search(r"\b(\d{1,2}):(\d{2})\s*(am|pm)\b", text)
    if match:
        return normalize_time(match.group(0))

    # 10 AM / 10PM
    match = re.search(r"\b(\d{1,2})\s*(am|pm)\b", text)
    if match:
        return normalize_time(match.group(0))

    # 10:30 (24-hour style)
    match = re.search(r"\b([01]?\d|2[0-3]):([0-5]\d)\b", text)
    if match:
        return normalize_time(match.group(0))

    return None


def find_class(query, day=None):
    """
    Search the timetable using a natural-language query.

    Returns:
        A dictionary with class details, or None if no matching class exists.
    """
    timetable = load_timetable()
    requested_time = extract_time(query)

    if requested_time is None:
        return None

    if day is None:
        day = datetime.now().strftime("%A")

    day = day.capitalize()

    for item in timetable:
        if item["day"].lower() == day.lower() and item["start_time"] == requested_time:
            return item

    return None


def answer_query(query, day=None):
    """Return a human-readable answer for a timetable question."""
    result = find_class(query, day=day)

    if result:
        return (
            f"You have {result['subject']} from {format_time(result['start_time'])} "
            f"to {format_time(result['end_time'])} in {result['room']}."
        )

    requested_time = extract_time(query)
    if requested_time:
        return f"No class is scheduled at {format_time(requested_time)} on {day or datetime.now().strftime('%A')}."

    return "I could not find a time in your question. Please ask something like: What class do I have at 10 AM?"


def format_time(value):
    """Format HH:MM into a user-friendly 12-hour time."""
    return datetime.strptime(value, "%H:%M").strftime("%I:%M %p").lstrip("0")


def listen_for_question():
    """Capture speech from the microphone and convert it to text."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Speak your timetable question.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)

    try:
        # Google Web Speech API is used for ASR.
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as exc:
        raise RuntimeError(
            "Speech recognition service is unavailable. Check your internet connection."
        ) from exc


def speak_answer(text):
    """Speak the answer using pyttsx3 when available."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        # Text output remains available if speech synthesis is unavailable.
        pass


def main():
    print("=" * 60)
    print("       VOICE-BASED TIMETABLE ASSISTANT")
    print("=" * 60)
    print("Example: What class do I have at 10 AM?")
    print("Press Ctrl+C to exit.\n")

    while True:
        try:
            query = listen_for_question()

            if not query:
                print("Sorry, I could not understand your speech.\n")
                continue

            print(f"You said: {query}")
            response = answer_query(query)
            print(f"Assistant: {response}\n")
            speak_answer(response)

        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.\n")
        except KeyboardInterrupt:
            print("\nExiting. Goodbye!")
            break
        except Exception as exc:
            print(f"Error: {exc}\n")


if __name__ == "__main__":
    main()
