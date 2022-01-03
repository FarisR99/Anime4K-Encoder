import subprocess

from pymkv import MKVFile

from utils import current_date


def genExt(codec):
    if "PGS" in codec:
        return "sup"
    elif "ASS" in codec or "SubStationAlpha" in codec:
        return "ass"
    elif "SRT" in codec or "SubRip" in codec:
        return "srt"
    else:
        return None


def extract_subs(fn: str, out_dir: str):
    """
    Extract subtitles from a media file.

    Args:
        fn: input media file path
        out_dir: directory where subtitles are extracted to
    """

    if out_dir is None:
        out_dir = ""

    print("Loading file={0}".format(fn))
    mkv = MKVFile(fn)

    print("Subtitle extraction start time: " + current_date())
    tracks = mkv.get_track()
    for track in tracks:
        if track.track_type == 'subtitles':
            ext = genExt(track._track_codec)
            if ext is None:
                continue
            lang = track._language
            id = str(track._track_id)

            subprocess.call(['mkvextract', 'tracks', fn,
                             id + ':' + str(out_dir) + str(
                                 lang) + '_' + id + '.' + ext])
    print("Subtitle extraction end time: " + current_date())
