class Wiki:
    def __init__(self, filename):
        self.filename = filename

    def write_line(self, artist, song, spotify_uri):

        line = "*" + artist + " - " + song + " {{SpotifyTextLink |# = track/" + spotify_uri + "}}\n"

        f = open(self.filename, mode="a", encoding="utf-8")
        f.write(line)
        f.close()
