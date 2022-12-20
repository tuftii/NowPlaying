from requests import get
from time import sleep
from secrets import refresh_token
from refresh import Refresh


class NowPlaying:
    def __init__(self):
        self.access_token = None
        self.refresh_token = refresh_token

    # Checks the existing track to see if it's changed from what's playing now.
    def check_change(self):
        for line in open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "r"):
            nowplaying = self.get_song()
            return line != nowplaying

        return True

    # Gets the currently playing song from Spotify and writes it out to a text file.
    def now_playing(self):
        line = self.get_song()

        # Look for hyphen in track name generated from REST call
        if line.find("-") == -1:
            return

        r = open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "r")
        current = r.readline()

        if line == current:
            return
        else:
            r.close()

        # Open the file for writing, truncate (clear) the file, add the Artist - Song found, and close.
        f = open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "a")
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

        # make a comma separated string of the artists
        if "item" in response_json:
            artists = response_json['item']['artists']
            artists_string = ""
            num_artists = len(artists)
            count = 0

            for artist in artists:
                artists_string += artist['name']
                count += 1
                if 1 < num_artists != count:
                    artists_string += ", "

            artists_string.strip()

            # Get the song title from the response
            song = response_json['item']['name']

            # Build the line for the text file.
            line = artists_string + " - " + song

            return line
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
    np = NowPlaying()
    np.call_refresh()
    refresh_time = 0

    while True:
        change = np.check_change()
        if change:
            np.now_playing()
        refresh_time += 10
        sleep(10)

        if refresh_time > 3000:
            np.call_refresh()
            refresh_time = 0
