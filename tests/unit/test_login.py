from server import find_club_by_email


def test_find_club_by_email_returns_the_club():
    fake_clubs = [
        {"name": "Club A", "email": "a@test.com", "points": "10"},
        {"name": "Club B", "email": "b@test.com", "points": "5"},
    ]

    result = find_club_by_email(fake_clubs, "b@test.com")

    assert result["name"] == "Club B"


def test_find_club_by_email_returns_none_when_not_found():
    fake_clubs = [
            {"name": "Club A", "email": "a@test.com", "points": "10"},
            {"name": "Club B", "email": "b@test.com", "points": "5"},
        ]

    result = find_club_by_email(fake_clubs, "c@test.com")

    assert result is None


def test_find_club_by_email_returns_none_when_list_is_empty():
    fake_clubs = []

    result = find_club_by_email(fake_clubs, "a@test.com") 

    assert result is None
