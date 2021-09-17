# Scary Cam
Scary Cam is a project forked from [VirtualVideo](https://github.com/Flashs/virtualvideo). Using two videos with the same total frames, a haunted video feed can be presented to a v4l2 virtual device.

Please visit the original github for additional help.

## Prerequisites 
* [v4l2loopback](https://github.com/umlaeute/v4l2loopback)
* [ffmpeg-python](https://github.com/kkroening/ffmpeg-python/) 
* [opencv-python](https://github.com/opencv/opencv-python)

## Running program
This program would only work on an OS that uses v4l2 devices, such as a Linux OS.

To run the program, simply double click the start.sh shell script or run in the termianal. You may be prompted to enter your password.

Before exiting the program, it is recommended that you disconnect your video feed in any software you may be using first. After that, simply hit ctrl-c to terminate the program.

## Customization
This github supplies two generated videos, but you may replace them with your own videos. The only requirement is that both videos must have the same total amount of frames.

To crop your own videos accordingly, please adjust line `75` in `cam.py`, where the pixels (0,0) is located at the top left corner of your video. The parameters are `img[starting_y_pixel:ending_y_pixel, starting_x_pixel:ending_x_pixel]`. 
```
yield img[100:self.src_y, 0:self.src_x]
```

There are also code commented out that can store each frame of your videos to increase performance but sacrifices storage space. Feel free to adjust the code accordingly to use this approach.

## Credits
This Module relies heavily on [v4l2loopback](https://github.com/umlaeute/v4l2loopback) 
and [ffmpeg-python](https://github.com/kkroening/ffmpeg-python/).
