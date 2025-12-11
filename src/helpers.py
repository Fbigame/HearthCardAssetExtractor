import csv
import logging
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

from unity3d import AssetManifest


@dataclass
class CardContext:
    input: Path
    output: Path
    asset_manifest: AssetManifest
    locale_options: tuple[str, ...]
    card_id: str
    ensure_ascii: bool
    enable_sub_struct: bool
    no_assets: bool
    merged_struct: bool
    gameplay_audio: dict[str, dict[str, str]] | None = None


@lru_cache(maxsize=1)
def load_emote_type(input_path: Path):
    import pythonnet
    pythonnet.load()
    # 导入C#环境
    import System  # noqa
    import System.Reflection as SR  # noqa
    asm = SR.Assembly.LoadFile((input_path / r"Hearthstone_Data\Managed\Assembly-CSharp.dll").as_posix())
    name = 'EmoteType'
    enum_type = asm.GetType(name)
    if enum_type is None:
        raise ValueError(f"Enum '{name}' not found in DLL")
    
    names = System.Enum.GetNames(enum_type)
    values = [System.Enum.Parse(enum_type, n).value__ for n in names]
    
    return {v: n for n, v in zip(names, values)}


@lru_cache(maxsize=1)
def load_strings_gameplay_audio(input_path: Path, locales: Sequence[str]):
    result = {}
    
    for locale in locales:
        path = input_path / 'Strings' / f'{locale[:2]}{locale[-2:].upper()}' / 'GAMEPLAY_AUDIO.txt'
        if not path.exists():
            logging.warning(f'File {path} not exists')
            continue
        with path.open('r', encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                # 祖传代码，忘记以前是踩了什么地方的坑要加\x00了
                tag: str = row['TAG'].replace("\x00", '')  # noqa
                logging.info(tag)
                if tag.startswith('#'):
                    continue
                text: str = row['TEXT'].replace("\x00", '')  # noqa
                result.setdefault(tag, {})[locale] = text
    return result


def get_guid(source: str) -> str | None:
    if isinstance(source, str) and len(parts := source.split(':')) > 1:
        return parts[1]
    return None
