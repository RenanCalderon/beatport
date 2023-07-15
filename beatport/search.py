# Module for scraping Music
import bs4
from Levenshtein import distance
import requests
import mutagen
import re


class BeatportSearch:

    def __init__(self, url_bp="https://www.beatport.com{}"):
        """Music Link for Beatport"""
        self.url_bp = url_bp

    # Function that allows you to search the metadata of a song; You can specify the song or search it

    def getSongMetadata(self, file="", save=False):

        if file == "":

            artist = input("Input the name of the artist: ")
            name = input("Input the name of the song: ")
            remix = input("Input the name of the artist remix: ")

            if remix != "":
                song = f"{artist} - {name} ({remix} Remix)"
                search_url = f"{artist}+{name}+{remix}".replace(" ", "+")
            else:
                song = f"{artist} - {name}"
                search_url = f"{artist}+{name}".replace(" ", "+")

        else:
            audio = mutagen.File(file)
            song = audio.filename.split("\\")[-1].replace(".mp3", "")
            search_url = re.sub(r"[^\w\s]", '', song)

        page = self.url_bp.format(f"/search?q={search_url}")
        similitud = len(song)

        resultado = requests.get(page)

        if resultado.status_code == 200:

            if save:

                with open(f"{artist}_{name}.html", 'wb') as f:
                    f.write(resultado.text.encode("utf-8"))
            else:
                pass

        else:

            raise print(f"Error: {resultado.status_code}")

        soup = bs4.BeautifulSoup(resultado.content, "lxml")

        # search tracks
        tracks = soup.select(".bucket-item.ec-item.track")
        href_s = ""
        for track in tracks:
            name = track["data-ec-name"]
            artist = track["data-ec-d1"]
            add = track.find("span", class_="buk-track-remixed").string
            song_b = f"{artist} - {name} ({add})"
            dist = distance(song, song_b)
            if dist < similitud:
                similitud = dist
                info_list = [name, artist, add]
                href_s = track.select_one("p.buk-track-title a")["href"]

        if href_s != "":

            url_song = self.url_bp.format(href_s)
            resultado = requests.get(url_song)

            if resultado.status_code != 200:

                raise print(f"Error: {resultado.status_code}")

            else:

                if save:

                    with open(f"{artist}_{name}_data.html", 'wb') as f:
                        f.write(resultado.text.encode("utf-8"))
                else:
                    pass

            soup = bs4.BeautifulSoup(resultado.content, "lxml")

            info = soup.select(".interior-track-content-item")

            for item in info:

                info_list.append(item.select("span", class_="value"
                                             )[1].text.replace("\n", ""))

            return info_list
        else:
            return f"{song} Not Found"

    def get_beatport_playlist(self, playlist_num):

        url = self.url_bp.format(f"/library/playlists/{playlist_num}")
        print(url)
        response = requests.get(url)

        soup = bs4.BeautifulSoup(response.content, "lxml")

        return soup
