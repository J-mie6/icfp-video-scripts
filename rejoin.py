#Note the Scala one is in npfl

import os, sys, subprocess

ffmpeg = r"F:\Downloads\ffmpeg-20181007-0a41a8b-win64-static\ffmpeg-20181007-0a41a8b-win64-static\bin\ffmpeg.exe"

def concat(s, e, to):
    cmd1 = ffmpeg + " -hwaccel nvdec -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts tmp-1.ts"
    cmd2 = ffmpeg + " -hwaccel nvdec -i %s -c copy -bsf:v h264_mp4toannexb -f mpegts tmp-2.ts"
    cmd3 = ffmpeg + " -hwaccel nvdec -f mpegts -i \"concat:tmp-1.ts|tmp-2.ts\" -c copy -bsf:a aac_adtstoasc %s"
    cmd4 = "del tmp-1.ts tmp-2.ts"
    os.system(cmd1 % s)
    os.system(cmd2 % e)
    os.system(cmd3 % to)
    os.system(cmd4)

if __name__ == "__main__":
    files = [f for f in os.listdir("ICFP18Norm\\titled") if f.endswith("mp4")]
    for f in files:
        print(f)
        concat("ICFP18Norm\\titled\\" + f, "ICFP18Norm\\tails\\" + f, "ICFP18Norm\\final\\" + f)
    
