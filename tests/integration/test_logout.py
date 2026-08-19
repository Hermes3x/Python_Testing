def test_logout_redirects(client):
    response = client.get("/logout")
    assert response.status_code == 302


def test_logout_lands_on_index(client):
    response = client.get("/logout", follow_redirects=True)
    assert "Welcome to the GUDLFT Registration Portal!" in response.get_data(as_text=True)
