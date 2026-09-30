import app


def test_normalize_time():
    assert app.normalize_time("10 AM") == "10:00"
    assert app.normalize_time("2:30 PM") == "14:30"
    assert app.normalize_time("14:30") == "14:30"


def test_extract_time():
    assert app.extract_time("What class do I have at 10 AM?") == "10:00"
    assert app.extract_time("What do I have at 2:30 PM?") == "14:30"
    assert app.extract_time("Tell me my class at 10:00") == "10:00"


def test_find_monday_class():
    result = app.find_class("What class do I have at 10 AM?", day="Monday")
    assert result is not None
    assert result["subject"] == "Database Management Systems"
    assert result["room"] == "Room 204"


def test_no_class():
    result = app.find_class("What class do I have at 2 PM?", day="Monday")
    assert result is None


def test_answer_query():
    answer = app.answer_query("What class do I have at 10 AM?", day="Monday")
    assert "Database Management Systems" in answer
    assert "Room 204" in answer


def test_missing_time():
    answer = app.answer_query("What class do I have?", day="Monday")
    assert "could not find a time" in answer.lower()
