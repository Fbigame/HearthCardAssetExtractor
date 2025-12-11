import argparse
import logging
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from version import __version__
from unity3d.asset_manifest import AssetManifest

__all__ = [
    'parse_args',
    'HearthstoneExtractContext'
]


def configure_logging(output_path, level: str):
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }.get(level, logging.WARNING)
    logging.basicConfig(
        filename=output_path / "log.txt",
        level=level,
        filemode='w',
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_input() -> Path | None:
    if platform.system() != "Windows":
        return None
    # 仅仅当 windows 环境的时候使用 winreg
    import winreg
    try:
        key_path = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Hearthstone"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            install_location, _ = winreg.QueryValueEx(key, "InstallLocation")
            return Path(install_location)
    except (OSError, FileNotFoundError):
        return None


def wrap_parse_list_arg(
        *allow_args: str,
        name: str,
) -> Callable[[str], tuple[str, ...]]:
    def wrap(value: str) -> tuple[str, ...]:
        if not value:
            return tuple()
        args = tuple(strip_id for id in value.split(',') if (strip_id := id.strip()))
        # case none
        if 'none' in args:
            if len(args) > 1:
                raise argparse.ArgumentTypeError('Cannot use "none" with other arguments')
            return tuple()
        # case all
        if 'all' in args:
            if len(args) > 1:
                raise argparse.ArgumentTypeError('Cannot use "all" with other arguments')
            elif allow_args:
                return allow_args
            else:
                raise argparse.ArgumentTypeError(f'"all" is not supported in {name}')
        
        # validate arguments
        if allow_args:
            valid_args = set(allow_args)
            for arg in args:
                if arg not in valid_args:
                    raise argparse.ArgumentTypeError(f'Invalid argument: "{arg}" in {name}')
        return args
    
    return wrap


@dataclass
class HearthstoneExtractContext:
    """Context class for Hearthstone asset extraction"""
    input_path: Path
    output_path: Path
    asset_manifest: AssetManifest
    card_ids: tuple[str, ...]
    image_options: tuple[str, ...]
    audio_options: tuple[str, ...]
    locale_options: tuple[str, ...]
    ensure_ascii: bool
    enable_sub_struct: bool
    no_assets: bool
    merged_struct: bool


def parse_args() -> HearthstoneExtractContext:
    parser = argparse.ArgumentParser(description="Hearthstone card asset extractor")
    
    # Add help and version handling
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    
    # 输入参数
    parser.add_argument(
        "--input",
        type=Path,
        default=(auto_input := get_input()),
        help="Input folder containing Hearthstone assets" + (
            f"(default: {auto_input})" if auto_input else ""
        ),
        required=auto_input is None,
    )
    
    # 输出参数
    parser.add_argument(
        "--output",
        type=Path,
        help="Output folder for extracted assets (default: ./output)",
        default=Path("./output")
    )
    
    # 语言参数
    parser.add_argument(
        "--locale",
        type=wrap_parse_list_arg(*(args := (
            'enus', 'zhcn', 'zhtw', 'jajp',
            'eses', 'kokr', 'ptbr', 'ruru',
            'frfr', 'esmx', 'itit', 'dede',
            'plpl', 'thth',
        )), name='locale'),
        help=f'Language locales to extract: all, {", ".join(args)}, or none (default: none)',
        default="zhcn"
    )
    
    # 卡牌ID参数
    parser.add_argument(
        "--id",
        type=str,
        help="Comma-separated list of card IDs to extract (e.g., HERO_01,HERO_02), or 'all' to extract all cards",
        default="all"
    )
    
    # 图片参数
    parser.add_argument(
        "--image",
        type=wrap_parse_list_arg(*(args := ('normal', 'signature')), name='image'),
        help=f'Image types to extract: all, {", ".join(args)}, or none (default: none)',
        default="none"
    )
    
    # 音频参数
    parser.add_argument(
        "--audio",
        type=wrap_parse_list_arg(*(args := (
            'additional-play', 'attack', 'death', 'lifetime',
            'trigger', 'sub-option', 'reset-game', 'sub-spell', 'emote'
        )), name='audio'),
        help=f'Audio types to extract: all, {", ".join(args)}, or none (default: none)',
        default="none"
    )
    
    # ensure_ascii参数
    parser.add_argument(
        "--ensure_ascii",
        action='store_true',
        help="Ensure ASCII encoding for output (default: false)"
    )
    
    # enable_sub_struct参数
    parser.add_argument(
        "--enable_sub_struct",
        action='store_true',
        help="Control whether to output struct.json in subfolders (default: false).\n"
        "Note: The overall struct.json will always be output in the card_id folder regardless of this setting."
    )
    
    # no_assets参数
    parser.add_argument(
        "--no_assets",
        action='store_true',
        help="Only output struct.json, do not output asset files (default: false)."
    )
    
    # merged_struct参数
    parser.add_argument(
        "--merged_struct",
        action='store_true',
        help="Merge output/{card_id}/struct.json into output/struct.json (default: false).\n"
        "Note: If enable_sub_struct is true, output/{card_id}/struct.json will still be output."
    )
    
    # log_level参数
    parser.add_argument(
        "--log_level",
        type=str,
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='error',
        help="Set the logging level (default: error).\n"
        "Available options: debug, info, warning, error, critical"
    )
    
    # 如果没有传任何参数，打印帮助并退出
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)
    args = parser.parse_args()
    
    if not args.input.exists() or not args.input.is_dir():
        parser.error(f"Input folder '{args.input}' does not exist or is not a directory.")
    
    if not args.audio and not args.image:
        raise argparse.ArgumentTypeError('At least one of --audio or --image must be specified')
    output: Path = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    configure_logging(output, args.log_level)
    return HearthstoneExtractContext(
        input_path=(input_path := args.input.resolve()),
        output_path=output,
        asset_manifest=(asset_manifest := AssetManifest(input_path)),
        image_options=args.image,
        audio_options=args.audio,
        locale_options=args.locale,
        ensure_ascii=args.ensure_ascii,
        enable_sub_struct=args.enable_sub_struct,
        no_assets=args.no_assets,
        merged_struct=args.merged_struct,
        card_ids=(
            tuple(asset_manifest.cards_map.keys())
            if args.id == 'all'
            else tuple(id.strip() for id in args.id.split(",") if id.strip())
        ),
    )
