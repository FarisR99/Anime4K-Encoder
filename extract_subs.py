import subprocess
import sys

from pymkv import MKVFile

from utils import current_date

def genExt(codec):
    if "PGS" in codec:
        return "sup"
    elif "ASS" in codec or "SubStationAlpha" in codec:
        return "ass"
    elif "SRT" in codec or "SubRip" in codec:
        return "srt"
    elif "VobSub" in codec:
        return "idx"
    else:
        return None


def extract_subs(debug: bool, fn: str, out_dir: str) -> bool:
    """
    Extract subtitles from a media file.

    Args:
        fn: input media file path
        out_dir: directory where subtitles are extracted to
    Returns:
        True if the subtitles were successfully extracted
    """

    if out_dir is None:
        out_dir = ""

    print("Loading file={0}".format(fn))
    mkv = MKVFile(fn)

    print("Subtitle extraction start time: " + current_date())
    tracks = mkv.get_track()
    success = True
    for track in tracks:
        if track.track_type == 'subtitles':
            ext = genExt(track._track_codec)
            if ext is None:
                print(
                    "WARNING: Skipping unknown subtitle with id={0}, codec={1}".format(
                        str(track._track_id),
                        str(track._track_codec or "Unknown")))
                continue
            lang = track._language
            id = str(track._track_id)

            return_code = -1
            try:
                return_code = subprocess.call([
                    'mkvextract', 'tracks', fn,
                    id + ':' + str(out_dir) + str(lang) + '_' + id + '.' + ext
                ])
            except KeyboardInterrupt:
                print("Cancelled subtitles extraction.")
                print("Exiting program...")
                sys.exit(-1)
            if debug:
                print("mkvextract exited with return code={}", return_code)
            if return_code != 0:
                success = False
    print("Subtitle extraction end time: " + current_date())
    return success
