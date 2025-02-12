import os
import subprocess
import sys

from simple_term_menu import TerminalMenu

from utils import current_date, is_tool, clear


def encode_to_hevc(debug: bool, input_files: "list[str]", out: str,
                   skip_menus: dict) -> dict:
    """
    Encode a media file to HEVC using X265

    Args:
        input_files: list of input media file paths
        out: output path
        skip_menus: menu skipping options passed from command line
    Returns:
        a mapping of successfully encoded input files to their output paths
    """

    param_line = "crf=18.0:limit-sao=1:bframes=8:aq-mode=3:psy-rd=1.0"

    detail_choice = None
    if "encode" in skip_menus:
        detail_choice = int(skip_menus["encode"])
        if detail_choice < 0 or detail_choice > 4:
            detail_choice = None
    if detail_choice is None:
        detail_menu = TerminalMenu(
            [
                "One setting to rule them all (Recommended if you don't know)",
                "Flat, slow anime (slice of life, everything is well lit, e.g. Your Name)",
                "Some dark scenes, some battle scenes (shonen, historical, etc., e.g. Kimetsu no Yaiba)",
                "[TV Series] Movie-tier dark scene, complex grain/detail (Rarely used)",
                "[Movie] Movie-tier dark scene, complex grain/detail (Rarely used)",
            ],
            title="Choose the encode options",
            clear_screen=(debug is False),
            clear_menu_on_exit=(debug is False)
        )
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

    encoded_files = {}

    file_count = len(input_files)
    start_time = current_date()
    print("Encoding start time: " + start_time)
    i = 0
    for f in input_files:
        print("Encoding start time for file={0}: {1}".format(
            str(i + 1),
            current_date()
        ))

        cmd.append("-i")
        cmd.append(f)
        output_path = None
        if file_count == 1 and not os.path.isdir(out):
            output_path = os.path.join(out)
        else:
            name = f.split("/")
            name = name[len(name) - 1]
            output_path = os.path.join(out, name + "-encoded.mkv")
        cmd.append(output_path)

        return_code = -1
        try:
            return_code = subprocess.call(cmd)
        except KeyboardInterrupt:
            print("Cancelled encoding for file={0}".format(f))
            print("Exiting program...")
            try:
                sys.exit(-1)
            except SystemExit:
                os._exit(-1)
        if return_code == 0:
            encoded_files[f] = output_path
        else:
            print("error: failed to encode file={0}".format(f))
        print("Encoding end time for file={0}: {1}".format(
            str(i + 1),
            current_date())
        )
        i = i + 1
        clear()
    print("Encoding start time: " + start_time)
    print("Encoded files: {0}".format(", ".join(encoded_files.keys())))
    print("Encoding end time: " + current_date())
    return encoded_files
