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
    Select a shader

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
        title="Please refer to the Anime4k Wiki for more info\nand try the shaders on mpv beforehand to know what's best for you.\nChoose Shader Preset:"
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
        title="Choose your video codec."
    )
    cg_choice = cg_menu.show()
    if cg_choice == 0:
        cpu_h264_shader(fn, width, height, shader_path, ten_bit, softsubs,
                        outname,
                        files=files)
    elif cg_choice == 1:
        cpu_hevc_shader(fn, width, height, shader_path, ten_bit, softsubs,
                        outname,
                        files=files)
    else:
        print("Cancel")
        sys.exit(-2)

    # Delete temp.mkv
    if os.path.isdir(fn):
        os.remove("temp.mkv")
    else:
        os.remove(fn)


def cpu_h264_shader(fn: str, width: int, height: int, shader_path: str,
                    ten_bit: bool, softsubs: bool, outname: str,
                    files: list[str] = []):
    """
    Start the encoding of input file(s) to H264.

    Args:
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

    # Detect width and height of input video.
    if len(files) == 0:
        _m = MediaInfo.parse(fn)
    else:
        _m = MediaInfo.parse(files[0])
    track_width = -1
    for t in _m.tracks:
        if t.track_type == 'Video':
            track_width = t.width
            str_shaders = menu_fhd_shaders(shader_path)
    clear()

    # Select Codec Presets
    encoder_preset = [
        "veryfast", "fast", "medium", "slow", "veryslow"
    ]
    codec_preset = encoder_preset[
        TerminalMenu(encoder_preset,
                     title="Choose your encoder preset:").show()
    ]

    crf = input(
        "Insert compression factor (CRF) 0-51\n0 = Lossless | 23 = Default | 51 = Highest compression\n"
    )

    # Print Info
    print("File: " + fn)
    print("Using the following shaders:")
    print(str_shaders)
    print("Encoding with preset: " + codec_preset + " crf=" + crf)
    import time
    time.sleep(3)
    # clear()

    # Encode
    if len(files) == 0:
        subprocess.call([
            "mpv",
            "--vf=format=" + format,
            fn,
            "--profile=gpu-hq",
            "--scale=ewa_lanczossharp",
            "--cscale=ewa_lanczossharp",
            "--video-sync=display-resample",
            "--interpolation",
            "--tscale=oversample",
            '--vf=gpu=w=' + str(width) + ':h=' + str(height),
            "--glsl-shaders=" + str_shaders,
            "--oac=libopus",
            "--oacopts=b=192k",
            "--ovc=libx264",
            '--ovcopts=preset=' + codec_preset + ',level=6.1,crf=' + str(
                crf) + ',aq-mode=3,psy-rd=1.0,bf=6',
            '--vf-pre=sub',
            '--o=' + outname
        ])
    else:
        i = 0
        for f in files:
            remove_audio_and_subs(f, softsubs)
            clear()
            name = f.split("/")
            name = name[len(name) - 1]
            subprocess.call([
                "mpv",
                "--vf=format=" + format,
                "temp.mkv",
                "--profile=gpu-hq",
                "--scale=ewa_lanczossharp",
                "--cscale=ewa_lanczossharp",
                "--video-sync=display-resample",
                "--interpolation",
                "--tscale=oversample",
                '--vf=gpu=w=' + str(width) + ':h=' + str(height),
                "--glsl-shaders=" + str_shaders,
                "--oac=libopus",
                "--oacopts=b=192k",
                "--ovc=libx264",
                '--ovcopts=preset=' + codec_preset + ',level=6.1,crf=' + str(
                    crf) + ',aq-mode=3,psy-rd=1.0,bf=8',
                '--vf-pre=sub',
                '--o=' + os.path.join(outname, name)
            ])
            i = i + 1


def cpu_hevc_shader(fn: str, width: int, height: int, shader_path: str,
                    ten_bit: bool, softsubs: bool, outname: str,
                    files: list[str] = []):
    """
    Start the encoding of input file(s) to H265/HEVC.

    Args:
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

    # Detect width and height of input video.
    if len(files) == 0:
        _m = MediaInfo.parse(fn)
    else:
        _m = MediaInfo.parse(files[0])
    track_width = -1
    for t in _m.tracks:
        if t.track_type == 'Video':
            track_width = t.width
            str_shaders = menu_fhd_shaders(shader_path)
    clear()

    # Select Codec Presets
    encoder_preset = [
        "veryfast", "fast", "medium", "slow", "veryslow"
    ]
    codec_preset = encoder_preset[
        TerminalMenu(encoder_preset,
                     title="Choose your encoder preset:").show()
    ]
    crf = input(
        "Insert compression factor (CRF) 0-51\n0 = Lossless | 28 = Default | 51 = Highest compression\n"
    )

    # Print Info
    print("File: " + fn)
    print("Using the following shaders:")
    print(str_shaders)
    print("Encoding with preset: " + codec_preset + " crf=" + crf)
    import time
    time.sleep(3)
    # clear()

    # Encode
    if len(files) == 0:
        subprocess.call([
            "mpv",
            "--vf=format=" + format,
            fn,
            "--profile=gpu-hq",
            "--scale=ewa_lanczossharp",
            "--cscale=ewa_lanczossharp",
            "--video-sync=display-resample",
            "--interpolation",
            "--tscale=oversample",
            '--vf=gpu=w=' + str(width) + ':h=' + str(height),
            "--glsl-shaders=" + str_shaders,
            "--oac=libopus",
            "--oacopts=b=192k",
            "--ovc=libx265",
            '--ovcopts=preset=' + codec_preset + ',level=6.1,crf=' + str(
                crf) + ',aq-mode=3,psy-rd=1.0,bf=6',
            '--vf-pre=sub',
            '--o=' + outname
        ])
    else:
        i = 0
        for f in files:
            remove_audio_and_subs(f, softsubs)
            clear()
            name = f.split("/")
            name = name[len(name) - 1]
            subprocess.call([
                "mpv",
                "--vf=format=" + format,
                "temp.mkv",
                "--profile=gpu-hq",
                "--scale=ewa_lanczossharp",
                "--cscale=ewa_lanczossharp",
                "--video-sync=display-resample",
                "--interpolation",
                "--tscale=oversample",
                '--vf=gpu=w=' + str(width) + ':h=' + str(height),
                "--glsl-shaders=" + str_shaders,
                "--oac=libopus",
                "--oacopts=b=192k",
                "--ovc=libx265",
                '--ovcopts=preset=' + codec_preset + ',level=6.1,crf=' + str(
                    crf) + ',aq-mode=3,psy-rd=1.0,bf=8',
                '--vf-pre=sub',
                '--o=' + os.path.join(outname, name)
            ])
            i = i + 1
