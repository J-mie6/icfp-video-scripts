#!/usr/bin/bash

# This script concatenates two video files that use the same encoding (avoiding
# any re-encoding)
# Script takes four arguments
#
# 1: The name of the first video file (beginning of new video)
# 2: The name of the second video file (end of new video)
# 3: A name for temporary files. If you pass 'temp'
#    the temporary files will be called 'temp-1.ts' and 'temp-2.ts'
# 4: The name of the output file

# Make a stream out of the first file
/usr/bin/ffmpeg -i $1 -c copy -bsf:v h264_mp4toannexb -f mpegts $3-1.ts

# Make a stream out of the second file
/usr/bin/ffmpeg -i $2 -c copy -bsf:v h264_mp4toannexb -f mpegts $3-2.ts

# Combine the first and second streams
/usr/bin/ffmpeg -f mpegts -i "concat:temp-1.ts|temp-2.ts" -c copy -bsf:a aac_adtstoasc $4

# Clean up the temporary files
rm $3-1.ts $3-2.ts
