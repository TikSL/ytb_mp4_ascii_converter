# Python code to convert an image to ASCII image.
import sys, random, argparse
import numpy as np
import math

from PIL import Image
import cv2

import time
import os
import shutil
import sys

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '


def getAverageL(image):
    # renvoie valeur moyenne du niveau de gris
    tab_image = np.array(image)
    largeur, hauteur = tab_image.shape
    return np.average(tab_image.reshape(largeur * hauteur))


def covertImageToAscii(fileName, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')

    # store dimensions
    W, H = image.size[0], image.size[1]
    # print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    # print("cols: %d, rows: %d" % (cols, rows))
    # print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            if moreLevels:
                gsval = gscale1[int((avg * 69) / 255)]
            else:
                gsval = gscale2[int((avg * 9) / 255)]

            # append ascii char to string
            aimg[j] += gsval

    # return txt image
    return aimg


# main() function
def main():
    #create parser
    # descStr = "This program converts an image into ASCII art."
    # parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    # parser.add_argument('--scale', dest='scale', required=False)
    # parser.add_argument('--cols', dest='cols', required=False)
    # parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    # parse args
    # args = parser.parse_args()

    # set output file
    outFile = 'out0.txt'

    # set scale default as 0.43 which suits
    # a Courier font
    scale = 0.43
    # if args.scale:
    #     scale = float(args.scale)

    # set cols
    cols = 10
    # if args.cols:
    #     cols = int(args.cols)

    nom_fichier = "video_to_ascii.mp4"

    folder_frames = os.path.join(os.getcwd(), "output")
    if "output" not in os.listdir():
        os.makedirs(folder_frames)
    else:
        shutil.rmtree(folder_frames)
        os.makedirs(folder_frames)

    video = cv2.VideoCapture(nom_fichier)

    fichiers = []

    currentframe = 0

    while True:
        ret, frame = video.read()

        if ret:

            if currentframe % 5 == 0:
                name = os.path.join(folder_frames, str(currentframe) + '.jpg')

                cv2.imwrite(name, frame)
                # print("Génération image ...", name)
                # convert image to ascii txt
                aimg = covertImageToAscii(name, cols, scale, "")
                # open file
                # print("Génération fichier ...", outFile)
                file = os.path.join(folder_frames, outFile)
                f = open(file, 'w')

                # write to file
                for row in aimg:
                    f.write(row + '\n')
                    # bloc += row + "\n"
                # sys.stdout.write(bloc)
                # cleanup
                f.close()
                fichiers.append(file)

                os.remove(name)

                if currentframe % 100 == 0:
                    print("Génération fichier OK", outFile)




            currentframe += 1
            outFile = str(currentframe) +".txt"

        else:
            break
    video.release()
    cv2.destroyAllWindows()

    input("Please press the Enter key to proceed")

    for fichier in fichiers:
        print(fichier)
        # f = open(fichier, 'r')
        # sys.stdout.write(f.read())
        # time.sleep(0.2)
        # f.close()


if __name__ == '__main__':

    main()
