def test_unknown_competition_does_not_crash(client):
    response = client.get("/book/Nope/Simply%20Lift")

    assert response.status_code != 500


def test_unknown_club_does_not_crash(client):
    response = client.get("/book/Winter%20Challenge/Nope")

    assert response.status_code != 500


def test_valid_booking_page_shows_competition(client):
    response = client.get("/book/Winter%20Challenge/Simply%20Lift")

    assert "Winter Challenge" in response.get_data(as_text=True)


def test_booking_a_competition_in_the_past_is_impossible(client):
    response = client.get("/book/Spring%20Festival/Simply%20Lift")

    assert "Sorry, this competition is over" in response.get_data(as_text=True)


def test_booking_page_is_not_shown_for_past_competition(client):
    response = client.get("/book/Spring%20Festival/Simply%20Lift")

    assert "How many places?" not in response.get_data(as_text=True)
