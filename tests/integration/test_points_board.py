def test_points_board_is_accessible(client):
    response = client.get("/pointsBoard")
    assert response.status_code == 200


def test_points_board_shows_all_clubs(client):
    response = client.get("/pointsBoard")
    assert "Simply Lift" in response.get_data(as_text=True)
    assert "Iron Temple" in response.get_data(as_text=True)
    assert "She Lifts" in response.get_data(as_text=True)


def test_points_board_shows_points(client):
    response = client.get("/pointsBoard")
    assert "Number of Points: 13" in response.get_data(as_text=True)
    assert "Number of Points: 4" in response.get_data(as_text=True)
    assert "Number of Points: 12" in response.get_data(as_text=True)


def test_points_board_has_no_booking_links(client):
    response = client.get("/pointsBoard")
    assert "Book" not in response.get_data(as_text=True)


def test_index_links_to_points_board(client):
    response = client.get("/")
    assert "/pointsBoard" in response.get_data(as_text=True)
