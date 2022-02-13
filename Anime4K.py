import argparse
import glob
import os
import sys

from encode import encode_to_hevc
from extract_audio import extract_audio
from extract_subs import extract_subs
from multi import multi
from mux import mux
from patch import patch
from shader import shader
from splitter import split_by_seconds, get_video_length
from utils import __current_version__, is_tool, credz, str2dict

# Constant variables
MODES_SUPPORTING_MULTI_INPUTS = ["shader", "multi", "encode", "patch"]
MODES_TO_IGNORE_OUTPUT_EXISTENCE = ["patch"]

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
parser.add_argument("--debug", "--verbose", required=False,
                    action='store_true',
                    help='Enable debug mode; print more information and no screen clearing')
parser.add_argument("-m", "--mode", required=False,
                    default="shader",
                    help='''Modes:
 shader - Apply Anime4K shaders and encode
 audio - Extract audio tracks from a media file
 subs - Extract subtitles from a media file
 mux - Mux/compile a media file with audio files and subtitle files
 multi - Apply shader with -ss and -sa, audio, subs and mux mode in order
 encode - Encode media files using X265 with predefined settings
 split - Split a media file into parts
 patch - Extract audio and subs from input files then mux with already upscaled 
         output files located in the output directory with matching file names.
         This is essentially a mux mode supporting multiple files.''')
parser.add_argument("-ew", "--width", required=False, type=int, default=3840,
                    help="Desired width when applying shader")
parser.add_argument("-eh", "--height", required=False, type=int, default=2160,
                    help="Desired height when applying shader")
parser.add_argument("-sd", "--shader_dir", required=False, type=str,
                    default="./shaders",
                    help="Path to shader folder")
parser.add_argument("-bit", "--bit", required=False,
                    action='store_true',
                    help="Set this flag if the source file is 10bit when using mode shader")
parser.add_argument("-i", "--input", required=False, action='append',
                    help="Input file/directory")
parser.add_argument("-o", "--output", required=False,
                    help="Output filename/directory")
parser.add_argument("-sz", "--split_length", required=False, type=int,
                    default=10, help="Seconds to split the video in")
parser.add_argument("-ss", "--softsubs", required=False,
                    action='store_true',
                    default=False,
                    help="Set this flag if you want to manually mux subtitles when using mode shader")
parser.add_argument("-sa", "--softaudio", required=False,
                    action='store_true',
                    default=False,
                    help="Set this flag if you want to manually mux audio when using mode shader")
parser.add_argument("-fps", "--fps", required=False, type=float,
                    help="Desired framerate when applying shader")
parser.add_argument("-sm", "--skip_menus", required=False, type=str2dict,
                    help='''Skip choice menus
Examples for mode shader:
 --skip_menus="shader=4,encoder=cpu,codec=h264,preset=fast,crf=23"
 --skip_menus="shader=4,encoder=nvenc,codec=hevc,preset=fast,qp=24"
Example for mode audio:
 --skip_menus="convert=0"
Example for mode encode:
 --skip_menus="encode=0"''')
parser.add_argument("-al", "--audio_language", required=False, type=str,
                    help=
                    '''Set this to the audio track language for the output video.
Supported values are ISO 639-2 three-letter language codes.
This will not do anything if "--softaudio" is used.''')
parser.add_argument("--delete_failures", required=False,
                    action='store_true',
                    default=False,
                    help="Set this flag to delete output files that have failed to compile when using mode multi")
parser.add_argument("-si", "--skip_input", required=False, action='append',
                    help="Input file to skip when using a directory as an input for modes shader, multi and patch")

args = vars(parser.parse_args())
if args['version']:
    print("Anime4K-Encoder v" + __current_version__)
    sys.exit(1)

debug = args['debug']
if debug is None:
    debug = False


def exit_if_missing(file_path: str, allow_dir: bool = True):
    if not os.path.isdir(file_path):
        if not os.path.isfile(file_path):
            print("error: input={0} does not exist".format(file_path))
            sys.exit(-2)
    elif allow_dir is False:
        print("error: cannot use a directory ({0}) as an input for this mode"
              .format(file_path))
        sys.exit(-2)


