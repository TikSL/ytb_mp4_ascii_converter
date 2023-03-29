import argparse
from pytube import YouTube
import pytube.request
import sys

# Modification pour barre de chargement
pytube.request.default_range_size = 9437184


def on_progress(stream, file_handle, bytes_remaining):
    taille_totale = stream.filesize
    taille_dl = taille_totale - bytes_remaining
    taux_dl = round(taille_dl / taille_totale * 100, 1)
    sys.stdout.write(f'\rTéléchargement du fichier : '
                     f'/' + '█' * int(taux_dl) + '*' * (100 - int(taux_dl)) + '/   ' + str(taux_dl) + '%\n')
    sys.stdout.flush()


def download():

    # create parser
    description = "Permet de download une vidéo ytb."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-o', '--out',        dest='nom_fichier', required=False, default='video_to_ascii')
    parser.add_argument('-l', '--lien',       dest='lien',        required=False, default='https://www.youtube.com/watch?v=uwmeH6Rnj2E')
    parser.add_argument('-q', '--quality',    dest='qualite',     required=False, default='low')
    args = parser.parse_args()

    nom_fichier = args.nom_fichier + ".mp4"
    lien = args.lien
    qualite = args.qualite

    yt = YouTube(lien)
    yt.register_on_progress_callback(on_progress)

    if qualite == 'high':
        resolution = yt.streams.get_highest_resolution()
    else :
        resolution = yt.streams.get_lowest_resolution()

    print("Lien : OK -> ", lien)

    print(f'Titre : {yt.title}\n'
          f'Durée : {yt.length} s\n'
          f'Taille du fichier : {round(resolution.filesize / 10000, 2)} Ko')

    resolution.download(filename=nom_fichier)
    
    print("Download : OK -> ", nom_fichier)


if __name__ == '__main__':
    download()
