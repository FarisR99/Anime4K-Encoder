import os

from ccolors import ccolors
from extract_audio import extract_audio, show_convert_audio_menu
from extract_subs import extract_subs
from mux import clean_up, mux
from shader import shader
from utils import clear


def multi(debug: bool, input_files: "list[str]", width: int, height: int,
          shader_path: str, ten_bit: bool, desired_fps: float,
          skip_menus: dict, del_failures: bool, outname: str):
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
        desired_fps: desired framerate of video
        skip_menus: menu skipping options passed from command line
        del_failures: true if encoded output files should be deleted on failure
        outname: output path
    """

    if skip_menus is None:
        skip_menus = {}

    successful_encoded_inputs = []
    failed_encoded_inputs = []
    successful_inputs = {}
    failed_inputs = []

    clear()
    show_convert_audio_menu(debug, skip_menus)

    for input_file in input_files:
        clear()
        if len(successful_inputs) > 0:
            print("Completed files:\n {0}".format("\n ".join(
                [os.path.basename(successful_input) for successful_input in
                 successful_inputs]
            )))
            print()

        encoded_files = shader(debug=debug, input_files=[input_file],
                               width=width, height=height,
                               shader_path=shader_path, ten_bit=ten_bit,
                               language="", softsubs=True,
                               softaudio=True, desired_fps=desired_fps,
                               skip_menus=skip_menus, exit_on_cancel=False,
                               outname=outname)
        if input_file not in encoded_files:
            print("error: failed to encode, skipping input file={0}".format(
                input_file))
            failed_encoded_inputs.append(input_file)
            continue
        successful_encoded_inputs.append(input_file)
        output_path = encoded_files[input_file]
        clear()

        print("Completed files: {0}".format(", ".join(successful_inputs)))
        print("Successfully encoded file: {0}".format(input_file))
        print()
        print("Starting mode subs for input={0}".format(input_file))
        extracted_subs = False
        try:
            extracted_subs = extract_subs(debug, input_file, "")
        except Exception as ex:
            print(ex)
            extracted_subs = False
        if not extracted_subs:
            print(
                "Failed to extract subtitles for file={0}".format(input_file)
            )
            clean_up()
            if del_failures:
                print("Deleting encoded file and skipping...")
                os.remove(output_path)
            else:
                print("Skipping...")
            failed_inputs.append(input_file)
            continue

        print()
        print("Starting mode audio for input={0}".format(input_file))
        extracted_audio = False
        try:
            extracted_audio = extract_audio(debug, input_file, "", skip_menus)
        except Exception as ex:
            print(ex)
            extracted_audio = False
        if not extracted_audio:
            print(
                "Failed to extract audio for file={0}".format(input_file)
            )
            clean_up()
            if del_failures:
                print("Deleting encoded file and skipping...")
                os.remove(output_path)
            else:
                print("Skipping...")
            clean_up()
            failed_inputs.append(input_file)
            continue
        print()

        new_output = os.path.splitext(output_path)[0] + "-mux.mkv"
        print("Starting mode mux for input={0}, output={1}".format(output_path,
                                                                   new_output))
        try:
            mux(debug, output_path, new_output)
        except Exception as e:
            print("Failed to mux file={0}".format(output_path))
            print(ccolors.FAIL + e)
            if os.path.isfile(new_output):
                print("Deleting compiled file={0}".format(new_output))
                os.remove(new_output)
            if del_failures:
                print("Deleting encoded file and skipping...")
                os.remove(output_path)
            else:
                print("Skipping...")
            failed_inputs.append(input_file)
            continue
        os.remove(output_path)
        os.rename(new_output, output_path)
        new_output = output_path
        print("Successfully compiled file={0}".format(new_output))
        successful_inputs[input_file] = new_output

    if not debug:
        clear()

    if len(successful_inputs) > 0:
        print(
            "All of the following input files have been encoded and compiled:")
        for input_path, output_path in successful_inputs.items():
            print(" {0} => {1}".format(input_path, output_path))
    if len(failed_encoded_inputs) > 0:
        print()
        print("Failed to encode the following input files:")
        print(" " + "\n ".join(failed_encoded_inputs))
    if len(failed_inputs) > 0:
        print()
        if len(failed_inputs) == len(successful_encoded_inputs):
            print("Failed to compile all encoded input files.")
        else:
            print("Failed to compile the following encoded input files:")
            print(" " + "\n ".join(failed_inputs))
