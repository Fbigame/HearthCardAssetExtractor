import argparse
import json
import logging
from typing import Sequence

from context import CardContext
from helpers import get_guid
from typed_dicts import CardDefDict

__all__ = [
    'extract_images',
]

from unity3d import CommonUnity3d


def extract_asset(
        context: CardContext,
        base_guid: str,
        name: str,
):
    if not base_guid:
        logging.warning(f'Card({context.card_id}) 不存在 {name}版本的卡牌')
        return {}
    result = {}
    save_dir = context.output / context.card_id / 'image'
    
    for locale in context.locale_options:
        guid = base_guid
        bundle = context.asset_manifest.base_assets_catalog.get(guid)
        if locale != 'enus' and base_guid in (map_ := context.asset_manifest.asset_catalog_locale[locale]):
            guid, bundle = map_[base_guid]['guid'], map_[base_guid]['bundle']
        if not bundle:
            result[locale] = {
                'guid': guid,
                'file': None,
            }
            continue
        path = (save_dir / f'{name}_{locale}.png').as_posix()
        
        result[locale] = {
            'guid': guid,
            'file': path,
        }
        if not context.no_assets:
            save_dir.mkdir(parents=True, exist_ok=True)
            try:
                asset_unity3d = CommonUnity3d(context.input, bundle)
                obj = asset_unity3d.env.container[guid]
                data = obj.deref_parse_as_object()
                data.image.save(path)
            except Exception as e:
                logging.warning(f'解析图片出现异常：{e}')
                result[locale]['file'] = None
    return result


def extract_images(
        context: CardContext,
        card_def: CardDefDict,
        options: Sequence[str]
):
    struct = {}
    if not options:
        return struct
    for option in options:
        match option:
            case 'normal':
                guid = get_guid(card_def['m_PortraitTexturePath'])
                struct['normal'] = extract_asset(context, guid, name='normal')
            case 'signature':
                guid = get_guid(card_def['m_SignaturePortraitTexturePath'])
                struct['signature'] = extract_asset(context, guid, name='signature')
            case _:
                raise argparse.ArgumentTypeError(f'unknown image option: {option}')
    
    if context.enable_sub_struct:
        path = context.output / context.card_id / 'image' / 'struct.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(struct, f, indent=2, ensure_ascii=context.ensure_ascii)
    
    return struct
