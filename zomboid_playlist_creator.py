# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "python-dotenv==1.2.2",
#     "spotipy==2.26.0",
# ]
# ///
import json
from dotenv import load_dotenv
from os import getenv
import difflib
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys


class ZomboidPlaylistCreator:
    def __init__(self, tape_name: str) -> None:
        self.tape_name: str = tape_name

        self.tapes: dict[str, dict] = {}
        self.load_tapes()
        self.get_closest_match()

        self.authenticate()

        self.uri_bin: list[str] = []
        self.genre = ""
        self.search_songs()

        self.create_playlist()

    def load_tapes(self) -> None:
        with open("tapes.json") as f:
            self.tapes = json.load(f)

    def get_closest_match(self) -> None:
        print("[*] Searching for matching tape...")
        for key in self.tapes.keys():
            if self.tape_name.lower() in key.lower():
                self.tape_name = key
                print(f"  [+] Found tape {self.tape_name}")
                return

        closest = difflib.get_close_matches(
            self.tape_name, self.tapes.keys(), n=1, cutoff=0.6
        )
        if closest:
            if input(f"  [!] Did you mean {closest[0]}? (y/n): ").lower() == "y":
                self.tape_name = closest[0]
                return
            else:
                print("[-] Exiting...")
                sys.exit(1)

        raise ValueError(f"No tape found with name {self.tape_name}")

    def authenticate(self) -> None:
        print("[*] Authenticating with Spotify...")
        load_dotenv()
        CLIENT_ID = getenv("CLIENT_ID")
        CLIENT_SECRET = getenv("CLIENT_SECRET")

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri="http://127.0.0.1:8888/callback",
                scope="playlist-modify-public playlist-modify-private",
                cache_path=".spotify_cache",
            )
        )

    def search_songs(self) -> None:
        print("[*] Searching for songs...")
        # search for songs
        uri_bin = []

        tape = self.tapes[self.tape_name]
        self.genre = tape["genre"]
        for track, artist in tape["songs"].items():
            results = self.sp.search(
                q=f"artist:{artist} track:{track}", type="track", limit=1
            )
            result_track = results["tracks"]["items"][0]["name"].lower()
            result_artist = results["tracks"]["items"][0]["artists"][0]["name"].lower()
            if track.lower() not in result_track or artist.lower() not in result_artist:
                raise ValueError(
                    f"Expected {track} by {artist}, but got {result_track} by {result_artist}"
                )
            uri_bin.append(results["tracks"]["items"][0]["uri"])
            print(f"  [+] {track} - {artist}")

        self.uri_bin = uri_bin

    def create_playlist(self) -> None:
        # create playlist
        print("[*] Creating playlist...")
        playlist = self.sp.current_user_playlist_create(
            name=self.tape_name, public=True, description=self.genre
        )
        playlist_id = playlist["id"]

        # add tracks
        self.sp.playlist_add_items(playlist_id=playlist_id, items=self.uri_bin)

        print(f"  [+] Playlist {self.tape_name} created successfully!")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        tape_name = sys.argv[1]
    else:
        tape_name = input("[*] Enter the name of the tape: ")
    creator = ZomboidPlaylistCreator(tape_name)
