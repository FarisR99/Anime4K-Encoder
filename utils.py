import os
from shutil import which

__current_version__ = '1.0.0-SNAPSHOT'


def credz():
    """
    Print credits
    """
    print("___________________________________")
    print("   _        _           _ _  _  __")
    print("  /_\  _ _ (_)_ __  ___| | || |/ /")
    print(" / _ \| ' \| | '  \/ -_)_  _| ' < ")
    print("/_/ \_\_||_|_|_|_|_\___| |_||_|\_\\")
    print("___________________________________")
    print("   Upscale your favorite anime!    ")
    print("       Made by ThoughtfulDev       ")
    print("    Updated by Secksdendfordff     ")
    print("          and KingFaris10          ")
    print("\n")


def is_tool(name: str) -> bool:
    """
    Check if the specified name is installed
    """
    return which(name) is not None


def lang_long_to_short(lang: str) -> str:
    if lang == 'English':
        return "eng"
    elif lang == 'Japanese':
        return "jpn"
    elif lang == 'German':
        return "ger"
    elif lang == 'Korean':
        return "kor"
    else:
        return "und"


def lang_short_to_long(lang: str) -> str:
    if lang == "eng":
        return "English"
    elif lang == "jpn" or lang == "jap" or lang == "ja":
        return "Japanese"
    elif lang == "fra":
        return "French"
    elif lang == "ger":
        return "German"
    elif lang == "kor":
        return "Korean"
    else:
        return "Unknown"


language_mapping = {
    "eng": "English",
    "ja": "Japanese",
    "jp": "Japanese",
    "jap": "Japanese",
    "jpn": "Japanese",
    "ger": "German",
    "kor": "Korean",
}


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def str2bool(v) -> bool:
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
