import os, sys, subprocess, argparse, functools, platform

# My ffmpeg directory, just because
#"F:\Downloads\ffmpeg-20181007-0a41a8b-win64-static\ffmpeg-20181007-0a41a8b-win64-static\bin\ffmpeg.exe"
# Required command for join
#C:/Users/Jamie/AppData/Local/Programs/Python/Python35/python.exe icfp.py -f "F:\Downloads\ffmpeg-20181007-0a41a8b-win64-static\ffmpeg-20181007-0a41a8b-win64-static\bin" -ha join --heads ICFP18Norm\\heads --tails ICFP18Norm\\tails -o ICFP18Norm\\final

rm = "del" if platform.system() == "Windows" else "rm"
sep = "\\" if platform.system() == "Windows" else "/"
drop = 5 if platform.system() == "Windows" else 3
exe = ".exe" if platform.system() == "Windows" else ""

## Script Functionality ##

#TODO - Complete
def normalise(args):
    ffmpeg = args.ffmpeg
    hwaccel = args.hardware_acceleration
    vids = args.videos
    output_dir = args.output_dir
    if output_dir is None: output_dir = path(vids, "normalized")
    
def join(args):
    ffmpeg = args.ffmpeg
    hwaccel = args.hardware_acceleration
    head_dir = args.heads
    tail_dir = args.tails
    output_dir = args.output_dir
    vids = [v for v in os.listdir(head_dir) if v.endswith("mp4")]
    for vid in vids:
        concat(path(ffmpeg, "ffmpeg" + exe),
               to=path(output_dir, vid),
               head=path(head_dir, vid),
               tail=path(tail_dir, vid))

