from requests import get
from time import sleep


# Checks the existing track to see if it's changed from what's playing now.
def check_change():
    for line in open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "r"):
        nowplaying = get_song()
        return line != nowplaying

    return True


# Gets the currently playing song from Spotify and writes it out to a text file.
def now_playing():
    line = get_song()

    if line.find("-") == -1:
        return

    # Open the file for writing, truncate (clear) the file, add the Artist - Song found, and close.
    f = open("C:\\Users\\Claire\\CGR\\NowPlaying.TXT", "a")
    f.truncate(0)
    f.write(line)
    f.close()

    print("Now Playing: " + line)


# Calls Spotify's REST handler to get the currently playing track, parses out the artists and song.
def get_song():
    # Make call to Spotify to get the currently playing track.
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer <your token>"
    }

    # Parse the response
    response = get(url=url, headers=headers).json()

    # make a comma separated string of the artists
    if "item" in response:
        artists = response['item']['artists']
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
        song = response['item']['name']

        # Build the line for the text file.
        line = artists_string + " - " + song

        return line
    elif "error" in response:
        error1 = "Failed to get song from Spotify"
        print(error1)
        return error1
    else:
        error2 = "Something weird idk."
        print(error2)
        return error2


# Main runner.
if __name__ == '__main__':
    while True:
        change = check_change()
        if change:
            now_playing()
        sleep(5)
