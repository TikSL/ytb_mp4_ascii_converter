import time
import argparse
import sys
import cv2

# 10 niveaux de gris
niv_gris = '@%#*+=-:. '


def coverImageToAscii(image, W, H, cols, rows, scale):

    w = W / cols
    h = w / scale

    aimg = ""
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        if j == rows - 1:
            y2 = H

        for i in range(cols):

            x1 = int(i * w)
            x2 = int((i + 1) * w)

            if i == cols - 1:
                x2 = W

            gris_image = []
            for x in range(x1,x2-1):
                for y in range(y1,y2-1):
                    gris_image.append(image[y, x])

            avg = sum(gris_image) / len(gris_image)
            gsval = niv_gris[int((avg * 9) / 255)]
            aimg += gsval

    return aimg


# main() function
def main():
    description = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-c', '--cols', dest='cols', required=False, default=100)
    parser.add_argument('-t', '--nbr_te', dest='coef_tempo', required=False, default=2)
    parser.add_argument('-i', '--nbr_im', dest='coef_image', required=False, default=2)

    # parse args
    args = parser.parse_args()

    # Constantes utiles
    scale = 0.43
    cols = int(args.cols)
    coef_image = int(args.coef_image)
    coef_tempo = int(args.coef_tempo)

    fichier_source = "video_to_ascii.mp4"
    fichier_sortie = "out_ascii.txt"
    fichier_info = "info.txt"

    # Acquisition vidéo
    video = cv2.VideoCapture(fichier_source)

    # Caractéristiques de la vidéo
    nombre_image = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    cols_video = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    rows_video = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # compute width of tile
    w = cols_video / cols
    # compute tile height based on aspect ratio and scale
    h = w / scale
    # compute number of rows
    rows = int(rows_video / h)

    # Vérification format image
    if cols > cols_video or rows > rows_video:
        print("L'image est trop petite pour un tel nombre de colonnes !")
        return

    # Génération du fichier info
    finfos = open("info.txt", 'w')
    finfos.write(f"Nombre images =          {nombre_image}\n"
                 f"FPS =                    {fps}\n"
                 f"Coef image =             {coef_image}\n"
                 f"Nombre colonnes video =  {cols_video}\n"
                 f"Nombre lignes video =    {rows_video}\n"
                 f"Nombre colonnes ASCII =  {cols}\n"
                 f"Nombre lignes ASCII =    {rows}")
    finfos.close()

    currentframe = 0
    aimg_tot = ""

    # Définition des variables de temps
    t1 = time.time()
    temps_restant = "???"

    while True:
        ret, frame = video.read()
        if ret:
            if currentframe % coef_image == 0:

                gray_image = 255 - cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                aimg = coverImageToAscii(gray_image, int(cols_video), int(rows_video), cols, rows, scale)
                aimg_tot += aimg + '\n'

                # Calcul temps restant
                if currentframe % coef_tempo == 0 and currentframe > 0:
                    temps_fait = time.time() - t1
                    temps_restant = (nombre_image - currentframe) / coef_tempo * temps_fait
                    temps_restant = int(temps_restant)
                    t1 = time.time()

                # Message évolution génération
                sys.stdout.write(
                    f"\rGénération fichier {fichier_sortie} : {round(currentframe / nombre_image * 100, 1)}% "
                    f"- {currentframe}/{nombre_image} "
                    f"- fin estimée dans {temps_restant} s.")
                sys.stdout.flush()

            currentframe += 1

        else:
            break

    # Ecriture du fichier out_ascii.txt
    fsortie = open(fichier_sortie, 'w')
    fsortie.write(aimg_tot)
    fsortie.close()

#     # Libération vidéo
    video.release()
    cv2.destroyAllWindows()

    # Pause pour préview
    input("\nAppuyer sur une touche pour lancer la video ASCII")

    haut = "#" * cols + "\n"
    milieu = "#" + " " * (cols - 2) + "#" + "\n"
    preview = haut + milieu * (rows - 2) + haut

    sys.stdout.write(preview)

    # Pause pour valider preview
    input("\nAppuyer sur une touche pour lancer la video ASCII")

    f = open(fichier_sortie, 'r')

    for k in range(0, nombre_image):
        lignes = f.readline()
        bloc = ""
        for x in range(0, rows * cols, cols):
            bloc += lignes[x:x + cols] + "\n"
        sys.stdout.write(bloc)
        time.sleep(1 / fps * coef_image)

    f.close()


if __name__ == '__main__':
    main()
