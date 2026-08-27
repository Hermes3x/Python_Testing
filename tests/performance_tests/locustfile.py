from locust import HttpUser, task, between


class GudlftUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def consulter_ses_competitions(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def consulter_le_tableau_des_points(self):
        self.client.get("/pointsBoard")

    @task
    def ouvrir_une_page_de_reservation(self):
        self.client.get("/book/Summer%20Con/Simply%20Lift")

    @task
    def reserver_des_places(self):
        self.client.post("/purchasePlaces", data={
            "competition": "Summer Con",
            "club": "Simply Lift",
            "places": "1"
        })
