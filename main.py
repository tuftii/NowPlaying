from requests import get
from time import sleep
from secrets import refresh_token
from refresh import Refresh
from wiki import Wiki
from datetime import date


class NowPlaying:
    def __init__(self):
        self.access_token = None
        self.refresh_token = refresh_token
        self.artist = ""
        self.song = ""
        self.uri = ""

    # Checks the existing track to see if it's changed from what's playing now.
    def check_change(self):
        for line in open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "r", encoding="utf-8"):
            nowplaying = self.get_song()

            if nowplaying.find("-") < 0:
                return False
            else:
                return line != nowplaying

        return True

    # Gets the currently playing song from Spotify and writes it out to a text file.
    def now_playing(self):
        line = self.get_song()

        if line.find("-") == -1:
            # Look for hyphen in track name generated from REST call
            return

        r = open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "r", encoding="utf-8")
        current = r.readline()

        if line == current:
            return
        else:
            r.close()

        # Open the file for writing, truncate (clear) the file, add the Artist - Song found, and close.
        f = open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "a", encoding="utf-8")
        f.truncate(0)
        f.write(line)
        f.close()

        print("Now Playing: " + line)

    # Calls Spotify's REST handler to get the currently playing track, parses out the artists and song.
    def get_song(self):
        # Make call to Spotify to get the currently playing track.
        url = "https://api.spotify.com/v1/me/player/currently-playing"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token
        }

        # Parse the response
        response = get(url=url, headers=headers)

        if response.status_code == 204:
            error0 = "No song playing"
            print(error0)
            return error0

        response_json = response.json()

        if "item" in response_json and response_json['is_playing'] is True:
            # make a comma separated string of the artists
            artists = response_json['item']['artists']
            num_artists = len(artists)
            count = 0
            self.artist = ""

            for artist in artists:
                self.artist += artist['name']
                count += 1
                if 1 < num_artists != count:
                    self.artist += ", "

            self.artist.strip()

            # Get the song title from the response
            self.song = response_json['item']['name']

            # Get the spotify id from the response
            self.uri = response_json['item']['id']

            # Build the line for the text file.
            line = self.artist + " - " + self.song

            return line
        elif "is_playing" in response_json and response_json['is_playing'] is False:
            error0 = "No song playing"
            print(error0)
            return error0
        elif "error" in response_json:
            error1 = "Failed to get song from Spotify"
            print(error1)
            return error1
        else:
            error2 = "Something weird idk."
            print(error2)
            return error2

    def call_refresh(self):
        refreshCaller = Refresh()
        self.access_token = refreshCaller.refresh()


# Main runner.
if __name__ == '__main__':
    f = open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "a", encoding="utf-8")
    f.truncate(0)
    f.close()

    filename = "C:\\Users\\Claire\\CGR\\Wiki" + date.today().strftime("%d-%m-%Y") + ".TXT"
    wiki = Wiki(filename)

    np = NowPlaying()
    np.call_refresh()
    refresh_time = 0

    while True:
        change = np.check_change()
        if change:
            np.now_playing()
            wiki.write_line(np.artist, np.song, np.uri)
        refresh_time += 10
        sleep(10)

        if refresh_time > 3000:
            np.call_refresh()
            refresh_time = 0
