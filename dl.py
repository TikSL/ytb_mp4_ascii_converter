from pytube import YouTube
import os

lien = "https://www.youtube.com/watch?v=4MdHz5birFo"
nomFichier = "video_test.mp4"
yt = YouTube(lien)
print("Lien : OK -> ", lien)
titre = yt.title
print("Titre : OK -> ", titre)
print("Début du téléchargement ...")
yt.streams.get_lowest_resolution().download(filename=nomFichier)
print("Download : OK -> ", nomFichier)

