import argparse
from pytube import YouTube
import sys
from pytube.cli import on_progress


def progress_function(chunk, file_handle, bytes_remaining):
    global filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()


def download():

    # create parser
    description = "Permet de download une vidéo ytb."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--out', dest='nomFichier', required=False)
    parser.add_argument('--lien', dest='lien', required=False)
    args = parser.parse_args()

    nomFichier = "video_test.mp4"
    if args.nomFichier:
        nomFichier = args.nomFichier + ".mp4"

    lien = "https://www.youtube.com/watch?v=4MdHz5birFo"
    if args.lien:
        lien = args.lien

    yt = YouTube(lien)
    yt.register_on_progress_callback(on_progress)
    print("Lien : OK -> ", lien)

    titre = yt.title
    print("Titre : OK -> ", titre)
    yt.streams.get_lowest_resolution().download(filename=nomFichier)
    
    print("Download : OK -> ", nomFichier)

    return yt.length


if __name__ == '__main__':
    # input("Please press the Enter key to proceed")
    download()
