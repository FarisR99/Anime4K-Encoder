import argparse
import os
import sys

from extract_audio import extract_audio
from extract_subs import extract_subs
from utils import is_tool

if not is_tool("mkvextract"):
    print("mkvnixtool not installed. Please install it")
    sys.exit(-3)

# Parse arguments
parser = argparse.ArgumentParser(
    description='Extracts audio and subtitles from a media file.',
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-i", "--input", required=True,
                    help="Input file path")
parser.add_argument("-o", "--output", required=False,
                    help="Output directory path")
parser.add_argument("--extract", required=True,
                    action="store", choices=["audio", "subtitles"],
                    help="What to extract, valid values=[audio, subtitles]")
args = vars(parser.parse_args())

input_path = args["input"]
extract = args["extract"]
output = args["output"]

if not os.path.exists(input_path):
    print("input={0} does not exist", input_path)
    sys.exit(-2)
elif not os.path.isfile(input_path):
    print("input={0} is not a file", input_path)
    sys.exit(-2)
if output is not None and not os.path.isdir(output):
    print("output={0} is not a directory", output)
    sys.exit(-2)

if extract == "audio":
    success = extract_audio(True, input_path, output, {
        "convert": "0",
        "recommended": "1"
    })
elif extract == "subs" or extract == "subtitles":
    success = extract_subs(True, input_path, output)
else:
    print("Invalid command line argument extract={0}".format(extract))
    success = False
if success:
    sys.exit(0)
else:
    sys.exit(-1)
