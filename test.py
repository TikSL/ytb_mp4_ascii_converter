import sys
import time
import os


fichiers = ["out" + str(k*5) + ".txt" for k in range(0, 867)]

for fichier in fichiers:
    f = open(fichier, 'r')
    # sys.stdout.write("\n"*10)
    # \n pas nécessaire
    sys.stdout.write(f.read())
    f.close()
    time.sleep(0.17)
    os.system('clear')
