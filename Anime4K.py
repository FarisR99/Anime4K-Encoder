import argparse
import os
import sys

from extract_audio import extract_audio
from extract_subs import extract_subs
from multi import multi
from mux import mux
from shader import shader
from splitter import split_by_seconds, get_video_length
from utils import __current_version__, is_tool, credz, str2dict

# Constant variables
MODES_SUPPORTING_MULTI_INPUTS = ["shader", "multi"]

# Print credits
credz()

# Check for required tools
if not is_tool("mkvextract"):
    print("mkvnixtool not installed. Please install it")
    sys.exit(-3)
if not is_tool("ffmpeg"):
    print("ffmpeg is not installed. Please install")
    sys.exit(-3)

if not is_tool("mpv"):
    print("mpv is not installed. Please install a new version")
    sys.exit(-3)

# Parse arguments
parser = argparse.ArgumentParser(
    description='Upscales animes to 4K automagically using Anime4K shaders.',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-v", "--version", required=False,
                    action='store_true',
                    help="Print the current version of Anime4K-Encoder")
parser.add_argument("-m", "--mode", required=False,
                    default="shader",
                    help='''Modes:
 shader - Apply Anime4K shaders and encode
 audio - Extract audio tracks from a media file
 subs - Extract subtitles from a media file
 mux - Mux/compile a media file with audio files and subtitle files
 multi - Apply shader with -ss and -sa, audio, subs and mux mode in order
 split - Split a media file into parts''')
parser.add_argument("-ew", "--width", required=False, type=int, default=3840,
                    help="Desired width when applying shader")
parser.add_argument("-eh", "--height", required=False, type=int, default=2160,
                    help="Desired height when applying shader")
parser.add_argument("-sd", "--shader_dir", required=False, type=str,
                    default="./shaders",
                    help="Path to shader folder")
parser.add_argument("-bit", "--bit", required=False,
                    action='store_true',
                    help="Set this flag if the source file is 10bit when using shader")
parser.add_argument("-i", "--input", required=False, action='append',
                    help="The input file/directory")
parser.add_argument("-o", "--output", required=False,
                    help="Output filename/directory")
parser.add_argument("-sz", "--split_length", required=False, type=int,
                    default=10, help="Seconds to split the video in")
parser.add_argument("-ss", "--softsubs", required=False,
                    action='store_true',
                    default=False,
                    help="Set this flag if you want to manually mux subtitles when using shader")
parser.add_argument("-sa", "--softaudio", required=False,
                    action='store_true',
                    default=False,
                    help="Set this flag if you want to manually mux audio when using shader")
parser.add_argument("-sm", "--skip_menus", required=False, type=str2dict,
                    help='''Skip shader/encoding choice menus when using shader
Example:
 --skip_menus="shader=4,encoder=cpu,codec=h264,preset=fast,crf=23"
 --skip_menus="shader=4,encoder=nvenc,codec=hevc,preset=fast,qp=24"''')
parser.add_argument("-al", "--audio_language", required=False, type=str,
                    help=
                    '''Set this to the audio track language for the output video.
This will not do anything if "--softaudio" is used.''')

args = vars(parser.parse_args())
if args['version']:
    print("Anime4K-Encoder v" + __current_version__)
    sys.exit(1)


def exit_if_missing(file_path: str, allow_dir: bool = True):
    if not os.path.isdir(file_path):
        if not os.path.isfile(file_path):
            print("error: input={0} does not exist".format(file_path))
            sys.exit(-2)
    elif allow_dir is False:
        print("error: cannot use a directory ({0}) as an input for this mode"
              .format(file_path))


fn = args['input']
mode = str(args['mode']).lower()

# Validate "input" argument
if fn is None:
    parser.print_help()
    print("error: the following arguments are required: -i/--input")
    sys.exit(-2)
if type(fn) is list:
    if len(fn) != 1:
        if mode != "shader":
            print(
                "error: Cannot use multiple inputs with mode={0}".format(mode))
            sys.exit(-2)
        for file in fn:
            exit_if_missing(file, mode in MODES_SUPPORTING_MULTI_INPUTS)
    else:
        fn = fn[0]
        exit_if_missing(fn, mode in MODES_SUPPORTING_MULTI_INPUTS)
else:
    exit_if_missing(fn, mode in MODES_SUPPORTING_MULTI_INPUTS)

if mode == "subtitles":
    mode = "subs"

# Validate "output" argument
if mode == "audio" or mode == "subs":
    output = args['output']
    if output is None:
        output = ""
    if output != "":
        if not os.path.isdir(output):
            print("Output directory {0} does not exist".format(output))
            sys.exit(-2)
        else:
            if not output.endswith("/"):
                output = output + "/"
elif mode == "mux" or mode == "shader" or mode == "multi":
    output = args['output'] or "out.mkv"
elif mode == "split":
    output = args['output']

if mode == "audio":
    extract_audio(fn, output)
elif mode == "subs":
    extract_subs(fn, output)
elif mode == "mux":
    mux(fn, output)
elif mode == "shader":
    if type(fn) is str:
        fn = [fn]
    shader(fn, args['width'], args['height'], args['shader_dir'], args['bit'],
           args['audio_language'], args['softsubs'], args['softaudio'],
           args['skip_menus'] or {}, output)
elif mode == "multi":
    if type(fn) is str:
        fn = [fn]
    multi(fn, args['width'], args['height'], args['shader_dir'], args['bit'],
          args['skip_menus'], output)
elif mode == "split":
    length = get_video_length(fn)
    split_by_seconds(filename=fn, split_length=args['split_length'],
                     video_length=length, split_dir=output)
else:
    print("Unknown option: {0}".format(mode))
