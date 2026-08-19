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

    assert "Sorry, you do not have enough points for that many places." in response.get_data(as_text=True)
    assert "Points available: 4" in response.get_data(as_text=True)


def test_purchase_with_unknown_club_does_not_crash(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Nope",
        "places": "1"
    })

    assert "Sorry, we could not find that club or competition." in response.get_data(as_text=True)


def test_purchase_more_places_than_available_is_not_allowed(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Simply Lift",
        "places": "12"
    })

    assert "Sorry, there are not enough places left in this competition." in response.get_data(as_text=True)
    assert "Number of Places: 10" in response.get_data(as_text=True)


def test_successive_purchases_deduct_points_cumulatively(client):
    response = client.post("/purchasePlaces", data={
            "competition": "Winter Challenge",
            "club": "Simply Lift",
            "places": "3"
        })

    assert "Points available: 10" in response.get_data(as_text=True)

    response = client.post("/purchasePlaces", data={
                "competition": "Winter Challenge",
                "club": "Simply Lift",
                "places": "3"
            })

    assert "Points available: 7" in response.get_data(as_text=True)


def test_purchase_12_places_max(client):
    client.post("/purchasePlaces", data={
            "competition": "Summer Con",
            "club": "Simply Lift",
            "places": "7"
        })

    response = client.post("/purchasePlaces", data={
            "competition": "Summer Con",
            "club": "Simply Lift",
            "places": "6"
        })

    assert "Points available: 6" in response.get_data(as_text=True)
    assert "Sorry, a club cannot book more than 12 places in one competition." in response.get_data(as_text=True)


def test_purchase_with_empty_places_field_is_rejected(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Simply Lift",
        "places": ""
    })

    assert "Please enter a number of places greater than zero." in response.get_data(as_text=True)
    assert "Points available: 13" in response.get_data(as_text=True)


def test_purchase_with_negative_places_is_rejected(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Simply Lift",
        "places": "-5"
    })

    assert "Please enter a number of places greater than zero." in response.get_data(as_text=True)
    assert "Points available: 13" in response.get_data(as_text=True)


def test_purchase_with_zero_places_is_rejected(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Winter Challenge",
        "club": "Simply Lift",
        "places": "0"
    })

    assert "Please enter a number of places greater than zero." in response.get_data(as_text=True)
    assert "Points available: 13" in response.get_data(as_text=True)
