import os
import sys

from extract_audio import extract_audio, show_convert_audio_menu
from extract_subs import extract_subs
from mux import clean_up, mux
from utils import clear


def patch(input_files: "list[str]", skip_menus: dict, outname: str):
    """
    Run extract audio and extract subs on the original input files,
    and finally mux the encoded file that already exists in the output
    directory with the extracted subs and audio track files.

    Args:
        input_files: list of input media files
        skip_menus: menu skipping options passed from command line
        outname: output directory
    Returns:

    """

    if not os.path.exists(outname):
        print("error: output directory does not exist at {0}".format(outname))
        sys.exit(-2)
    if not os.path.isdir(outname):
        print("error: output must be a directory".format(outname))
        sys.exit(-2)

    successful_inputs = {}
    failed_inputs = []

    clear()
    show_convert_audio_menu(skip_menus)

    for input_file in input_files:
        input_file_name = os.path.basename(input_file)
        encoded_input_file = os.path.join(outname, input_file_name)
        if not os.path.exists(encoded_input_file):
            print(
                "error: could not locate encoded file, skipping input file={0}".format(
                    input_file))

        clear()
        if len(successful_inputs) > 0:
            print("Completed input files:\n {0}".format("\n ".join(
                [os.path.basename(successful_input) for successful_input in
                 successful_inputs]
            )))
            print()
        print("Processing input file={0}".format(input_file))

        print("Starting mode subs")
        extracted_subs = False
        try:
            extracted_subs = extract_subs(input_file, "")
        except Exception as ex:
            print(ex)
            extracted_subs = False
        if not extracted_subs:
            print(
                "Failed to extract subtitles for file={0}".format(input_file)
            )
            print("Skipping...")
            failed_inputs.append(input_file)
            clean_up()
            continue

        print()
        print("Starting mode audio".format(input_file))
        extracted_audio = False
        try:
            extracted_audio = extract_audio(input_file, "", skip_menus)
        except Exception as ex:
            print(ex)
            extracted_audio = False
        if not extracted_audio:
            print(
                "Failed to extract audio for file={0}".format(input_file)
            )
            print("Skipping...")
            failed_inputs.append(input_file)
            clean_up()
            continue
        print()

        new_output = os.path.splitext(encoded_input_file)[0] + "-mux.mkv"
        print("Starting mode mux for input={0}, output={1}".format(
            encoded_input_file,
            new_output))
        try:
            mux(encoded_input_file, new_output)
        except Exception as e:
            print("Failed to mux file={0}".format(encoded_input_file))
            print(e)
            if os.path.isfile(new_output):
                print("Deleting compiled file={0}".format(new_output))
                os.remove(new_output)
            failed_inputs.append(input_file)
            print("Skipping...")
            clean_up()
            continue
        os.remove(encoded_input_file)
        os.rename(new_output, encoded_input_file)
        new_output = encoded_input_file
        print("Successfully compiled file={0}".format(new_output))
        successful_inputs[input_file] = new_output

    clear()
    if len(successful_inputs) > 0:
        print(
            "All of the following input files have been compiled:")
        for input_path, output_path in successful_inputs.items():
            print(" {0} => {1}".format(input_path, output_path))
    if len(failed_inputs) > 0:
        print()
        if len(failed_inputs) == len(input_files):
            print("Failed to compile all input files.")
        else:
            print("Failed to compile the following unencoded input files:")
            print("\n".join(failed_inputs))
