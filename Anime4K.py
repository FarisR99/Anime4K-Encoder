import argparse
import os
import sys

from extract_audio import extract_audio
from extract_subs import extract_subs
from mux import mux
from shader import shader
from splitter import split_by_seconds, get_video_length
from utils import __current_version__, is_tool, credz, str2bool

credz()

if not is_tool("mkvextract"):
    print("mkvnixtool not installed. Please install it")
    sys.exit(-3)
if not is_tool("ffmpeg"):
    print("ffmpeg is not installed. Please install")
    sys.exit(-3)

if not is_tool("mpv"):
    print("mpv is not installed. Please install a new version")
    sys.exit(-3)

parser = argparse.ArgumentParser(
    description='Upscales animes to 4K automagically using Anime4K shaders.')
parser.add_argument("-v", "--version", required=False,
                    action='store_true',
                    help="Print the current version of Anime4K-Encoder")
parser.add_argument("-m", "--mode", required=False,
                    default="shader",
                    help="Mode: choose from audio, subs, shader, or mux, split")
parser.add_argument("-ew", "--width", required=False, type=int,
                    help="desired width when applying shader")
parser.add_argument("-eh", "--height", required=False, type=int,
                    help="desired height when applying shader")
parser.add_argument("-sd", "--shader_dir", required=False, type=str,
                    default="./shaders",
                    help="Path to shader folder")
parser.add_argument("-bit", "--bit", required=False, type=str2bool, nargs='?',
                    const=True, default=False,
                    help="Set this flag if the source file is 10bit when using shader")
parser.add_argument("-i", "--file", required=False, help="The input file")
parser.add_argument("-o", "--output", required=False,
                    help="Output filename/directory")
parser.add_argument("-sz", "--split_length", required=False, type=int,
                    default=10, help="Seconds to split the video in")
parser.add_argument("-ns", "--no_subtitles", required=False,
                    action='store_true',
                    default=False,
                    help="Set this flag if you want to manually burn in subtitles when using shader")

args = vars(parser.parse_args())
if args['version']:
    print("Anime4K-Encoder v" + __current_version__)
    sys.exit(1)

fn = args['file']
if fn is None:
    parser.print_help()
    print("error: the following arguments are required: -i/--file")
    sys.exit(-2)
if not os.path.isdir(fn):
    if not os.path.isfile(fn):
        print("{0} does not exist".format(fn))
        sys.exit(-2)

if args['output'] == None:
    outname = "out.mkv"
else:
    outname = args['output']

mode = args['mode']
if mode == "audio":
    extract_audio(fn)
elif mode == "subs":
    extract_subs(fn)
elif mode == "mux":
    mux(fn, outname)
elif mode == "shader":
    shader(fn, args['width'], args['height'], args['shader_dir'], args['bit'],
           args['no_subtitles'], outname)
elif mode == "split":
    length = get_video_length(fn)
    split_by_seconds(filename=fn, split_length=args['split_length'],
                     video_length=length, split_dir=args['output'])
else:
    print("Unknown option: {0}".format(mode))
