import pytest
from server import (
    has_enough_points,
    has_enough_places,
    is_within_twelve_limit,
    is_valid_places_input,
    register_purchase,
    is_competition_in_the_future,
)


@pytest.fixture
def fake_club():
    return {"name": "Club A", "email": "a@test.com", "points": "10"}


@pytest.fixture
def fake_competition():
    return {
        "name": "Comp A",
        "date": "2030-01-01 10:00:00",
        "numberOfPlaces": "20",
        "bookings": {},
    }


def test_is_competition_in_the_future_with_future_date(fake_competition):
    assert is_competition_in_the_future(fake_competition)


def test_is_competition_in_the_future_is_false_with_past_date(fake_competition):
    fake_competition["date"] = "2020-01-01 10:00:00"
    assert not is_competition_in_the_future(fake_competition)


def test_has_enough_points_when_club_has_more(fake_club):
    assert has_enough_points(fake_club, 5)


def test_has_enough_points_when_club_has_the_exact_limit(fake_club):
    assert has_enough_points(fake_club, 10)


def test_has_enough_points_is_false_when_club_has_less(fake_club):
    assert not has_enough_points(fake_club, 11)


def test_has_enough_places_when_competition_has_more(fake_competition):
    assert has_enough_places(fake_competition, 2)


def test_has_enough_places_when_competition_has_exact_limit(fake_competition):
    assert has_enough_places(fake_competition, 20)


def test_has_enough_places_is_false_when_competition_has_less_places(fake_competition):
    assert not has_enough_places(fake_competition, 21)


def test_is_valid_places_input_rejects_empty_string():
    assert not is_valid_places_input("")


def test_is_valid_places_input_rejects_zero():
    assert not is_valid_places_input("0")


def test_is_valid_places_input_rejects_negative():
    assert not is_valid_places_input("-5")


def test_is_valid_places_input_rejects_string():
    assert not is_valid_places_input("abc")


def test_is_valid_places_input_rejects_float():
    assert not is_valid_places_input("0.5")


def test_is_valid_places_input_when_int():
    assert is_valid_places_input("1")


def test_is_within_twelve_limit_when_int(fake_competition, fake_club):
    assert is_within_twelve_limit(fake_competition, fake_club, 1)


def test_is_within_twelve_limit_when_exact_limit_when_one_time_purchase(fake_competition, fake_club):
    assert is_within_twelve_limit(fake_competition, fake_club, 12)


def test_is_within_twelve_limit_is_false_when_exceed_limit_when_one_time_purchase(fake_competition, fake_club):
    assert not is_within_twelve_limit(fake_competition, fake_club, 13)


def test_is_within_twelve_limit_when_exact_limit_when_previous_purchase_exist(fake_competition, fake_club):
    fake_competition["bookings"]["Club A"] = 7
    assert is_within_twelve_limit(fake_competition, fake_club, 5)


def test_is_within_twelve_limit_is_false_when_exceed_limit_when_previous_purchase_exist(fake_competition, fake_club):
    fake_competition["bookings"]["Club A"] = 7
    assert not is_within_twelve_limit(fake_competition, fake_club, 6)


def test_register_purchase_updates_points_places_and_bookings(fake_competition, fake_club):
    register_purchase(fake_competition, fake_club, 3)

    assert fake_club["points"] == 7
    assert fake_competition["numberOfPlaces"] == 17
    assert fake_competition["bookings"]["Club A"] == 3


def test_register_purchase_accumulates_over_several_purchases(fake_competition, fake_club):
    register_purchase(fake_competition, fake_club, 3)
    register_purchase(fake_competition, fake_club, 3)

    assert fake_club["points"] == 4
    assert fake_competition["numberOfPlaces"] == 14
    assert fake_competition["bookings"]["Club A"] == 6
