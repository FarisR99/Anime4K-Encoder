import os
import sys

from extract_audio import extract_audio
from extract_subs import extract_subs
from mux import clean_up, mux
from shader import shader
from utils import clear


def multi(input_files: "list[str]", width: int, height: int, shader_path: str,
          ten_bit: bool, skip_menus: dict, del_failures: bool, outname: str):
    """
    Run mode shader on the input files, then for each file successfully
    encoded with shaders applied, run extract audio and extract subs on
    the original input file, and finally mux the encoded file with the
    extracted subs and audio track files.

    Args:
        input_files: list of input media files
        width: desired width of video
        height: desired height of video
        shader_path: path where the shaders are located
        ten_bit: true if the input file(s) are a 10 bit source
        skip_menus: menu skipping options passed from command line
        del_failures: true if encoded output files should be deleted on failure
        outname: output path
    Returns:

    """

    if skip_menus is None:
        skip_menus = {}
    encoded_files = shader(input_files=input_files, width=width, height=height,
                           shader_path=shader_path, ten_bit=ten_bit,
                           language="", softsubs=True,
                           softaudio=True, skip_menus=skip_menus,
                           exit_on_cancel=False, outname=outname)
    clear()
    if len(encoded_files) == 0:
        print("error: no files encoded, terminating program early...")
        sys.exit(-2)
    else:
        print("Encoded files: {0}".format(", ".join(encoded_files.keys())))

    successful_inputs = {}
    failed_inputs = []
    for input_path, output_path in encoded_files.items():
        print()
        print("Starting mode subs for input={0}".format(input_path))
        if not extract_subs(input_path, ""):
            print(
                "Failed to extract subtitles for file={0}".format(input_path)
            )
            clean_up()
            if del_failures:
                print("Deleting encoded file and skipping...")
                os.remove(output_path)
            else:
                print("Skipping...")
            failed_inputs.append(input_path)
            continue
        print()
        print("Starting mode audio for input={0}".format(input_path))
        if not extract_audio(input_path, "", skip_menus):
            print(
                "Failed to extract audio for file={0}".format(input_path)
            )
            clean_up()
            if del_failures:
                print("Deleting encoded file and skipping...")
                os.remove(output_path)
            else:
                print("Skipping...")
            clean_up()
            failed_inputs.append(input_path)
            continue
        print()

        new_output = os.path.splitext(output_path)[0] + "-mux.mkv"
        print("Starting mode mux for input={0}, output={1}".format(output_path,
                                                                   new_output))
        try:
            mux(output_path, new_output)
        except Exception as e:
            print("Failed to mux file={0}".format(output_path))
            print(e)
            if os.path.isfile(new_output):
                print("Deleting compiled file={0}".format(new_output))
                os.remove(new_output)
            if del_failures:
                print("Deleting encoded file and skipping...")
                os.remove(output_path)
            else:
                print("Skipping...")
            failed_inputs.append(input_path)
            continue
        os.remove(output_path)
        os.rename(new_output, output_path)
        new_output = output_path
        print("Successfully compiled file={0}".format(new_output))
        successful_inputs[input_path] = new_output
    print()

    if len(successful_inputs) > 0:
        print(
            "All of the following input files have been encoded and compiled:")
        for input_path, output_path in successful_inputs.items():
            print(" {0} => {1}".format(input_path, output_path))
    if len(failed_inputs) > 0:
        print()
        if len(failed_inputs) == len(encoded_files):
            print("Failed to compile all encoded input files.")
        else:
            print("Failed to compile the following encoded input files:")
            print("\n".join(failed_inputs))
