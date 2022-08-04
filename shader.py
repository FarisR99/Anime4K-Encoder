import math
import os
import subprocess
import sys

from simple_term_menu import TerminalMenu

from consts import *
from utils import current_date, clear


# Menus

def menu_fhd_shaders(debug: bool, shader_path: str, skip_menus: dict) -> str:
    """
    Select a shader for FHD or higher resolution videos.

    Args:
        shader_path: path the shaders are located at
        skip_menus: menu skipping options passed from command line

    Returns:
        Shader string with selected shaders
    """

    mode_choice = None
    if "shader" in skip_menus:
        mode_choice = int(skip_menus['shader'])
        if mode_choice < 0 or mode_choice > 5:
            mode_choice = None
    elif "recommended" in skip_menus and skip_menus['recommended'] == "1":
        mode_choice = 4
    if mode_choice is None:
        mode_menu = TerminalMenu(
            [
                "Mode A (High Quality, Medium Artifacts)",
                "Mode B (Medium Quality, Minor Artifacts)",
                "Mode C (Unnoticeable Quality Improvements)",
                "Mode A+A (Higher Quality, Might Oversharpen)",
                "Mode B+B (RECOMMENDED. High Quality, Minor Artifacts)",
                "Mode C+A (Low Quality, Minor Artifacts)"
            ],
            title="Please refer to the Anime4k Wiki for more info and try the\n shaders on mpv beforehand to know what's best for you.\nChoose Shader Preset:",
            clear_screen=(debug is False),
            clear_menu_on_exit=(debug is False)
        )
        mode_choice = mode_menu.show()

        if mode_choice is None:
            print("Canceling")
            sys.exit(-1)
    skip_menus['shader'] = str(mode_choice)

    if mode_choice == 0:
        s = os.path.join(shader_path, Clamp_Highlights)
        s = s + ":"
        s = s + os.path.join(shader_path, Restore_CNN_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x2)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x4)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_M)
        return s
    elif mode_choice == 1:
        s = os.path.join(shader_path, Clamp_Highlights)
        s = s + ":"
        s = s + os.path.join(shader_path, Restore_CNN_Soft_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x2)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x4)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_M)
        return s
    elif mode_choice == 2:
        s = os.path.join(shader_path, Clamp_Highlights)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_Denoise_CNN_x2_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x2)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x4)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_M)
        return s
    elif mode_choice == 3:
        s = os.path.join(shader_path, Clamp_Highlights)
        s = s + ":"
        s = s + os.path.join(shader_path, Restore_CNN_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, Restore_CNN_M)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x2)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x4)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_M)
        return s
    elif mode_choice == 4:
        s = os.path.join(shader_path, Clamp_Highlights)
        s = s + ":"
        s = s + os.path.join(shader_path, Restore_CNN_Soft_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x2)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x4)
        s = s + ":"
        s = s + os.path.join(shader_path, Restore_CNN_Soft_M)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_M)
        return s
    elif mode_choice == 5:
        s = os.path.join(shader_path, Clamp_Highlights)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_Denoise_CNN_x2_VL)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x2)
        s = s + ":"
        s = s + os.path.join(shader_path, AutoDownscalePre_x4)
        s = s + ":"
        s = s + os.path.join(shader_path, Restore_CNN_M)
        s = s + ":"
        s = s + os.path.join(shader_path, Upscale_CNN_x2_M)
        return s
    else:
        print("Invalid shader mode choice")
        sys.exit(-1)


# Core

def remove_audio_and_subs(fn: str, softsubs: bool, softaudio: bool) -> int:
    """
    Remove audio and optionally subtitles from a file.

    Args:
        fn: media file path
        softsubs: true if subtitles should be removed
        softaudio: true if audio should be removed
    Returns:
        return code of the merge process
    """

    args = [
        "mkvmerge",
        "-o",
        "temp.mkv"
    ]
    if softsubs:
        args.append("--no-subtitles")
    if softaudio:
        args.append("--no-audio")
    args.append(fn)

    try:
        return subprocess.call(args)
    except KeyboardInterrupt:
        print("File processing cancelled for file={0}".format(fn))
        shader_cleanup()
        print("Exiting program...")
        try:
            sys.exit(-1)
        except SystemExit:
            os._exit(-1)


