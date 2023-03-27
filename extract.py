import cv2

nom_fichier = "video_test.mp4"
video = cv2.VideoCapture(nom_fichier)

currentframe = 0
while True:
	ret, frame = video.read()

	if ret:
		if currentframe % 100 == 0:
			name = str(currentframe) + '.jpg'
			print('Captured...' + name)
			cv2.imwrite(name, frame)
		currentframe += 1
	else:
		break
video.release()
cv2.destroyAllWindows()