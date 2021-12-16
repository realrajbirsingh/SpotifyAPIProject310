from flask import Flask
from flask import request, redirect

import os
import json
from spotifyclient import SpotifyClient

app = Flask(__name__)

#spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"),
#                                   os.getenv("SPOTIFY_USER_ID"))



spotify_client = SpotifyClient("BQBGmEPOb9-a1xnsRzf6llkp-adE_6p41Dvw8TCkl1nlnoyFsXjdseBKaTrl_dt0NfqaKIXxceQjg08uteTWhvPwEj_iLztbMCtRNn5l_por7jsQmotwIILnNUtWSNbERIFzWOWUOc50wY-BYBMcuXvIn3AJpOe3NY-zw4jS3aIoJdtFqCEv5qGxXR3hIorRVCz0gRReWS-lft5y58Pr7KepND1LSWkY8TmxPeuH",
                                   "12143085512")

@app.route("/")
def root():
    return "Poggers"


@app.route("/get_recs", methods=["GET"])
def get_recently_played():
    limit = request.args["limit"]

    tracks = spotify_client.get_last_played_tracks(limit)
    recommendations = spotify_client.get_track_recommendations(tracks)
    resp = json.dumps(recommendations)

    return resp

@app.route("/callback", methods=["GET"])
def callback():

    # Do some shit to get the auth tokens and all that

    return redirect("file:///Users/rajbirsingh/SpotifyAPIProject310/frontend/index.html")


if __name__== "__main__":
    app.run()