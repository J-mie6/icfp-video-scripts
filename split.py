#Note the Scala one is in npfl

import os, sys, subprocess

ffmpeg = r"F:\Downloads\ffmpeg-20181007-0a41a8b-win64-static\ffmpeg-20181007-0a41a8b-win64-static\bin\ffmpeg.exe"
ffprobe = r"F:\Downloads\ffmpeg-20181007-0a41a8b-win64-static\ffmpeg-20181007-0a41a8b-win64-static\bin\ffprobe.exe"
print(ffmpeg)

def pad(s, n, d): return (n - len(s)) * d + s

def slice_vid(vid, start, end, prefix):
    cmd = ffmpeg + " -i %s -vcodec copy -acodec copy -ss %s -t %s %s"
    run = cmd % (vid + ".mp4", start, end, f.split("\\")[0] + "\\" + prefix + "\\" + f.split("\\")[1] + ".mp4")
    os.system(run)

def find_length(vid):
    cmd = ffprobe + " -v error -show_entries format=duration -sexagesimal -of default=noprint_wrappers=1:nokey=1 {0}.mp4"
    run = cmd.format(vid)
    return str(subprocess.run(run, shell=True, stdout=subprocess.PIPE).stdout)[2:-5].split(".")[0]

if __name__ == "__main__":
    files = [os.path.join("ICFP18Norm", f[:-4]) for f in os.listdir("ICFP18Norm") if f.endswith("mp4")]
    for f in files:
        print(f)
        l = ":".join(pad(t, 2, '0') for t in find_length(f).split(":"))
        print(l)
        slice_vid(f, "00:00:00", "00:00:10", "heads")
        slice_vid(f, "00:00:10", l, "tails")
    
