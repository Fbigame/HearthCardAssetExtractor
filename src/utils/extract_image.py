import logging
from pathlib import Path
from typing import Callable

import UnityPy.classes

from unity3d.common import CommonUnity3d


def get_guid(source: str) -> str | None:
    if isinstance(source, str) and len(parts := source.split(':')) > 1:
        return parts[1]
    return None


def extract_asset(context, base_guid: str, save_callback: Callable[[UnityPy.classes.PPtr, str], None]):
    for locale in context.locale_options:
        guid = base_guid
        bundle = context.asset_manifest.base_assets_catalog[guid]
        if locale != 'enus' and base_guid in (map_ := context.asset_manifest.asset_catalog_locale[locale]):
            guid, bundle = map_[base_guid]['guid'], map_[base_guid]['bundle']
        
        asset_unity3d = CommonUnity3d(context.input, bundle)
        obj = asset_unity3d.env.container[guid]
        save_callback(obj, locale)


def extract_image(context, guid: str, name: str):
    if not guid:
        logging.warning(f'Card({context.card_id}) 不存在 {name} 版本的卡图')
        return
    
    def save_image(obj: UnityPy.classes.PPtr, locale: str):
        data = obj.deref_parse_as_object()
        save_dir = context.output / context.card_id / 'image'
        save_dir.mkdir(parents=True, exist_ok=True)
        data.image.save((save_dir / f'{name}_{locale}.png').as_posix())
    
    extract_asset(context, guid, save_image)
