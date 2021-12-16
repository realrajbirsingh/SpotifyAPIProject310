from flask import Flask, request, redirect, Response
from flask_cors import CORS

import json
import base64
import requests
from spotifyclient import SpotifyClient

app = Flask(__name__)
CORS(app)

info = {
    "client": None
}

red = "https://rajbirsingh.pythonanywhere.com/callback"
client_id = "863e4af9e14c4748be4d638fad066a68"
client_secret = "199511ad2e294e64aaec1aa7f9ad22e8"

@app.route("/")
def root():
    return "Base route is working"


@app.route("/get_recs", methods=["GET"])
def get_recently_played():
    limit = request.args["limit"]

    tracks = info["client"].get_last_played_tracks(limit)
    recommendations = info["client"].get_track_recommendations(tracks)
    resp = json.dumps(recommendations)

    toReturn = Response(resp, mimetype='application/json')
    toReturn.headers['Access-Control-Allow-Origin'] = '*'

    return toReturn

@app.route("/callback", methods=["GET"])
def callback():
    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    BASE_URL = 'https://api.spotify.com/v1/'

    # Make a request to the /authorize endpoint to get an authorization code
    our_code = request.args["code"]

    auth_code = requests.get(AUTH_URL, {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': red,
        'scope': 'playlist-modify-private',
    })

    auth_header = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode('ascii'))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + auth_header.decode('ascii')
    }

    payload = {
        'grant_type': 'authorization_code',
        'code': our_code,
        'redirect_uri': red,
    }

    # Make a request to the /token endpoint to get an access token
    access_token_request = requests.post(url=TOKEN_URL, data=payload, headers=headers)

    # convert the response to JSON
    access_token_response_data = access_token_request.json()
    # save the access token
    access_token = access_token_response_data['access_token']

    # build request to get the user id

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    user_profile_request = requests.get(BASE_URL + "me", headers=headers)
    json1 = user_profile_request.json()
    user_id = json1["id"]

    # Instantiate spotify client so it is no longer none
    info["client"] = SpotifyClient(access_token, user_id)

    return redirect("https://realrajbirsingh.github.io/SpotifyAPIProject310/index.html")

if __name__== "__main__":
    app.run()