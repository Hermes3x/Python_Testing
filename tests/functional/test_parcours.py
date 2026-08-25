def test_secretary_books_places_and_sees_points_updated(client):
    # 1. je me connecte et je vois mon solde
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert "Points available: 13" in response.get_data(as_text=True)

    # 2. j'ouvre la page de réservation d'une compétition à venir
    response = client.get("/book/Summer%20Con/Simply%20Lift")
    assert "Summer Con" in response.get_data(as_text=True)

    # 3. je réserve 3 places
    response = client.post("/purchasePlaces", data={
        "competition": "Summer Con",
        "club": "Simply Lift",
        "places": "3"
    })

    # 4. je vois la confirmation ET mon solde à jour
    assert "Great! Your booking is complete." in response.get_data(as_text=True)
    assert "Points available: 10" in response.get_data(as_text=True)


def test_secretary_books_too_much_places_and_sees_error_message(client):
    # 1. je me connecte et je vois mon solde
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert "Points available: 4" in response.get_data(as_text=True)

    # 2. j'ouvre la page de réservation d'une compétition à venir
    response = client.get("/book/Summer%20Con/Iron%20Temple")
    assert "Summer Con" in response.get_data(as_text=True)

    # 3. je réserve 3 places
    response = client.post("/purchasePlaces", data={
        "competition": "Summer Con",
        "club": "Iron Temple",
        "places": "5"
    })

    # 4. je vois le message d'erreur ET mon solde n'est pas débité
    assert "Sorry, you do not have enough points for that many places." in response.get_data(as_text=True)
    assert "Points available: 4" in response.get_data(as_text=True)


def test_points_board_reflects_a_purchase(client):
    # 1. un secrétaire réserve 3 places
    client.post("/purchasePlaces", data={
        "competition": "Summer Con",
        "club": "Simply Lift",
        "places": "3"
    })

    # 2. un visiteur non connecté consulte le tableau public
    response = client.get("/pointsBoard")

    # 3. il voit le solde À JOUR, pas l'ancien
    assert "Number of Points: 10" in response.get_data(as_text=True)
