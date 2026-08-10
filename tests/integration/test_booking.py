def test_unknown_competition_does_not_crash(client):
    response = client.get("/book/Nope/Simply%20Lift")

    assert response.status_code != 500


def test_unknown_club_does_not_crash(client):
    response = client.get("/book/Spring%20Festival/Nope")

    assert response.status_code != 500

def test_valid_booking_page_shows_competition(client):
    response = client.get("/book/Spring%20Festival/Simply%20Lift")

    assert "Spring Festival" in response.get_data(as_text=True)
