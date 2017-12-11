#!/bin/bash

# This script takes a video name and overlays the logo (second arg) at the
# beginning for 3 seconds, 2 of which are fade out.
ffmpeg -i $1 -framerate 29.97 -loop 1 -i $2 \
  -filter_complex "[1:v] fade=out:st=3:d=2:alpha=1 [ov]; [0:v][ov] overlay=10:10 [v]" \
  -map "[v]" -map 0:a -c:a copy -c:v libx264 -shortest titled-$1
