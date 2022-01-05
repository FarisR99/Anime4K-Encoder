import glob
import os
import subprocess
import sys

from simple_term_menu import TerminalMenu

from utils import current_date, is_tool, clear


def encode_to_hevc(fn: "list[str]", out: str, skip_menus: dict):
    """
    Encode a media file to HEVC using X265

    Args:
        fn: list of input media file/directory paths
        out: output path
        skip_menus: menu skipping options passed from command line
    """

    param_line = "crf=18.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.0"

    detail_choice = None
    if "encode" in skip_menus:
        detail_choice = int(skip_menus["encode"])
        if detail_choice < 0 or detail_choice > 4:
            detail_choice = None
    if detail_choice is None:
        detail_menu = TerminalMenu([
            "One setting to rule them all (Recommended if you don't know)",
            "Flat, slow anime (slice of life, everything is well lit, e.g. Your Name)",
            "Some dark scenes, some battle scenes (shonen, historical, etc., e.g. Kimetsu no Yaiba)",
            "[TV Series] Movie-tier dark scene, complex grain/detail (Rarely used)",
            "[Movie] Movie-tier dark scene, complex grain/detail (Rarely used)",
        ], title="Choose the encode options")
        detail_choice = detail_menu.show()
        if detail_choice is None:
            print("Cancelled")
            sys.exit(-1)

    if detail_choice == 1:
        # Flat, slow anime (slice of life, everything is well lit)
        param_line = "crf=19.0:bframes=8:aq-mode=3:psy-rd=1:aq-strength=0.8:deblock=1,1"
    elif detail_choice == 2:
        # Some dark scenes, some battle scenes (shonen, historical, etc.)
        param_line = "crf=18.0:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=2"
    elif detail_choice == 3:
        # [TV Series] Movie-tier dark scene, complex grain/detail
        param_line = "crf=18.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=3.5"
    elif detail_choice == 4:
        # [Movie] Movie-tier dark scene, complex grain/detail
        param_line = "crf=16.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=3.5"

    if is_tool("ffmpeg-bar"):
        binary = "ffmpeg-bar"
    else:
        binary = "ffmpeg"

    # Collect input files
    files = []
    for file in fn:
        if os.path.isdir(file):
            for input_file in glob.glob(os.path.join(file, "*.mkv")):
                files.append(os.path.join(input_file))
            for input_file in glob.glob(os.path.join(file, "*.mp4")):
                files.append(os.path.join(input_file))
        else:
            files.append(os.path.join(file))

    cmd = [
        binary,
        "-hide_banner",
        "-c:v",
        "libx265",
        "-profile:v",
        "main10",
        "-pix_fmt",
        "yuv420p10le",
        "-preset",
        "slow",
        "-x265-params",
        param_line,
        "-map",
        "0:v:0",
        "-f",
        "matroska",
        '-vf',
        'scale=out_color_matrix=bt709',
        '-color_primaries',
        'bt709',
        '-color_trc',
        'bt709',
        '-colorspace',
        'bt709'
    ]
    if len(files) == 1:
        print("Encoding start time: " + current_date())
        if os.path.isdir(out):
            if not os.path.exists(out):
                print("error: output directory={0} does not exist".format(out))
                sys.exit(-2)
            out = os.path.join(out,
                               os.path.basename(files[0]) + "-encoded.mkv")

        cmd.append("-i")
        cmd.append(files[0])
        cmd.append(out)
        try:
            subprocess.call(cmd)
        except KeyboardInterrupt:
            print("Cancelled encoding, exiting program...")
            try:
                sys.exit(-1)
            except SystemExit:
                os._exit(-1)
        print("Encoding end time: " + current_date())
    else:
        if not os.path.isdir(out):
            print(
                "error: when using multiple input files, the output must be a directory")
            sys.exit(-2)

        start_time = current_date()
        print("Encoding start time: " + start_time)
        i = 0
        for f in files:
            print("Encoding start time for file={0}: {1}".format(
                str(i + 1),
                current_date()
            ))

            name = f.split("/")
            name = name[len(name) - 1]
            cmd.append("-i")
            cmd.append(f)
            cmd.append(os.path.join(out, name + "-encoded.mkv"))
            try:
                subprocess.call(cmd)
            except KeyboardInterrupt:
                print("Cancelled encoding for file={0}".format(f))
                print("Exiting program...")
                try:
                    sys.exit(-1)
                except SystemExit:
                    os._exit(-1)
            print("Encoding end time for file={0}: {1}".format(
                str(i + 1),
                current_date())
            )
            i = i + 1
            clear()
        print("Encoding start time: " + start_time)
        print("Encoding end time: " + current_date())
