import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


def find_by(items, key, value):
    matching_items = [item for item in items if item[key] == value]
    if not matching_items:
        return None

    return matching_items[0]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():

    email = request.form['email']
    club = find_by(clubs, "email", email)

    if club is None:
        flash("Sorry, that email wasn't found.")
        return render_template('index.html')

    else:
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):

    foundClub = find_by(clubs, "name", club)
    foundCompetition = find_by(competitions, "name", competition)

    if foundClub and foundCompetition:
        competition_date = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() < competition_date:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else: 
            flash("Sorry, this competition has already taken place.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
    else:
        flash("Sorry, we could not find that club or competition.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)


def has_enough_points(club, places_required):
    return places_required <= int(club['points'])


def has_enough_places(competition, places_required):
    return places_required <= int(competition['numberOfPlaces'])


def is_within_twelve_limit(competition, club, places_required):
    return competition['bookings'].get(club['name'], 0) + places_required <= 12


def is_valid_places_input(places_input):
    return places_input.isdigit() and int(places_input) >= 1


def register_purchase(competition, club, placesRequired):
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points']) - placesRequired
    booked = competition['bookings'].get(club['name'], 0)
    competition['bookings'][club['name']] = booked + placesRequired


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    competition = find_by(competitions, "name", request.form['competition'])
    club = find_by(clubs, "name", request.form['club'])

    if not competition or not club:
        flash("Sorry, we could not find that club or competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    places_input = request.form['places']

    if not is_valid_places_input(places_input):
        flash("Please enter a number of places greater than zero.")
        return render_template('welcome.html', club=club, competitions=competitions)

    placesRequired = int(places_input)

    if not has_enough_points(club, placesRequired):
        flash("Sorry, you do not have enough points for that many places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if not has_enough_places(competition, placesRequired):
        flash("Sorry, there are not enough places left in this competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if not is_within_twelve_limit(competition, club, placesRequired):
        flash("Sorry, a club cannot book more than 12 places in one competition.")
        return render_template('welcome.html', club=club, competitions=competitions)

    register_purchase(competition, club, placesRequired)
    flash("Great! Your booking is complete.")
    return render_template('welcome.html', club=club, competitions=competitions)


#@app.route('/pointsBoard', methods=['GET'])


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
