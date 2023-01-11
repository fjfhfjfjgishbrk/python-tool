import cv2

FPS = 24
FRAMERATE = 1 / FPS
HEIGHT = 1644
WIDTH = 1538

vidcap = cv2.VideoCapture('result.mov')
out = cv2.VideoWriter("out.mp4", cv2.VideoWriter_fourcc(*'DIVX'), FPS, (HEIGHT, WIDTH))


def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, round(sec*1000))
    hasFrames, image = vidcap.read()
    if hasFrames:
        out.write(image)
    return hasFrames


sec = 0
count = 1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + FRAMERATE
    if count % 6 == 1:
        success = getFrame(sec)
    if count % 240 == 0:
        print("converted", round(sec), "seconds")
out.release()