import os
from datetime import datetime
from shutil import which

__current_version__ = '1.1.2'


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
    Returns:
        true if the specified tool name is installed
    """
    return which(name) is not None


def current_date() -> str:
    """
    Returns:
        the current date in the format: YYYY-MM-dd HH-MM-SS
    """
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def lang_long_to_short(lang: str) -> str:
    if lang in reversed_lang_mapping:
        return reversed_lang_mapping[lang]
    else:
        return "und"


def lang_short_to_long(lang: str) -> str:
    if lang in language_mapping:
        return language_mapping[lang]
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
    "por": "Portuguese",
    "spa": "Spanish",
    "ita": "Italian",
    "pol": "Polish",
    "hin": "Hindi",
    "chi": "Chinese"
}

reversed_lang_mapping = {
    "English": "eng",
    "Japanese": "jpn",
    "German": "ger",
    "Korean": "kor",
    "Portuguese": "por",
    "Spanish": "spa",
    "Italian": "ita",
    "Polish": "pol",
    "Hindi": "hin",
    "Chinese": "chi"
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


def str2dict(v) -> dict:
    if v is None:
        return {}
    if isinstance(v, dict):
        return v
    v = str(v)
    dictionary = {}
    for entry in v.split(","):
        if "=" not in entry:
            raise argparse.ArgumentTypeError(
                'Invalid entry, must follow key=value')
        entry_split = entry.split("=")
        dictionary[entry_split[0]] = entry_split[1]
    return dictionary
