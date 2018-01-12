#!/bin/bash

# This file normalizes the audio in a video. While this is useful in
# many cases (workshops with no mic, etc) it does result in a not-great
# sound. So only use if necessary

# This takes two arguments:
#
# 1: The name of the input file
# 2: The name of the output file
/usr/bin/ffmpeg -i $1 -filter:a loudnorm $2
