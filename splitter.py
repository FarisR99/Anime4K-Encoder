import csv
import json
import math
import os
import shlex
import subprocess
import sys


def split_by_manifest(filename, manifest, vcodec="copy", acodec="copy",
                      extra="", **kwargs):
    """
    Split video into segments based on the given manifest file.

    Arguments:
        filename (str)      - Location of the video.
        manifest (str)      - Location of the manifest file.
        vcodec (str)        - Controls the video codec for the ffmpeg video
                            output.
        acodec (str)        - Controls the audio codec for the ffmpeg video
                            output.
        extra (str)         - Extra options for ffmpeg.
    """

    if not os.path.exists(manifest):
        print("File does not exist: %s".format(manifest))
        raise SystemExit

    with open(manifest) as manifest_file:
        manifest_type = manifest.split(".")[-1]
        if manifest_type == "json":
            config = json.load(manifest_file)
        elif manifest_type == "csv":
            config = csv.DictReader(manifest_file)
        else:
            print("Format not supported. File must be a csv or json file")
            raise SystemExit

        split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec,
                     "-acodec", acodec, "-y"] + shlex.split(extra)
        try:
            fileext = filename.split(".")[-1]
        except IndexError as e:
            raise IndexError("No . in filename. Error: " + str(e))
        for video_config in config:
            split_str = ""
            split_args = []
            try:
                split_start = video_config["start_time"]
                split_length = video_config.get("end_time", None)
                if not split_length:
                    split_length = video_config["length"]
                filebase = video_config["rename_to"]
                if fileext in filebase:
                    filebase = ".".join(filebase.split(".")[:-1])

                split_args += ["-ss", str(split_start), "-t",
                               str(split_length), filebase + "." + fileext]
                print(
                    "########################################################")
                print("About to run: " + " ".join(split_cmd + split_args))
                print(
                    "########################################################")
                subprocess.check_output(split_cmd + split_args)
            except KeyError as e:
                print("############# Incorrect format ##############")
                if manifest_type == "json":
                    print("The format of each json array should be:")
                    print(
                        "{start_time: <int>, length: <int>, rename_to: <string>}")
                elif manifest_type == "csv":
                    print(
                        "start_time,length,rename_to should be the first line ")
                    print("in the csv file.")
                print("#############################################")
                print(e)
                raise SystemExit


def get_video_length(filename: str) -> int:
    """
    Args:
        filename: input video file path

    Returns: video length
    """

    output = subprocess.check_output((
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1",
        filename)).strip()
    video_length = int(float(output))
    print("Video length in seconds: " + str(video_length))

    return video_length


def ceildiv(a, b) -> int:
    return int(math.ceil(a / float(b)))


def split_by_seconds(filename: str, split_length: int, vcodec: str = "copy",
                     acodec: str = "copy", extra: str = "",
                     video_length: int = None, split_dir: str = "./",
                     **kwargs):
    if split_length and split_length <= 0:
        print("Split length can't be 0")
        raise SystemExit

    if not video_length:
        video_length = get_video_length(filename)
    split_count = ceildiv(video_length, split_length)
    if (split_count == 1):
        print("Video length is less then the target split length.")
        raise SystemExit

    split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec, "-acodec",
                 acodec] + shlex.split(extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count):
        split_args = []
        if n == 0:
            split_start = 0
        else:
            split_start = split_length * n
        filebase = os.path.join(split_dir, "split")
        split_args += ["-ss", str(split_start), "-t", str(split_length),
                       filebase + "-" + str(n + 1) + "-of-" + str(
                           split_count) + "." + fileext]
        try:
            subprocess.check_output(split_cmd + split_args)
        except KeyboardInterrupt:
            print("Splitting cancelled, exiting program...")
            try:
                sys.exit(-1)
            except SystemExit:
                os._exit(-1)
