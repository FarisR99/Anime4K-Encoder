import glob
import os
import subprocess
import sys

from simple_term_menu import TerminalMenu

from utils import current_date, is_tool, clear


def encode_to_hevc(fn: str, out: str):
    """
    Encode a media file to HEVC

    Args:
        fn: media file path
        out: output path
    """

    param_line = "crf=18.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.0"

    detail_menu = TerminalMenu([
        "One setting to rule them all (Recommended if you don't know)",
        "Flat, slow anime (slice of life, everything is well lit, e.g. Your Name)",
        "Some dark scenes, some battle scenes (shonen, historical, etc., e.g. Kimetsu no Yaiba)",
        "[TV Series] Movie-tier dark scene, complex grain/detail (Rarely used)",
        "[Movie] Movie-tier dark scene, complex grain/detail (Rarely used)",
    ], title="Choose the encode options")

    choice = detail_menu.show()
    # Flat, slow anime (slice of life, everything is well lit)
    if choice == 1:
        param_line = "crf=19.0:bframes=8:aq-mode=3:psy-rd=1:aq-strength=0.8:deblock=1,1"
    # Some dark scenes, some battle scenes (shonen, historical, etc.)
    elif choice == 2:
        param_line = "crf=18.0:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=2"
    # [TV Series] Movie-tier dark scene, complex grain/detail
    elif choice == 3:
        param_line = "crf=18.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=3.5"
    # [Movie] Movie-tier dark scene, complex grain/detail
    elif choice == 4:
        param_line = "crf=16.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.5:psy-rdoq=3.5"

    if is_tool("ffmpeg-bar"):
        binary = "ffmpeg-bar"
    else:
        binary = "ffmpeg"

    files = []
    if os.path.isdir(fn):
        for file in glob.glob(os.path.join(fn, "*.mkv")):
            files.append(os.path.join(file))
    if len(files) == 0:
        print("Encoding start time: " + current_date())
        cmd = [
            binary,
            "-hide_banner",
            "-i",
            fn,
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
            'bt709',
            out
        ]
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
        print("Encoding start time: " + current_date())
        i = 0
        for f in files:
            clear()
            name = f.split("/")
            name = name[len(name) - 1]
            cmd = [
                binary,
                "-hide_banner",
                "-i",
                f,
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
                'bt709',
                os.path.join(out, name)
            ]
            try:
                subprocess.call(cmd)
            except KeyboardInterrupt:
                print("Cancelled encoding for file={0}".format(f))
                print("Exiting program...")
                try:
                    sys.exit(-1)
                except SystemExit:
                    os._exit(-1)
            print("Encoding end time for file=" + str(
                i + 1) + ": " + current_date())
            i = i + 1
        print("Encoding end time: " + current_date())