def shader_cleanup():
    """
    Post-encoding cleanup
    """

    os.remove("temp.mkv")


def handle_encoding_cancellation(file_name: str, output_file, start_time: str,
                                 exit: bool):
    """
    Handle cancellation during encoding

    Args:
        file_name: The current file being encoded
        output_file: The output file to delete
        start_time: The time the first file began encoding
        exit: true if the program should terminate
    """

    print("Cancelled encoding of file={0}".format(file_name))
    print("Start time: {0}".format(start_time))
    print("End time: " + current_date())
    print()
    print("Deleting temporary files...")
    shader_cleanup()
    if output_file is not None:
        os.remove(output_file)
    if exit:
        print("Exiting program...")
        try:
            sys.exit(-1)
        except SystemExit:
            os._exit(-1)


def getLevel(encoder: str, width: int, height: int, desired_fps: float):
    if desired_fps is None:
        desired_fps = 0.0
    if "h264" in encoder or "x264" in encoder:
        if (width * height) <= (1920 * 1080):
            if desired_fps > 60:
                return 5.1
            elif desired_fps > 30:
                return 4.2
            else:
                return 4.1
        else:
            if desired_fps > 60:
                return 6.0
            elif desired_fps > 30:
                return 5.2
            else:
                return 5.1
    elif "hevc" in encoder or "h265" in encoder or "x265" in encoder:
        if (width * height) <= (1920 * 1080):
            if desired_fps > 60:
                return 5.0
            elif desired_fps > 30:
                return 4.1
            else:
                return 4.0
        else:
            if desired_fps > 60:
                return 5.2
            elif desired_fps > 30:
                return 5.1
            else:
                return 5.0
    return 5.1


def shader(debug: bool, input_files: "list[str]", width: int, height: int,
           shader_path: str,
           ten_bit: bool, language: str, softsubs: bool, softaudio: bool,
           desired_fps: float, skip_menus: dict, exit_on_cancel: bool,
           outname: str) -> dict:
    """
    Select encoding and start the encoding process.

    Args:
        input_files: list of input media paths
        width: output width
        height: output height
        shader_path: path the shaders are located at
        ten_bit: true if the input media is a 10 bit source
        language: optional desired audio track language
        softsubs: true if subtitles should be removed
        softaudio: true if audio should be removed
        desired_fps: output framerate
        skip_menus: menu skipping options passed from command line
        exit_on_cancel: true if the program should exit when the user cancels
            during encoding, false if the function call should terminate
        outname: output path

    Returns:
        mapping of files that were successfully encoded to their output paths
    """

    if not os.path.isdir(shader_path):
        print("error: shaders directory does not exist at: {0}".format(
            shader_path))
        sys.exit(-2)

    output_is_dir = os.path.isdir(outname)
    if len(input_files) == 1:
        if output_is_dir:
            new_outname = os.path.join(outname,
                                       os.path.basename(input_files[0]))
            out_name_index = 1
            while os.path.exists(new_outname):
                new_outname = os.path.join(outname, "out-{0}.mkv"
                                           .format(str(out_name_index)))
                out_name_index = out_name_index + 1
            outname = new_outname
            output_is_dir = False
        if not debug:
            clear()
        remove_audio_and_subs(input_files[0], softsubs, softaudio)
        if not debug:
            clear()
        else:
            print()

    # Select encoder
    encoder = ""

    if "encoder" in skip_menus:
        encoder = skip_menus['encoder']
    if encoder == "":
        if "recommended" in skip_menus and skip_menus["recommended"] == "1":
            encoder = "x264"
    if encoder == "":
        cg_menu = TerminalMenu(
            [
                "CPU - X264 (Medium Quality/Size ratio, Fast)",
                "CPU - X265 (High Quality/Size ratio, Slow)",
                "CPU - AV1 (Very High Quality/Size ratio)",
                "NVIDIA GPU - NVENC H264",
                "NVIDIA GPU - NVENC HEVC",
                "AMD GPU - VAAPI H264",
                "AMD GPU - VAAPI HEVC",
                "Intel QuickSync - X264 (Low Quality, Fast)",
                "Intel QuickSync - HEVC (Low Quality, Slow)"
            ],
            title="Choose Encoder:",
            clear_screen=(debug is False),
            clear_menu_on_exit=(debug is False)
        )
        cg_choice = cg_menu.show()
        if cg_choice == 0:
            encoder = "x264"
        elif cg_choice == 1:
            encoder = "x265"
        elif cg_choice == 2:
            encoder = "cpu_av1"
        elif cg_choice == 3:
            encoder = "nvenc_h264"
        elif cg_choice == 4:
            encoder = "nvenc_hevc"
        elif cg_choice == 5:
            encoder = "vaapi_h264"
        elif cg_choice == 6:
            encoder = "vaapi_hevc"
        elif cg_choice == 7:
            encoder = "h264_qsv"
        elif cg_choice == 8:
            encoder = "hevc_qsv"
        else:
            print("Cancelled")
            shader_cleanup()
            sys.exit(-2)
    skip_menus['encoder'] = encoder

    return start_encoding(debug, encoder, width, height, shader_path,
                          ten_bit, language, softsubs, softaudio, desired_fps,
                          skip_menus, exit_on_cancel, input_files, outname)


