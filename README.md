# Zomboid Playlist Creator

A small Python CLI tool that creates **Spotify playlists from the mixtapes in the Project Zomboid mod [*True Music Mixtape Megapack*](https://steamcommunity.com/sharedfiles/filedetails/?id=3068955583).**

The script reads mixtape data from `tapes.json`, searches Spotify for each track, and automatically builds a playlist in your Spotify account.

---

## Features

* Creates Spotify playlists from Project Zomboid mixtapes
* Searches and validates songs before adding them
* Fuzzy-matches mixtape names if you mistype them
* Simple CLI usage

---

## Requirements

* Python 3.10+
* Spotify Developer account

Install dependencies:

```bash
pip install spotipy python-dotenv
```

---

## Setup

1. Create a Spotify app:
   https://developer.spotify.com/dashboard

2. Add a redirect URI:

```
http://127.0.0.1:8888/callback
```

3. Create a `.env` file:

```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
```

---

## Usage

Run with a mixtape name:

```bash
python zomboid_playlist_creator.py "Geek Rock"
```

or run interactively:

```bash
python zomboid_playlist_creator.py
```

The script will:

1. Load the mixtape data
2. Search Spotify for each track
3. Create a playlist
4. Add all songs automatically

---

## Example

```
[*] Enter the name of the tape: rock darkness
  [!] Did you mean Classic Rock Darkness? (y/n): y
[*] Authenticating with Spotify...
[*] Searching for songs...
  [+] Found (Don't Fear) The Reaper by Blue Öyster Cult
  [+] Found Paint It, Black by The Rolling Stones
  [+] Found House Of The Rising Sun by The Animals
  [+] Found Season of the Witch by Donovan
  [+] Found Somebody to Love by Jefferson Airplane
  [+] Found People Are Strange by The Doors
  [+] Found White Room by Cream
  [+] Found Time of the Season by The Zombies
[*] Creating playlist...
  [+] Playlist Classic Rock Darkness created successfully!
```

---

## Credits

Mixtape data based on the [**True Music Mixtape Megapack**](https://steamcommunity.com/sharedfiles/filedetails/?id=3068955583) mod for
**Project Zomboid**.
