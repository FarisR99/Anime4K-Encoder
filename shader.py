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

    if skip_menus['shader'] is not None:
        mode_choice = int(skip_menus['shader'])
    else:
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

def remove_audio_and_subs(fn: str, softsubs: bool):
    """
    Remove audio and optionally subtitles from a file.

    Args:
        fn: media file path
        softsubs: true if audio and subtitles should be removed
    """

    args = [
        "mkvmerge",
        "-o",
        "temp.mkv"
    ]
    if softsubs:
        args.append("--no-subtitles")
        args.append("--no-audio")
    args.append(fn)

    subprocess.call(args)


def shader(fn: str, width: int, height: int, shader_path: str, ten_bit: bool,
           softsubs: bool, skip_menus: dict, outname: str):
    """
    Select encoding and start the encoding process.

    Args:
        fn: input media path
        width: output width
        height: output height
        shader_path: path the shaders are located at
        ten_bit: true if the input media is a 10 bit source
        softsubs: true if audio and subtitles should be removed
        skip_menus: menu skipping options passed from command line
        outname: output path
    """

    if not os.path.isdir(shader_path):
        print("Shaders directory does not exist at: " + shader_path)
        sys.exit(-2)

    # Create temp.mkv if input path is a single file
    clear()
    files = []
    if os.path.isdir(fn):
        for file in glob.glob(os.path.join(fn, "*.mkv")):
            files.append(os.path.join(file))
    else:
        if fn != "temp.mkv":
            remove_audio_and_subs(fn, softsubs)
            fn = "temp.mkv"
        clear()

    # Select encoder
    codec = ""
    encoder = ""

    if skip_menus['encoder'] is not None:
        encoder = skip_menus['encoder']
        if encoder != 'cpu' and encoder != 'nvenc':
            print("Unsupported encoder={0}".format(encoder))
            sys.exit(-2)
    if skip_menus['codec'] is not None:
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
                "GPU H264 NVENC",
                "GPU HEVC NVENC"
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
        else:
            print("Cancel")
            sys.exit(-2)

    start_encoding(codec, encoder, fn, width, height, shader_path, ten_bit,
                   softsubs, skip_menus, outname, files)

    # Delete temp.mkv
    if os.path.isdir(fn):
        os.remove("temp.mkv")
    else:
        os.remove(fn)


def start_encoding(codec: str, encoder: str, fn: str, width: int, height: int,
                   shader_path: str, ten_bit: bool, softsubs: bool,
                   skip_menus: dict, outname: str, files):
    """
    Start the encoding of input file(s) to the specified encoding using the CPU.

    Args:
        codec: h264/hevc
        encoder: cpu/nvenc
        fn: input media path
        width: output width
        height: output height
        shader_path: path the shaders are located at
        ten_bit: true if the input media is a 10 bit source
        softsubs: true if audio and subtitles should be removed
        skip_menus: menu skipping options passed from command line
        outname: output path
        files: list of input media file paths, empty if only one
    """

    clear()

    if ten_bit:
        format = "yuv420p10le"
    else:
        format = "yuv420p"

    # Open shaders menu
    str_shaders = menu_fhd_shaders(shader_path, skip_menus)
    clear()

    # Select Codec Presets
    if encoder == "cpu":
        codec_presets = [
            "ultrafast", "veryfast", "fast", "medium", "slow", "veryslow"
        ]
    elif encoder == "nvenc":
        codec_presets = ["fast", "medium", "slow", "lossless"]
    else:
        print("ERROR: Unknown encoder " + encoder)
        sys.exit(-2)

    codec_preset = codec_presets[
        TerminalMenu(codec_presets,
                     title="Choose Encoder Preset:").show()
    ]

    comp_level = ""
    if encoder == "cpu":
        if skip_menus['crf'] is not None:
            crf = int(skip_menus['crf'])
            if 0 <= crf <= 51:
                comp_level = str(crf)
            else:
                comp_level = "23"
        else:
            comp_level = input(
                "Insert compression factor (CRF) 0-51\n0 = Lossless | 23 = Default | 51 = Highest compression\n"
            )
            if comp_level == "" or comp_level is None:
                comp_level = "23"
    elif encoder == "nvenc":
        if skip_menus['qp'] is not None:
            qp = int(skip_menus['qp'])
            if 0 <= qp <= 51:
                comp_level = str(qp)
            else:
                comp_level = "24"
        else:
            comp_level = input(
                "Insert Quantization Parameter (QP) 0-51\n0 = Lossless | 24 = Default | 51 = Highest compression\n"
            )
            if comp_level == "" or comp_level is None:
                comp_level = "24"

    # Print Info
    print("File: " + fn)
    print("Using the following shaders:")
    print(str_shaders)
    if encoder == "cpu":
        print("Encoding with preset: {0} crf={1}".format(codec_preset, comp_level))
    elif encoder == "nvenc":
        print("Encoding with preset: {0} qp={1}".format(codec_preset, comp_level))
    print("Start time: " + current_date())
    import time
    time.sleep(3)
    # clear()

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

    # Arguments specific to the encoding and encoder specified
    if encoder == "cpu":
        bf = 8
        if len(files) == 0:
            bf = 6

        if codec == "h264":
            encoding_args.append("--ovc=libx264")
        elif codec == "hevc":
            encoding_args.append("--ovc=libx265")
        else:
            print("ERROR: Unknown codec={0}".format(codec))
            sys.exit(-2)

        encoding_args.append(
            '--ovcopts=preset=' + codec_preset + ',level=5.1,crf=' + str(
                comp_level) + ',aq-mode=3,psy-rd=1.0,bf=' + str(bf))
    elif encoder == "nvenc":
        encoding_args.append("--vo=gpu")

        profile = ""
        if codec == "h264":
            encoding_args.append("--ovc=h264_nvenc")
            profile = "high"
        elif codec == "hevc":
            encoding_args.append("--ovc=hevc_nvenc")
            profile = "main10"
        encoding_args.append(
            '--ovcopts=rc=constqp,preset=' + codec_preset + ',profile='
            + profile + ',level=5.1,rc-lookahead=32,qp=' + str(comp_level))

    if len(files) == 0:
        subprocess.call(encoding_args + ['--o=' + outname, fn])
        print("End time: " + current_date())
    else:
        i = 0
        for f in files:
            remove_audio_and_subs(f, softsubs)
            clear()
            name = f.split("/")
            name = name[len(name) - 1]
            subprocess.call(
                encoding_args + [
                    '--o=' + os.path.join(outname, name) + outname,
                    "temp.mkv"])
            subprocess.call(encoding_args)
            print("End time for file=" + str(i + 1) + ": " + current_date())
            i = i + 1
        print("End time: " + current_date())
