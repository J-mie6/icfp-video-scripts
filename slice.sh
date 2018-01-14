#!/bin/bash

# This script is to cut a clip out of a video, useful if the recording is of a
# full session and you want the individual talks

# This script takes 4 arguments:
# 1: The name of the input video
# 2: The name of the output video
# 3: The start time of the clip in arg-1 (in HH:MM:SS)
# 3: The end time of the clip in arg-1 (in HH:MM:SS)

ffmpeg -i $1 -vcodec copy -acodec copy -ss $3 -t $4 $2

# Example usage: make a video of the first 20 minute talk in a video file:
#
# > slice.sh MVI_0199.MP4 talk1.MP4 00:00:00 00:20:00