def start_encoding(debug: bool, encoder: str, width: int,
                   height: int, shader_path: str, ten_bit: bool, language: str,
                   softsubs: bool, softaudio: bool, desired_fps: float,
                   skip_menus: dict, exit_on_cancel: bool, files: "list[str]",
                   outname: str) -> dict:
    """
    Start the encoding of input file(s) to the specified encoding using the CPU.
    """

    if not debug:
        clear()

    if ten_bit:
        vid_format = "yuv420p10le"
    else:
        vid_format = "yuv420p"

    # Open shaders menu
    str_shaders = menu_fhd_shaders(debug, shader_path, skip_menus)
    if not debug:
        clear()
    else:
        print()

    # Select Encoder Presets
    encoder_presets = []
    encoder_preset = None
    if not encoder.startswith("vaapi_"):
        if encoder == "x264" or encoder == "x265" or encoder.endswith("_qsv"):
            encoder_presets = [
                "ultrafast", "veryfast", "fast", "medium", "slow", "veryslow"
            ]
        elif encoder.startswith("nvenc_"):
            encoder_presets = ["fast", "medium", "slow", "lossless"]
        else:
            encoder_presets = ["fast", "medium", "slow"]
        if "preset" in skip_menus:
            encoder_preset = skip_menus['preset']
            if encoder_preset not in encoder_presets:
                encoder_preset = None
        elif "recommended" in skip_menus and skip_menus["recommended"] == "1":
            encoder_preset = "fast"
        if encoder_preset is None:
            selected_encoder_preset = TerminalMenu(
                encoder_presets,
                title="Choose Encoder Preset:",
                clear_screen=(debug is False),
                clear_menu_on_exit=(debug is False)
            ).show()
            if selected_encoder_preset is None:
                print("Cancelled")
                shader_cleanup()
                sys.exit(-1)
            encoder_preset = encoder_presets[selected_encoder_preset]
        skip_menus['preset'] = encoder_preset

    comp_level = ""
    if encoder == "x264" or encoder == "x265" or encoder.endswith("_qsv"):
        if "crf" in skip_menus:
            crf = int(skip_menus['crf'])
            if 0 <= crf <= 51:
                comp_level = str(crf)
            else:
                comp_level = "23"
                print("Invalid crf provided, using default crf={0}".format(
                    comp_level))
        elif "recommended" in skip_menus and skip_menus["recommended"] == "1":
            comp_level = "23"
        else:
            comp_level = input(
                "Insert compression factor (CRF) 0-51\n0 = Lossless | 23 = Default | 51 = Highest compression\n"
            )
            if comp_level == "" or comp_level is None:
                comp_level = "23"
        skip_menus['crf'] = comp_level
    else:
        if "qp" in skip_menus:
            qp = int(skip_menus['qp'])
            if 0 <= qp <= 51:
                comp_level = str(qp)
            else:
                comp_level = "24"
                print("Invalid qp provided, using default qp={0}".format(
                    comp_level))
        elif "recommended" in skip_menus and skip_menus["recommended"] == "1":
            comp_level = "24"
        else:
            comp_level = input(
                "Insert Quantization Parameter (QP) 0-51\n0 = Lossless | 24 = Default | 51 = Highest compression\n"
            )
            if comp_level == "" or comp_level is None:
                comp_level = "24"
        skip_menus['qp'] = comp_level

    # Print Info
    files_string = ", ".join(files)
    print("Files: {0}".format(files_string))
    print("Using the following shaders:")
    print(str_shaders)
    if not encoder.startswith("vaapi_"):
        print("Encoding with preset: {0} compression={1}".format(encoder_preset,
                                                                 comp_level))
    else:
        print("Encoding with preset: qp={0}".format(comp_level))
    start_time = current_date()
    print("Start time: " + start_time)
    import time
    time.sleep(3)
    if not debug:
        clear()
    else:
        print()

    # Encode
    encoding_args = [
        "mpv",
        "--no-config",
        "--profile=gpu-hq",
        "--vf-add=format=" + vid_format,
        '--vf-add=gpu=w=' + str(width) + ':h=' + str(height),
        '--vf-pre=sub',
        "--scale=ewa_lanczossharp",
        "--cscale=ewa_lanczossharp",
        "--video-sync=display-resample",
        "--interpolation",
        "--tscale=oversample",
        "--glsl-shaders=" + str_shaders,
        "--oac=libopus",
        "--oacopts=b=192k",
    ]
    if language is not None and language != "":
        encoding_args.append("--alang=" + str(language))
    if encoder.endswith("_qsv") and desired_fps is None:
        print("ERROR: Intel QuickSync requires an FPS to be set.")
        sys.exit(-1)
    if desired_fps is not None and desired_fps > 0:
        encoding_args.append("--vf-add=fps=" + str(desired_fps))
        if encoder.endswith("_qsv"):
            encoding_args.append("--ovcopts-add=time_base=1000/" + str(math.floor(desired_fps * 1000)))

    # Arguments specific to the encoding and encoder specified
    level = getLevel(encoder, width, height, desired_fps)
    if encoder == "x264" or encoder == "x265":
        bf = 6 if len(files) == 1 else 8

        if encoder == "x264":
            encoding_args.append("--ovc=libx264")
            encoding_args.append('--ovcopts=preset=' + encoder_preset + ',level=' + str(level) + ',crf=' + str(
                comp_level) + ',aq-mode=3,psy-rd=1.0,bf=' + str(bf))
        elif encoder == "x265":
            encoding_args.append("--ovc=libx265")
            encoding_args.append(
                '--ovcopts=preset=' + encoder_preset + ',level=' + str(level) + ',crf=' + str(
                    comp_level) + ',bf=' + str(
                    bf))
        else:
            print("ERROR: Unknown encoder: {0}".format(encoder))
            shader_cleanup()
            sys.exit(-2)
    elif encoder.startswith("nvenc_"):
        encoding_args.append("--ovcopts-add=rc=constqp")
        encoding_args.append("--ovcopts-add=preset={0}".format(encoder_preset))
        encoding_args.append("--ovcopts-add=qp={0}".format(comp_level))
        encoding_args.append("--ovcopts-add=rc-lookahead={0}".format(32))
        if encoder == "nvenc_h264":
            encoding_args.append("--ovc=h264_nvenc")
            encoding_args.append("--ovcopts-add=profile=high")
            encoding_args.append("--ovcopts-add=level={0}".format(str(level)))
        elif encoder == "nvenc_h265":
            encoding_args.append("--ovc=hevc_nvenc")
            encoding_args.append("--ovcopts-add=profile=main10")
    elif encoder.startswith("vaapi_"):
        profile = ""
        if encoder == "h264":
            encoding_args.append("--ovc=h264_vaapi")
            profile = "high"
        elif encoder == "hevc":
            encoding_args.append("--ovc=hevc_vaapi")
            profile = "main10"
        encoding_args.append("--ovcopts-add=rc_mode=CQP")
        encoding_args.append("--ovcopts-add=profile={0}".format(profile))
        encoding_args.append("--ovcopts-add=level={0}".format(str(level)))
        encoding_args.append("--ovcopts-add=qp={0}".format(comp_level))
    elif encoder.endswith("_qsv"):
        profile = ""
        if encoder == "h264_qsv":
            encoding_args.append("--ovc=h264_qsv")
            profile = "high"
        elif encoder == "hevc_qsv":
            encoding_args.append("--ovc=hevc_qsv")
            profile = "main10"

        if encoder_preset == "ultrafast":
            encoder_preset = "veryfast"
        elif encoder_preset == "veryfast":
            encoder_preset = "faster"
        elif encoder_preset == "veryslow":
            encoder_preset = "slower"

        bf = 6 if len(files) == 1 else 8

        encoding_args.append("--ovcopts-add=preset={0}".format(encoder_preset))
        encoding_args.append("--ovcopts-add=level={0}".format(str(level)))
        encoding_args.append("--ovcopts-add=profile={0}".format(profile))
        encoding_args.append("--ovcopts-add=bf={0}".format(bf))
        encoding_args.append("--ovcopts-add=global_quality={0}".format(comp_level))
    elif encoder == "cpu_av1":
        encoding_args.append("--ovc=libsvtav1")
        # TODO: Really bad way of doing preset. Needs improvement.
        preset = max(0, min(8, 1 + (len(encoder_presets) - encoder_presets.index(encoder_preset))))
        encoding_args.append("--ovcopts-add=rc=cqp")
        encoding_args.append("--ovcopts-add=la_depth={0}".format(32))
        encoding_args.append("--ovcopts-add=preset={0}".format(preset))
        encoding_args.append("--ovcopts-add=qp={0}".format(comp_level))

    successful_encodes = {}
    if len(files) == 1:
        # No need to remove audio and subs for a single file
        # since it is done prior in the shader function
        return_code = -1
        try:
            return_code = subprocess.call(
                encoding_args + ['--o=' + outname, "temp.mkv"]
            )
        except KeyboardInterrupt:
            handle_encoding_cancellation(files[0], outname, start_time,
                                         exit_on_cancel)
            return successful_encodes
        print("End time: " + current_date())
        os.remove("temp.mkv")
        print()
        if return_code == 0:
            successful_encodes[files[0]] = outname
            print("Successfully encoded file to: {0}".format(outname))
        else:
            print("Failed to encode file={0} to output={1}".format(
                files[0], outname))
            print("mpv/ffmpeg exited with code={0}".format(return_code))
    else:
        i = 0
        failed_files = []
        for f in files:
            name = f.split("/")
            name = name[len(name) - 1]
            remove_audio_and_subs(f, softsubs, softaudio)
            if not debug:
                clear()
            else:
                print()
            print("Encoded files:\n {0}".format("\n ".join(
                [os.path.basename(successful_encode) for successful_encode in
                 successful_encodes.keys()]
            )))
            print()
            print("Remaining files:\n {0}".format("\n ".join(
                [
                    os.path.basename(item) for item in files
                    if
                    item not in failed_files and item not in successful_encodes
                ]
            )))
            print()
            print("Start time: {0}".format(start_time))
            print("Start time for file={0}: {1}".format(str(i + 1),
                                                        current_date()))

            raw_name = os.path.splitext(name)[0]
            return_code = -1
            output_path = os.path.join(outname, raw_name + ".mkv")
            try:
                return_code = subprocess.call(encoding_args + [
                    '--o=' + output_path,
                    "temp.mkv"
                ])
            except KeyboardInterrupt:
                handle_encoding_cancellation(f, output_path, start_time,
                                             exit_on_cancel)
                return successful_encodes

            if return_code != 0:
                failed_files.append(f)
            else:
                successful_encodes[f] = output_path
            print("End time for file={0}: {1}".format(str(i + 1),
                                                      current_date()))
            os.remove("temp.mkv")
            if not debug:
                clear()
            i = i + 1
        print()
        print("Files: {0}".format(files_string))
        print("Start time: {0}".format(start_time))
        print("End time: {0}".format(current_date()))
        if len(failed_files) > 0:
            print("Failed to encode files: {0}".format(
                ", ".join(failed_files)))
        else:
            print(
                "Encoded all {0} files successfully.".format(str(len(files))))
    return successful_encodes
