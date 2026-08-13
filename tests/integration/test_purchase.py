def test_purchase_deducts_points_from_club(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Simply Lift",
        "places": "3"
    })

    assert "Points available: 10" in response.get_data(as_text=True)


def test_cannot_buy_more_places_than_points(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Iron Temple",
        "places": "6"
    })

    assert "Sorry, you are trying to purchase more places than your available points" in response.get_data(as_text=True)
    assert "Points available: 4" in response.get_data(as_text=True)


def test_purchase_with_unknown_club_does_not_crash(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Nope",
        "places": "1"
    })

    assert "Something went wrong" in response.get_data(as_text=True)


def test_purchase_more_places_than_available_is_not_allowed(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Simply Lift",
        "places": "12"
    })

    assert "Not enough places are available" in response.get_data(as_text=True)
    assert "Number of Places: 10" in response.get_data(as_text=True)
