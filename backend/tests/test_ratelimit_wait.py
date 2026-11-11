from app.services.ratelimit import human_wait


def test_human_wait_speaks_in_minutes_under_an_hour():
    assert human_wait(2220) == "about 37 minutes"


def test_human_wait_says_one_minute():
    assert human_wait(60) == "about 1 minute"


def test_human_wait_switches_to_hours():
    assert human_wait(21600) == "about 6 hours"


def test_human_wait_switches_to_days():
    assert human_wait(86400) == "about 1 day"
