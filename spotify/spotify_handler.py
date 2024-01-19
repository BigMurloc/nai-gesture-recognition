import os

import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth


class MissingEnvironmentVariable(Exception):
    pass


def init_spotify():
    client_id = validate_and_return_env_variable('SPOTIFY_CLIENT_ID')
    client_secret = validate_and_return_env_variable('SPOTIFY_SECRET')

    scope = "user-modify-playback-state,user-read-playback-state"

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
        self.last_known_volume_percent = None

    def handle_hand_gesture(self, hand_gesture):
        if self.last_known != hand_gesture:
            print("Sending to spotify! Gesture: " + hand_gesture)

            if hand_gesture == 'Pause':
                self.spotify.pause_playback()
            if hand_gesture == 'Resume':
                self.spotify.start_playback()
            if hand_gesture == 'Mute':
                device_volume_percent = self.spotify.current_playback()['device']['volume_percent']
                if device_volume_percent != 0:
                    self.last_known_volume_percent = self.spotify.current_playback()['device']['volume_percent']
                print("Setting volume to 0, previous known volume: " + str(self.last_known_volume_percent))
                self.spotify.volume(0)
            if hand_gesture == 'Unmute' and self.last_known_volume_percent is not None:
                self.spotify.volume(self.last_known_volume_percent)
            if hand_gesture == 'Next song':
                self.spotify.next_track()
            if hand_gesture == 'Previous song':
                self.spotify.previous_track()

        self.last_known = hand_gesture