# Validate "mode" argument
mode = str(args['mode']).lower()
if mode == "subtitles":
    mode = "subs"

# Validate "input" argument
fn = args['input']
if fn is None:
    parser.print_help()
    print("error: the following arguments are required: -i/--input")
    sys.exit(-2)
if type(fn) is list:
    if len(fn) != 1:
        if mode not in MODES_SUPPORTING_MULTI_INPUTS:
            print(
                "error: cannot use multiple inputs with mode={0}".format(mode))
            sys.exit(-2)
        for file in fn:
            exit_if_missing(file, mode in MODES_SUPPORTING_MULTI_INPUTS)
    else:
        fn = fn[0]
        exit_if_missing(fn, mode in MODES_SUPPORTING_MULTI_INPUTS)
else:
    exit_if_missing(fn, mode in MODES_SUPPORTING_MULTI_INPUTS)
if mode in MODES_SUPPORTING_MULTI_INPUTS:
    if type(fn) is str:
        fn = [fn]

# Validate "output" argument
if mode == "audio" or mode == "subs":
    output = args['output']
    if output is None:
        output = ""
    if output != "":
        if not os.path.isdir(output):
            print("error: output directory {0} does not exist".format(output))
            sys.exit(-2)
        else:
            if not output.endswith("/"):
                output = output + "/"
elif mode in MODES_SUPPORTING_MULTI_INPUTS:
    output = args['output'] or "out.mkv"
    if mode not in MODES_TO_IGNORE_OUTPUT_EXISTENCE \
            and os.path.isdir(output) \
            and not os.path.exists(output):
        try:
            os.mkdir(output)
        except Exception as e:
            print(
                "error: failed to create output directory={0}:".format(output))
            print(e)
            sys.exit(-2)
else:
    output = args['output'] or "out.mkv"

# Collect input file paths from the input argument(s)
in_files = []
if mode in MODES_SUPPORTING_MULTI_INPUTS:
    skip_inputs = args['skip_input']
    if skip_inputs is None:
        skip_inputs = []
    elif type(skip_inputs) is str:
        skip_inputs = [skip_inputs]

    for file in fn:
        if os.path.isdir(file):
            for file_in_dir in glob.glob(
                    os.path.join(file, "*.mkv")
            ) + glob.glob(
                os.path.join(file, "*.mp4")
            ):
                file_name = os.path.basename(file_in_dir)
                if file_in_dir in skip_inputs or file_name in skip_inputs:
                    continue
                in_files.append(os.path.join(file_in_dir))
        else:
            # Only here for consistency
            # Why would you specify a file input then add that file
            # to a list of files to ignore?
            if file in skip_inputs or os.path.basename(file) in skip_inputs:
                continue
            in_files.append(os.path.join(file))
    file_count = len(in_files)
    if file_count > 1:
        if not os.path.isdir(output):
            print(
                "error: output path must be a directory when there are more than one input files")
            sys.exit(-2)
    elif file_count == 0:
        print("error: no valid input media files found")
        sys.exit(-2)

# Validate "skip_menus" argument
skip_menus = args['skip_menus']
if skip_menus is None:
    skip_menus = {}

# Perform action based on mode
if mode == "audio":
    extract_audio(debug, fn, output, skip_menus)
elif mode == "subs":
    extract_subs(debug, fn, output)
elif mode == "mux":
    mux(debug, fn, output)
elif mode == "shader":
    shader(debug, in_files, args['width'], args['height'],
           args['shader_dir'], args['bit'], args['audio_language'],
           args['softsubs'], args['softaudio'], args['fps'], skip_menus, True,
           output)
elif mode == "multi":
    multi(debug, in_files, args['width'], args['height'],
          args['shader_dir'], args['bit'], args['fps'], skip_menus,
          args['delete_failures'], output)
elif mode == "encode":
    encode_to_hevc(debug, in_files, output, skip_menus)
elif mode == "split":
    length = get_video_length(fn)
    split_by_seconds(debug=debug, filename=fn,
                     split_length=args['split_length'],
                     video_length=length, split_dir=output)
elif mode == "patch":
    patch(debug, in_files, skip_menus, output)
else:
    print("Unknown mode: {0}".format(mode))
