![Logo of the project](demo.gif)

# Anime4K-Encoder

> Wrapper for [Anime4K](https://github.com/bloc97/Anime4K)

Makes it easy to encode anime using the MPV shaders with predefined encoding
profiles!

## Features

* Encode videos with Anime4K shaders easily
* Encode using x264, x265, NVIDIA NVENC or AMD AMF
* Extract audio and subtitles automatically
* Predefined profiles for Anime4K and ffmpeg

## Key differences to Anime4K-Encoder-4.0.1-

[Anime4K-Encoder-4.0.1-](https://github.com/Secksdendfordff/Anime4K-Encoder-4.0.1-)
is a repository based
on [Anime4K-PyWrapper](https://github.com/ThoughtfulDev/Anime4K) that updates
the [Anime4K](https://github.com/bloc97/Anime4K) shaders used and other
changes. The key differences between Anime4K-Encode-4.0.1 and this repository
are:

- Cleaned up code
- Re-added NVENC support and added CPU AV1, AMD GPU and Intel QuickSync support
- Re-added 10-bit toggling support
- Removed official support for videos with a resolution lower than FHD
- Added support for MP4 files
- Ability to choose to manually mux subtitles and audio via `--softsubs`
  and `--softaudio`. You can also use `-m multi` which will apply mode shaders
  with `--softsubs` and `--softaudio`, audio, subs and mux all at once.
- Ability to skip menus in shader mode via `--skip_menus`
- Added support for multiple `--input` arguments
- Use default values for some arguments

## Installing / Getting started

What you need:

- Linux
- Python 3.X
- mpv > 0.32
- ffmpeg
- mkvnixtool (e.g mkvtoolnix on Ubuntu)
- A dedicated GPU (no VM) [AMD/NVIDIA/Intel]

You can skip installing the necessary python libs and the initial configuration
by running `setup.sh`.

**Installing the necessary python libs**

```
pip3 install -r requirements.txt
```

### Initial Configuration

Download the latest shaders
from [here](https://github.com/bloc97/Anime4K/releases). Put them all into one
folder, for example called *shaders*

### Burning in subs

If there's a default sub track, it will be burned in automatically. If you want
to add softsubs, you will have to run the script with `--no_subtitles` and add
them later.

This can also fix some audio problems that you may encounter during encoding,
which may or may not slow down your encoding progress.

### Upscaling your first Anime!

Assuming your Anime Movie/Episode is called *input.mkv* and has a resolution of
1920x1080, and you want to upscale it to 4K (3840x2160), here are the commands
you would run:

1. Encode the video with the following command

```
python3 Anime4K.py -m shader --shader_dir "./shaders" --width 3840 --height 2160 -i input.mkv -o video_upscale.mkv
```

Note: Width and height arguments are optional as they default to 3840x2160. The
mode argument is also optional as it defaults to shader.

2. Follow the dialogues - they should be pretty self-explanatory
4. Your file should now be in *video_upscale.mkv*
5. Done!

### Burning softsubs/softaudio

1. Extract the audio and/or subtitles from the original file

```
python3 Anime4K.py -m audio -i input.mkv
python3 Anime4K.py -m subs -i input.mkv
```

Now we have the audio files and subtitles in the current folder.

2. Add them into the final output
3. Done!

```
python3 Anime4K.py -m mux -i video_upscale.mkv -o video_upscaled_with_audio_and_subs.mkv
```

**Feel free to explore the other options of the program (or profiles) by
typing**:

```
python3 Anime4K.py --help
```

### GPU Encoding

#### NVENC

NVENC support has been re-added as Ampere NVENC is pretty good in my experience
with an RTX 3090. I would not recommend using this on 10-series cards or older.
<br/><b>Note</b>: Whilst H264 NVENC will use level 5.1, running mpv/ffmpeg
using HEVC NVENC throws an error if a level is specified, and therefore the
default is used. On my system and I'd assume most systems, this is 6.2.

Requirements:

- Latest NVIDIA driver
- Type `ffmpeg` and ensure ffmpeg has been built with `--enable-nvenc`. If not, manually compile ffmpeg
  with [these]((https://docs.nvidia.com/video-technologies/video-codec-sdk/ffmpeg-with-nvidia-gpu/#compiling-for-linux))
  instructions
- May
  need [cuda](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#verify-you-have-cuda-enabled-system)
  installed

#### AMD GPUs

I've added support for AMD GPUs using VAAPI. This requires AMD drivers. I do not know how this encoder works nor have I
tested it, so the code implementation is based on online (lack of) documentation. Feel free to raise an Issue ticket on
GitHub if there are errors, however I cannot fix it myself.

#### Intel QuickSync

Intel QuickSync is supported, but requires the desired FPS to be set. It's also very slow and is best for 1080p or
lower.

## **[Optional]** Encoding ffmpeg progressbar

To get an overview of your current encoding of ffmpeg, you may install
the [ffmpeg-progressbar-cli](https://github.com/sidneys/ffmpeg-progressbar-cli)

```
npm install --global ffmpeg-progressbar-cli
```

*Don't worry, the script will also work with normal ffmpeg.*

## Misc

This is a list of things that the creators of the repositories that this
repository is a fork of have encountered but it may or may not be true for
every user:

- The shader mode affects the encoding speed, from faster to slower C > B > A >
  C+A > B+B > A+A.
- The encoding preset doesn't noticeably affect the encoding speed (only tested
  from fastest to medium)

The best way to use the shaders is in real time, its intended purpose. The
purpose of this program is for those that can't run the HQ version of the
shader (the one this one uses) in real time, or to use them for later (
Phone, streaming server, etc). This encoding process can take hours or even
days for episodes and movies.

### Examples

Please view the examples in a new tab/in large to compare.

#### Fate/stay night: Heaven's Feel III

Input - 1080p - 45Mbps bitrate:

![1080p](../media/example-original.png?raw=true)

Output - 4K - 180Mbps bitrate - NVENC H264 Medium - Shaders mode B+B:

![2160p](../media/example-upscaled.png?raw=true)

Upscaling this movie from 1080p to 4K with a constant bitrate of ~45Mbps using
NVENC H264 Fast (Shaders mode B+B) took roughly 2hrs 50 minutes.

## TODO

- Adding extra shaders that are not included in the [Modes] by default (Darken,
  Thin, Etc)

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Links

- Related projects:
    - [Anime4K](https://github.com/bloc97/Anime4K)
    - [ThoughtfulDev](https://github.com/ThoughtfulDev/Anime4K)
    - [video2x](https://github.com/k4yt3x/video2x)
    - [Anime4K-Encoder-4.0.1-](https://github.com/Secksdendfordff/Anime4K-Encoder-4.0.1-)

- Thanks to:
    - [ffmpeg-progressbar-cli](https://github.com/sidneys/ffmpeg-progressbar-cli)
    - [simple-term-menu](https://github.com/IngoHeimbach/simple-term-menu)

## Licensing

The code in this project is licensed under GNU GENERAL PUBLIC LICENSE.
