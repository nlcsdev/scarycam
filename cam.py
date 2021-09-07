import virtualvideo

import cv2

import numpy as np

import random

import os.path
import os

import atexit


class MyVideoSource(virtualvideo.VideoSource):
    def __init__(self):
        self.normal = cv2.VideoCapture("normal.mp4")
        self.haunted = cv2.VideoCapture("haunted.mp4")
        if not self.normal.isOpened() or not self.haunted.isOpened():
            print("Unable to read video.")

        self.frames = self.normal.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Total Frames:%d" % (self.frames))
        self.src_x = int(self.normal.get(3))
        self.src_y = int(self.normal.get(4))
        # opencv's shape is y,x,channels
        self._size = (self.src_x, self.src_y-100)

    def img_size(self):
        return self._size

    def fps(self):
        return 10

    def generator(self):
        #prefix = ""
        frameIndex = 0
        forward = True

        # if not (os.path.exists("frames/haunted")):
        #     os.makedirs("frames/haunted")

        # if not (os.path.exists("frames/normal")):
        #     os.makedirs("frames/normal")

        while True:
            vid = None
            if(random.randint(0, 2) > 1):
                vid = self.haunted
                #prefix = "frames/haunted/haunted"
            else:
                vid = self.normal
                #prefix = "frames/normal/normal"

            vid.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
            ret, frame = vid.read()

            #fileName = prefix + str(frameIndex) + '.jpg'
            fileName = 'current.jpg'

            if ret == True:
                if(frameIndex == 0):
                    forward = True
                elif(frameIndex == self.frames-1):
                    forward = False

                if(forward):
                    frameIndex += 1
                else:
                    frameIndex -= 1

                # if not os.path.isfile(fileName):
                cv2.imwrite(fileName, frame)
                img = cv2.imread(fileName)
                yield img[100:self.src_y, 0:self.src_x]
            else:
                continue


os.system("sudo modprobe v4l2loopback video_nr=0")


vidsrc = MyVideoSource()
fvd = virtualvideo.FakeVideoDevice()


def clean():
    fvd.stop()
    os.system("sudo rm /dev/video0")
    os.system("sudo modprobe -rf v4l2loopback")


atexit.register(clean)

fvd.init_input(vidsrc)
fvd.init_output(0, vidsrc.img_size()[0], vidsrc.img_size()[1], fps=60)

fvd.run()
