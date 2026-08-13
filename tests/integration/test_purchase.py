def test_purchase_deducts_points_from_club(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "3"
    })

    assert "Points available: 10" in response.get_data(as_text=True)
