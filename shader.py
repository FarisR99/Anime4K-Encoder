import glob
import os
import subprocess
import sys

from simple_term_menu import TerminalMenu

from consts import *
from utils import current_date, clear


# Menus

def menu_fhd_shaders(shader_path: str, skip_menus: dict) -> str:
    """
    Select a shader for FHD or higher resolution videos.

    Args:
        shader_path: path the shaders are located at
        skip_menus: menu skipping options passed from command line

    Returns:
        Shader string with selected shaders
    """

    mode_choice = None
    if "shader" in skip_menus and skip_menus['shader'] is not None:
        mode_choice = int(skip_menus['shader'])
        if mode_choice < 0 or mode_choice > 5:
            mode_choice = None
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
            title="Please refer to the Anime4k Wiki for more info and try the\n shaders on mpv beforehand to know what's best for you.\nChoose Shader Preset:"
        )
        mode_choice = mode_menu.show()

        if mode_choice is None:
            print("Canceling")
            sys.exit(-1)

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

def remove_audio_and_subs(fn: str, softsubs: bool, softaudio: bool):
    """
    Remove audio and optionally subtitles from a file.

    Args:
        fn: media file path
        softsubs: true if subtitles should be removed
        softaudio: true if audio should be removed
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
        subprocess.call(args)
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


def shader(fn: "list[str]", width: int, height: int, shader_path: str,
           ten_bit: bool,
           language: str, softsubs: bool, softaudio: bool, skip_menus: dict,
           outname: str) -> dict:
    """
    Select encoding and start the encoding process.

    Args:
        fn: list of input media paths
        width: output width
        height: output height
        shader_path: path the shaders are located at
        ten_bit: true if the input media is a 10 bit source
        language: optional desired audio track language
        softsubs: true if subtitles should be removed
        softaudio: true if audio should be removed
        skip_menus: menu skipping options passed from command line
        outname: output path

    Returns:
        mapping of files that were successfully encoded to their output paths
    """

    if not os.path.isdir(shader_path):
        print("error: shaders directory does not exist at: {0}".format(
            shader_path))
        sys.exit(-2)

    files = []
    for file in fn:
        if os.path.isdir(file):
            for fileInDir in glob.glob(os.path.join(file, "*.mkv")):
                files.append(os.path.join(fileInDir))
            for fileInDir in glob.glob(os.path.join(file, "*.mp4")):
                files.append(os.path.join(fileInDir))
        else:
            files.append(os.path.join(file))
    file_count = len(files)
    if file_count > 1:
        if not os.path.isdir(outname):
            print(
                "error: output path must be a directory when there are more than one input files")
            sys.exit(-2)
    elif file_count == 0:
        print("error: no valid input media files found")
        sys.exit(-2)
    else:
        clear()
        if os.path.isdir(outname):
            outname = os.path.join(outname, "out.mkv")
        remove_audio_and_subs(files[0], softsubs, softaudio)
        clear()

    # Select encoder
    codec = ""
    encoder = ""

    if "encoder" in skip_menus and skip_menus['encoder'] is not None:
        encoder = skip_menus['encoder']
        if encoder != 'cpu' and encoder != 'nvenc' and encoder != 'amf':
            print("Unsupported encoder: {0}".format(encoder))
            sys.exit(-2)
    if "codec" in skip_menus and skip_menus['codec'] is not None:
        codec = skip_menus['codec']
        if codec == 'x264':
            codec = 'h264'
            encoder = 'cpu'
        elif codec == 'x265':
            codec = 'hevc'
            encoder = 'cpu'
        elif codec == 'h265':
            codec = 'hevc'
        if codec != 'h264' and codec != 'hevc':
            print("Unsupported codec={0}".format(encoder))
            sys.exit(-2)
    if codec == "" or encoder == "":
        cg_menu = TerminalMenu(
            [
                "CPU X264 (Medium Quality/Size ratio, Fast)",
                "CPU X265 (High Quality/Size ratio, Slow)",
                "NVIDIA GPU H264 (NVENC)",
                "NVIDIA GPU HEVC (NVENC)",
                "AMD GPU H264 (AMF)",
                "AMD GPU HEVC (AMF)"
            ],
            title="Choose Video Codec:"
        )
        cg_choice = cg_menu.show()
        if cg_choice == 0:
            codec = "h264"
            encoder = "cpu"
        elif cg_choice == 1:
            codec = "hevc"
            encoder = "cpu"
        elif cg_choice == 2:
            codec = "h264"
            encoder = "nvenc"
        elif cg_choice == 3:
            codec = "hevc"
            encoder = "nvenc"
        elif cg_choice == 4:
            codec = "h264"
            encoder = "amf"
        elif cg_choice == 5:
            codec = "hevc"
            encoder = "amf"
        else:
            print("Cancel")
            sys.exit(-2)

    return start_encoding(codec, encoder, width, height, shader_path, ten_bit,
                          language, softsubs, softaudio, skip_menus, outname,
                          files)


def handle_encoding_cancellation(file_name: str, output_file, start_time: str):
    """
    Handle cancellation during encoding

    Args:
        file_name: The current file being encoded
        output_file: The output file to delete
        start_time: The time the first file began encoding
    """

    print("Cancelled encoding of file={0}".format(file_name))
    print("Start time: {0}".format(start_time))
    print("End time: " + current_date())
    print()
    print("Deleting temporary files...")
    shader_cleanup()
    if output_file is not None:
        os.remove(output_file)
    print("Exiting program...")
    try:
        sys.exit(-1)
    except SystemExit:
        os._exit(-1)


def start_encoding(codec: str, encoder: str, width: int, height: int,
                   shader_path: str, ten_bit: bool, language: str,
                   softsubs: bool, softaudio: bool, skip_menus: dict,
                   outname: str, files: "list[str]") -> dict:
    """
    Start the encoding of input file(s) to the specified encoding using the CPU.

    Args:
        codec: h264/hevc
        encoder: cpu/nvenc/amf
        width: output width
        height: output height
        shader_path: path the shaders are located at
        ten_bit: true if the input media is a 10 bit source
        language: optional desired audio track language
        softsubs: true if subtitles should be removed
        softaudio: true if audio should be removed
        skip_menus: menu skipping options passed from command line
        outname: output path
        files: list of input media file paths

    Returns:
        mapping of files that were successfully encoded to their output paths
    """

    clear()

    if ten_bit:
        format = "yuv420p10le"
    else:
        format = "yuv420p"
    # AMD GPU Encoding only supports "vaapi_vld"
    # I can't seem to find what this actually is.
    if encoder == "amf":
        format = "vaapi_vld"

    # Open shaders menu
    str_shaders = menu_fhd_shaders(shader_path, skip_menus)
    clear()

    # Select Codec Presets
    if encoder == "cpu" or encoder == "nvenc":
        codec_presets = []
        if encoder == "cpu":
            codec_presets = [
                "ultrafast", "veryfast", "fast", "medium", "slow", "veryslow"
            ]
        elif encoder == "nvenc":
            codec_presets = ["fast", "medium", "slow", "lossless"]
        codec_preset = None
        if "preset" in skip_menus and skip_menus['preset'] is not None:
            codec_preset = skip_menus['preset']
            if codec_preset not in codec_presets:
                codec_preset = None
        if codec_preset is None:
            selected_codec_preset = TerminalMenu(codec_presets,
                                                 title="Choose Encoder Preset:").show()
            if selected_codec_preset is None:
                print("Cancelled")
                sys.exit(-1)
            codec_preset = codec_presets[selected_codec_preset]

    comp_level = ""
    if encoder == "cpu":
        if "crf" in skip_menus and skip_menus['crf'] is not None:
            crf = int(skip_menus['crf'])
            if 0 <= crf <= 51:
                comp_level = str(crf)
            else:
                comp_level = "23"
                print("Invalid crf provided, using default crf={0}".format(
                    comp_level))
        else:
            comp_level = input(
                "Insert compression factor (CRF) 0-51\n0 = Lossless | 23 = Default | 51 = Highest compression\n"
            )
            if comp_level == "" or comp_level is None:
                comp_level = "23"
    elif encoder == "nvenc" or encoder == "amf":
        if "qp" in skip_menus and skip_menus['qp'] is not None:
            qp = int(skip_menus['qp'])
            if 0 <= qp <= 51:
                comp_level = str(qp)
            else:
                comp_level = "24"
                print("Invalid qp provided, using default qp={0}".format(
                    comp_level))
        else:
            comp_level = input(
                "Insert Quantization Parameter (QP) 0-51\n0 = Lossless | 24 = Default | 51 = Highest compression\n"
            )
            if comp_level == "" or comp_level is None:
                comp_level = "24"

    # Print Info
    files_string = ", ".join(files)
    print("Files: {0}".format(files_string))
    print("Using the following shaders:")
    print(str_shaders)
    if encoder == "cpu":
        print("Encoding with preset: {0} crf={1}".format(codec_preset,
                                                         comp_level))
    elif encoder == "nvenc":
        print("Encoding with preset: {0} qp={1}".format(codec_preset,
                                                        comp_level))
    elif encoder == "amf":
        print("Encoding with preset: qp={0}".format(comp_level))
    start_time = current_date()
    print("Start time: " + start_time)
    import time
    time.sleep(3)
    clear()

    # Encode
    encoding_args = [
        "mpv",
        "--vf=format=" + format,
        "--profile=gpu-hq",
        "--scale=ewa_lanczossharp",
        "--cscale=ewa_lanczossharp",
        "--video-sync=display-resample",
        "--interpolation",
        "--tscale=oversample",
        '--vf-pre=sub',
        '--vf=gpu=w=' + str(width) + ':h=' + str(height),
        "--glsl-shaders=" + str_shaders,
        "--oac=libopus",
        "--oacopts=b=192k",
    ]
    if language is not None and language != "":
        encoding_args.append("--alang=" + str(language))

    # Arguments specific to the encoding and encoder specified
    if encoder == "cpu":
        bf = 8
        if len(files) == 1:
            bf = 6

        if codec == "h264":
            encoding_args.append("--ovc=libx264")
        elif codec == "hevc":
            encoding_args.append("--ovc=libx265")
        else:
            print("ERROR: Unknown codec: {0}".format(codec))
            sys.exit(-2)

        encoding_args.append(
            '--ovcopts=preset=' + codec_preset + ',level=5.1,crf=' + str(
                comp_level) + ',aq-mode=3,psy-rd=1.0,bf=' + str(bf))
    elif encoder == "nvenc":
        encoding_args.append("--vo=gpu")

        if codec == "h264":
            encoding_args.append("--ovc=h264_nvenc")
            encoding_args.append(
                '--ovcopts=rc=constqp,preset=' + codec_preset +
                ',profile=high,level=5.1,rc-lookahead=32,qp=' + str(comp_level)
            )
        elif codec == "hevc":
            encoding_args.append("--ovc=hevc_nvenc")
            encoding_args.append(
                '--ovcopts=rc=constqp,preset=' + codec_preset +
                ',profile=main10,rc-lookahead=32,qp=' + str(comp_level)
            )
    elif encoder == "amf":
        encoding_args.append("--vo=gpu")

        profile = ""
        if codec == "h264":
            encoding_args.append("--ovc=h264_vaapi")
            profile = "high"
        elif codec == "hevc":
            encoding_args.append("--ovc=hevc_vaapi")
            profile = "main10"
        encoding_args.append(
            '--ovcopts=rc_mode=cqp,profile=' + profile + ',level=5.1,qp='
            + str(comp_level))

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
            handle_encoding_cancellation(files[0], outname, start_time)
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
            clear()
            print("Files: {0}".format(files_string))
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
                handle_encoding_cancellation(f, output_path, start_time)
            if return_code != 0:
                failed_files.append(f)
            else:
                successful_encodes[f] = output_path
            print("End time for file={0}: {1}".format(str(i + 1),
                                                      current_date()))
            os.remove("temp.mkv")
            clear()
            i = i + 1
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
