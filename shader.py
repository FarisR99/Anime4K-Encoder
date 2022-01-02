import glob
import os
import subprocess
import sys

from pymediainfo import MediaInfo
from simple_term_menu import TerminalMenu

from consts import *
from utils import clear


# Menus

def menu_fhd_shaders(shader_path: str) -> str:
    """
    Select a shader for FHD or higher resolution videos.

    Args:
        shader_path: path the shaders are located at

    Returns:
        Shader string with selected shaders
    """

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
           softsubs: bool, outname: str):
    """
    Select encoding and start the encoding process.

    Args:
        fn: input media path
        width: output width
        height: output height
        shader_path: path the shaders are located at
        ten_bit: true if the input media is a 10 bit source
        softsubs: true if audio and subtitles should be removed
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
        remove_audio_and_subs(fn, softsubs)
        fn = "temp.mkv"
        clear()

    # Select encoder
    cg_menu = TerminalMenu(
        [
            "X264 (Medium Quality/Size ratio, Fast)",
            "X265 (High Quality/Size ratio, Slow)"
        ],
        title="Choose Video Codec:"
    )
    cg_choice = cg_menu.show()
    if cg_choice == 0:
        cpu_shader("h264", fn, width, height, shader_path, ten_bit, softsubs,
                   outname, files)
    elif cg_choice == 1:
        cpu_shader("hevc", fn, width, height, shader_path, ten_bit, softsubs,
                   outname, files)
    else:
        print("Cancel")
        sys.exit(-2)

    # Delete temp.mkv
    if os.path.isdir(fn):
        os.remove("temp.mkv")
    else:
        os.remove(fn)


def cpu_shader(encoding: str, fn: str, width: int, height: int,
               shader_path: str,
               ten_bit: bool, softsubs: bool, outname: str,
               files):
    """
    Start the encoding of input file(s) to the specified encoding.

    Args:
        encoding: h264/hevc
        fn: input media path
        width: output width
        height: output height
        shader_path: path the shaders are located at
        ten_bit: true if the input media is a 10 bit source
        softsubs: true if audio and subtitles should be removed
        outname: output path
        files: list of input media file paths, empty if only one
    """

    clear()

    if ten_bit:
        format = "yuv420p10le"
    else:
        format = "yuv420p"

    # Open shaders menu
    str_shaders = menu_fhd_shaders(shader_path)
    clear()

    # Select Codec Presets
    encoder_preset = [
        "ultrafast", "veryfast", "fast", "medium", "slow", "veryslow"
    ]
    codec_preset = encoder_preset[
        TerminalMenu(encoder_preset,
                     title="Choose Encoder Preset:").show()
    ]

    crf = input(
        "Insert compression factor (CRF) 0-51\n0 = Lossless | 23 = Default | 51 = Highest compression\n"
    )
    if crf == "" or crf is None:
        crf = "23"

    # Print Info
    print("File: " + fn)
    print("Using the following shaders:")
    print(str_shaders)
    print("Encoding with preset: " + codec_preset + " crf=" + crf)
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

    bf = 8
    if len(files) == 0:
        bf = 6

    # Arguments specific to the encoding specified
    if encoding == "h264":
        encoding_args.append("--ovc=libx264")
    elif encoding == "hevc":
        encoding_args.append("--ovc=libx265")
    else:
        print("ERROR: Unknown encoding " + encoding)
        sys.exit(-2)

    encoding_args.append(
        '--ovcopts=preset=' + codec_preset + ',level=5.1,crf=' + str(
            crf) + ',aq-mode=3,psy-rd=1.0,bf=' + str(bf))

    if len(files) == 0:
        subprocess.call(encoding_args + ['--o=' + outname, fn])
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
            i = i + 1
