import argparse
import sys
import cv2

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

        aimg += '\n'
    return aimg


# main() function
def main():
    description = "This program converts the webcam video into ASCII art."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-c', '--cols', dest='cols', required=False, default=100)

    args = parser.parse_args()

    # Constantes utiles
    scale = 0.43
    cols = int(args.cols)

    # Acquisition vidéo
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Caractéristiques de la vidéo
    nombre_image = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    cols_video = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    rows_video = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    w = cols_video / cols
    h = w / scale
    rows = int(rows_video / h)

    # Vérification format image
    if cols > cols_video or rows > rows_video:
        print("L'image est trop petite pour un tel nombre de colonnes !")
        return

    while True:
        ret, frame = cam.read()
        if ret:
            gray_image = cv2.flip(255 - cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1)
            bloc = coverImageToAscii(gray_image, int(cols_video), int(rows_video), cols, rows, scale)
            sys.stdout.write(bloc)
        else:
            break

#     # Libération vidéo
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
