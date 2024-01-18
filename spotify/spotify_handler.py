import os

import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth


class MissingEnvironmentVariable(Exception):
    pass


def init_spotify():
    client_id = validate_and_return_env_variable('SPOTIFY_CLIENT_ID')
    client_secret = validate_and_return_env_variable('SPOTIFY_SECRET')

    scope = "user-modify-playback-state"

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id,
            client_secret,
            redirect_uri="http://localhost/",
            scope=scope
        )
    )


def validate_and_return_env_variable(var_name):
    load_dotenv()
    var_env = os.getenv(var_name)
    if var_env is None or len(var_env) == 0:
        raise MissingEnvironmentVariable('Variable ' + var_name + ' is missing')
    return var_env


class SpotifyHandler:
    def __init__(self):
        self.last_known = ""
        self.spotify = init_spotify()

    def handle_hand_gesture(self, hand_gesture):
        if self.last_known != hand_gesture:
            print("Sending to spotify! Gesture: " + hand_gesture)

            if hand_gesture == 'Pause':
                self.spotify.pause_playback()
            if hand_gesture == 'Resume':
                self.spotify.start_playback()

        self.last_known = hand_gesture
