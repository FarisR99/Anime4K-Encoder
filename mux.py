import glob
import os
import sys

from pymkv import MKVFile, MKVTrack

from utils import current_date, lang_long_to_short, lang_short_to_long

audio_file_extensions = [
    "AAC", "MP3", "DTS", "Opus", "FLAC", "TrueHD Atmos",
    "AC-3", "E-AC-3", "DTS-HD Master Audio"
]

subtitle_file_extensions = ["sup", "srt", "ass", "idx"]


def addAudio(source, ext: str):
    """
    Add all audio tracks with the specified extension to the source

    Args:
        source: source file
        ext: extension of the audio files
    """

    for file in glob.glob("*." + ext):
        t = MKVTrack(file)
        lang = file.split('.')[0]
        t.track_name = lang
        t.language = lang_long_to_short(lang)
        print("Adding audio track={0}".format(t.track_name))
        source.add_track(t)


def addSubs(source, ext: str):
    """
    Add all subtitles with the specified extension to the source

    Args:
        source: source file
        ext: extension of the subtitle files
    """

    for file in glob.glob("*." + ext):
        t = MKVTrack(file)
        lang = file.split('.')[0]
        if "_" in lang:
            lang = lang.split('_')[0]
        else:
            lang = lang
        t.track_name = lang_short_to_long(lang)
        try:
            t.language = lang
        except Exception as e:
            print("Failed to set track language to={0}".format(lang))
            raise e
        print("Adding new subs={0}".format(t.track_name))
        source.add_track(t)


def delete_by_extension(ext: str):
    """
    Delete all files with the specified extension

    Args:
        ext: File extension
    """
    for file in glob.glob("*." + ext):
        os.remove(file)


def clean_up():
    for audio_file_ext in audio_file_extensions:
        delete_by_extension(audio_file_ext)
    for subtitle_file_ext in subtitle_file_extensions:
        delete_by_extension(subtitle_file_ext)


def mux(debug: bool, fn: str, out: str):
    """
    Start the muxing process

    Args:
        fn: input media file path
        out: output file path
    """

    mkv = MKVFile(fn)

    for audio_file_ext in audio_file_extensions:
        addAudio(mkv, audio_file_ext)
    for subtitle_file_ext in subtitle_file_extensions:
        addSubs(mkv, subtitle_file_ext)

    print("Mux start time: " + current_date())
    try:
        mkv.mux(out)
    except KeyboardInterrupt:
        print("Cancelled process, exiting program...")
        os.remove(out)
        try:
            sys.exit(-1)
        except SystemExit:
            os._exit(-1)
    print("Mux end time: " + current_date())

    # Clean up
    print()
    print("Cleaning...")
    clean_up()
    print("Cleaned!")
