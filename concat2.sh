ffmpeg -i test.mp4 -framerate 29.97 -loop 1 -i ../Downloads/icfp-titlecard.png -filter_complex \
  "[1:v] fade=out:st=3:d=2:alpha=1 [ov]; [0:v][ov] overlay=10:10 [v]" -map "[v]" \
  -map 0:a -c:a copy -c:v libx264 -shortest out.mp4
