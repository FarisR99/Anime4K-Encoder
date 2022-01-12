import glob
import os
import subprocess
import sys
import time

from pymkv import MKVFile
from simple_term_menu import TerminalMenu

from utils import current_date, language_mapping


def extract_audio(fn: str, out_dir: str, skip_menus: dict) -> bool:
    """
    Extract audio from a media file.

    Args:
        fn: input media file path
        out_dir: directory where audio files are extracted to
        skip_menus: menu skipping options passed from command line
    Returns:
        True if the audio tracks were successfully extracted
    """

    if out_dir is None:
        out_dir = ""

    print("Loading file={0}".format(fn))
    mkv = MKVFile(fn)
    success = True

    # Extract tracks from input media
    print("Audio extraction start time: " + current_date())
    tracks = mkv.get_track()
    for track in tracks:
        if track.track_type == 'audio':
            ext = track._track_codec
            lang = language_mapping[track._language]
            id = str(track._track_id)
            return_code = -1
            try:
                return_code = subprocess.call([
                    'mkvextract', 'tracks', fn,
                    id + ':' + out_dir + lang + '.' + ext
                ])
            except KeyboardInterrupt:
                print("Cancelled track extraction.")
                print("Please clear the audio files in the current directory.")
                print("Exiting program...")
                try:
                    sys.exit(-1)
                except SystemExit:
                    os._exit(-1)
            if return_code != 0:
                success = False

    print("Audio extraction end time: " + current_date())

    flacs = []
    for file in glob.glob(out_dir + "*.FLAC"):
        flacs.append(file)
    if len(flacs) > 0:
        convert_choice = None
        if "convert" in skip_menus:
            convert_choice = int(skip_menus['convert'])
            if convert_choice < 0 or convert_choice > 1:
                convert_choice = None
            else:
                # Flip the value, because "1" in the command line arg means
                # "Yes" which is at index 0 in convert_menu choice array
                convert_choice = 1 - convert_choice
        if convert_choice is None:
            convert_menu = TerminalMenu(
                ["Yes", "No"],
                title="Do you want to convert every FLAC to Opus?"
            )
            convert_choice = convert_menu.show()
            if convert_choice is None:
                print("Cancelled conversion")

        if convert_choice == 0:
            print("Conversion start time: " + current_date())
            for f in flacs:
                bit_rates = ["192K", "256K", "320K"]
                br_choice = None
                if "bitrate" in skip_menus:
                    br_choice = bit_rates.index(skip_menus["bitrate"])
                    if br_choice < 0 or br_choice > 2:
                        br_choice = None
                if br_choice is None:
                    br_menu = TerminalMenu(
                        bit_rates,
                        title="What's the format of the file? => {0}".format(f)
                    )
                    br_choice = br_menu.show()
                    if br_choice is None:
                        print("Cancelled conversion")
                        continue
                if br_choice == 0:
                    br = "192K"
                elif br_choice == 1:
                    br = "256K"
                elif br_choice == 2:
                    br = "320K"

                fn_base = f.split(".")[0]
                out_audio = fn_base + ".Opus"
                return_code = -1
                try:
                    return_code = subprocess.call([
                        "ffmpeg",
                        "-hide_banner",
                        "-i",
                        f,
                        "-c:a",
                        "libopus",
                        "-b:a",
                        br,
                        "-vbr",
                        "on",
                        out_audio
                    ])
                except KeyboardInterrupt:
                    print("Cancelled conversion.")
                    os.remove(out_audio)
                time.sleep(1)
                if return_code == 0:
                    os.remove(f)
            print("Conversion end time: " + current_date())
    return success