def split(args):
    ffmpeg = args.ffmpeg
    hwaccel = args.hardware_acceleration
    heads = args.heads
    tails = args.tails
    head_length = args.head_length
    vid_dir = args.videos
    if heads is None: heads = path(vids, "heads")
    if tails is None: tails = path(vids, "tails")
    head_end = "00:00:{}".format(pad(str(head_length), 2, '0'))
    vids = [v for v in os.listdir(vid_dir) if v.endswith("mp4")]
    for vid in vids:
        length = find_length(path(ffmpeg, "ffprobe" + exe), path(vid_dir, vid)).split(":")
        secs = 0
        for t in length: secs = secs * 60 + int(t)
        secs -= head_length
        hours = str(secs // 3600)
        mins = str((secs % 3600) // 60)
        secs = str(secs % 60)
        tail_length = ":".join([pad(hours, 2, '0'), pad(mins, 2, '0'), pad(secs, 2, '0')])
        slice_vid(path(ffmpeg, "ffmpeg" + exe), path(vid_dir, vid), "00:00:00", head_end, path(heads, vid))
        slice_vid(path(ffmpeg, "ffmpeg" + exe), path(vid_dir, vid), head_end, tail_length, path(tails, vid))

def add_logo(args):
    ffmpeg = args.ffmpeg
    hwaccel = args.hardware_acceleration
    vid_dir = args.videos
    output_dir = args.output_dir
    logo = args.logo
    cmd = "{ffmpeg} -hwaccel nvdec -i {vid} -framerate 30000/1001 -loop 1 -i {logo} -filter_complex \"[1:v] fade=out:st=3:d=2:alpha=1 [ov]; [0:v][ov] overlay=10:10 [v]\" -map \"[v]\" -map 0:a -c:v h264_nvenc -c:a copy -shortest {out}"
    vids = [v for v in os.listdir(vid_dir) if v.endswith("mp4")]
    for vid in vids:
        execute(cmd.format(ffmpeg=path(ffmpeg, "ffmpeg" + exe), vid=path(vid_dir, vid), out=path(output_dir, vid), logo=logo))
        
## Helper Functions ##

def path(*parts): return sep.join(parts)
def pad(s, n, d): return (n - len(s)) * d + s
def execute(cmd):
    return str(subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout)[2:-drop]

def concat(ffmpeg, head, tail, to, fast=False):
    cmd1 = "{ffmpeg} -hwaccel nvdec -i {head} -c copy -bsf:v h264_mp4toannexb -f mpegts tmp-1.ts"
    cmd2 = "{ffmpeg} -hwaccel nvdec -i {tail} -c copy -bsf:v h264_mp4toannexb -f mpegts tmp-2.ts"
    cmd3 = "{ffmpeg} -hwaccel nvdec -f mpegts -i \"concat:tmp-1.ts|tmp-2.ts\" -c copy -bsf:a aac_adtstoasc {to}"
    cmd4 = "{rm} tmp-1.ts tmp-2.ts".format(rm=rm)
    #cmd = "{ffmpeg} -hwaccel nvdec -i {head} -i {tail} -filter_complex \"[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]\" -map \"[outv]\" -map \"[outa]\" -c:v h264_nvenc {to}"
    execute(cmd1.format(ffmpeg=ffmpeg, head=head))
    execute(cmd2.format(ffmpeg=ffmpeg, tail=tail))
    execute(cmd3.format(ffmpeg=ffmpeg, to=to))
    execute(cmd4)
    #execute(cmd.format(ffmpeg=ffmpeg, head=head, tail=tail, to=to))

def slice_vid(ffmpeg, vid, start, end, out):
    #cmd = ffmpeg + " -i {vid} -vcodec copy -acodec copy -ss {start} -t {duration} {out}"
    cmd = ffmpeg + " -hwaccel nvdec -ss {start} -i {vid} -t {duration} -c:v h264_nvenc -c:a aac -strict experimental -b:a 128k {out}"
    run = cmd.format(vid=vid, out=out, start=start, duration=end)
    execute(run)

def find_length(ffprobe, vid):
    cmd = ffprobe + " -v error -show_entries format=duration -sexagesimal -of default=noprint_wrappers=1:nokey=1 {vid}"
    run = cmd.format(vid=vid)
    return execute(run).split(".")[0]


## Main ##

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ICFP Video Processing Script")
    parser.add_argument("-f",
                        "--ffmpeg",
                        help="install directory of ffmpeg",
                        required=True)
    subparsers = parser.add_subparsers(help="help for subcommand")
    parser_normalise = subparsers.add_parser("normalize", help="normalizes the audio of every video in a directory")
    parser_normalise.add_argument("-v",
                                  "--videos",
                                  help="directory containing videos, defaults to current directory",
                                  default=".")
    parser_normalise.add_argument("-o",
                                  "--output-dir",
                                  help="directory to place results, defaults to video directory with new subfolder \"normalized\"",
                                  default=None)
    parser_normalise.set_defaults(func=normalise)
    parser_split = subparsers.add_parser("split", help="splits every video in a directory into a head and a tail, with the head of a specified length")
    parser_split.add_argument("-v",
                              "--videos",
                              help="directory containing videos, defaults to current directory",
                              default=".")
    parser_split.add_argument("-hd",
                              "--heads",
                              help="directory to place heads, defaults to video directory with new subfolder \"heads\"",
                              default=None)
    parser_split.add_argument("-td",
                              "--tails",
                              help="directory to place tails, defaults to video directory with new subfolder \"heads\"",
                              default=None)
    parser_split.add_argument("-l",
                              "--head-length",
                              help="how long the prefix split for the videos should be, in seconds (default 10)",
                              type=int,
                              default=10)
    parser_split.set_defaults(func=split)
    parser_join = subparsers.add_parser("join", help="remerges back videos split into heads and tails")
    parser_join.add_argument("-o",
                             "--output-dir",
                             help="directory to place results, defaults to a new subfolder \"joined\"",
                             default="joined")
    parser_join.add_argument("-hd",
                             "--heads",
                             help="directory containing heads, defaults to directory \"heads\" in current directory",
                             default="heads")
    parser_join.add_argument("-td",
                             "--tails",
                             help="directory containing tails, defaults to directory \"tails\" in current directory",
                             default="tails")
    parser_join.set_defaults(func=join)
    parser_icon = subparsers.add_parser("add-logos", help="adds the ICFP logo to each video in a directory, image is scaled automatically")
    parser_icon.add_argument("-v",
                             "--videos",
                             help="directory containing videos, defaults to current directory",
                             default=".")
    parser_icon.add_argument("-l",
                             "--logo",
                             help="this year's ICFP logo in png format",
                             required=True)
    parser_icon.add_argument("-o",
                             "--output-dir",
                             help="directory to place results, defaults to a new subfolder \"titled\"",
                             default="titled")
    parser.add_argument("-ha",
                        "--hardware-acceleration",
                        help="attempt to perform hardware acceleration where possible",
                        action="store_true")
    parser_icon.set_defaults(func=add_logo)
    args = parser.parse_args()
    args.func(args)
