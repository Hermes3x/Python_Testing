import pytest
import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_data():
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()

def purchasePlaces(competition, club):

    foundCompetition = find_by(competitions, "name", competition)
    foundClub = find_by(clubs, "name", club)

    placesRequired = int(request.form['places'])

    if competition and club:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points']) - placesRequired

        if club['points'] > -1:
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competition)

        else:
            flash("Sorry, you are traying to purchase more places than your available points")
            return render_template('welcome.html', club=club, competitions=competition)

    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competition)

