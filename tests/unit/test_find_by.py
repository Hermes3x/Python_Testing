from server import find_by
import pytest


@pytest.fixture
def fake_clubs():
    return [
        {"name": "Club A", "email": "a@test.com", "points": "10"},
        {"name": "Club B", "email": "b@test.com", "points": "5"},
    ]


def test_find_by_returns_the_club(fake_clubs):
    result = find_by(fake_clubs, "name", "Club A")

    assert result["name"] == "Club A"


def test_find_by_returns_none_when_not_found(fake_clubs):
    result = find_by(fake_clubs, "name", "Club C")

    assert result is None

def test_find_by_returns_none_when_list_is_empty():
    fake_clubs = []

    result = find_by(fake_clubs,"name", "Club A")

    assert result is None


def test_find_by_works_with_another_key(fake_clubs):
    result = find_by(fake_clubs, "email", "a@test.com")

    assert result["name"] == "Club A"


def test_find_by_works_on_any_list_shape():

    fake_competitions = [
        {"name": "Competition A", "date": "2021-03-27 10:00:00", "numberOfPlaces": "15"},
        {"name": "Competition B", "date": "2021-12-15 10:00:00", "numberOfPlaces": "24"},
    ]

    result = find_by(fake_competitions, "name", "Competition A")

    assert result["name"] == "Competition A"
