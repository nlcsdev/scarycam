import virtualvideo

import cv2

import numpy as np

import random

import os.path
import os

import atexit


class MyVideoSource(virtualvideo.VideoSource):
    def __init__(self):
        # open the videos and remember their resolution
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
        # prefix used for caching images
        #prefix = ""
        frameIndex = 0
        # start the video playing forward
        forward = True

        # used to cache the frames, frames need to be stored and named a specific way
        # if not (os.path.exists("frames/haunted")):
        #     os.makedirs("frames/haunted")

        # if not (os.path.exists("frames/normal")):
        #     os.makedirs("frames/normal")

        # continue running until manually interrupted
        while True:
            vid = None
            # randomly select a video as source
            if(random.randint(0, 2) > 1):
                vid = self.haunted
                #prefix = "frames/haunted/haunted"
            else:
                vid = self.normal
                #prefix = "frames/normal/normal"

            # select the corresponding frame at this time
            vid.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
            ret, frame = vid.read()

            # use the specific file name to use cached frame
            #fileName = prefix + str(frameIndex) + '.jpg'
            # simply use a current frame
            fileName = 'current.jpg'

            if ret == True:
                # if frame index is 0, play video forward
                if(frameIndex == 0):
                    forward = True
                # if frame index is at the end, play backwards
                elif(frameIndex == self.frames-1):
                    forward = False

                # increment and decrement frame index appropriately
                if(forward):
                    frameIndex += 1
                else:
                    frameIndex -= 1

                # check for cached frame if using such a method, if not cached, create/overwrite frame file
                # if not os.path.isfile(fileName):
                cv2.imwrite(fileName, frame)
                # reopen the frame file as an image
                img = cv2.imread(fileName)
                # crop image
                yield img[100:self.src_y, 0:self.src_x]
            else:
                continue


# shell command to create v4l2 device
os.system("sudo modprobe v4l2loopback video_nr=0")


vidsrc = MyVideoSource()
fvd = virtualvideo.FakeVideoDevice()

# on exit clean up, remove virtual device and remove v4l2loopback module


def clean():
    fvd.stop()
    os.system("sudo rm /dev/video0")
    os.system("sudo modprobe -rf v4l2loopback")


atexit.register(clean)

# set ffmpeg input
fvd.init_input(vidsrc)
# set ffmpeg output info
fvd.init_output(0, vidsrc.img_size()[0], vidsrc.img_size()[1], fps=60)

fvd.run()
