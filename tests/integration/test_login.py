def test_unknown_email_does_not_crash(client):
    invalid_mail = "inconnu@test.com"
    response = client.post("/showSummary", data={"email": invalid_mail})

    assert response.status_code == 200


def test_unknown_email_shows_error_message(client):
    invalid_mail = "inconnu@test.com"
    response = client.post("/showSummary", data={"email": invalid_mail})

    assert "Sorry, that email wasn" in response.get_data(as_text=True)


def test_valid_email_does_not_crash(client):
    valid_mail = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": valid_mail})

    assert response.status_code == 200


def test_valid_email_shows_welcome_page(client):
    valid_mail = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": valid_mail})

    assert "Welcome, john@simplylift.co" in response.get_data(as_text=True)    


def test_valid_email_shows_club_points(client):
    valid_mail = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": valid_mail})

    assert "Points available: 13" in response.get_data(as_text=True)
