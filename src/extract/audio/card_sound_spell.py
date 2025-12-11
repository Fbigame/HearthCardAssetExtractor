import logging

from helpers import CardContext
from unity3d import CommonUnity3d
from unity3d.common import SoundDefReturnDict


def extract_asset(
        context: CardContext,
        guid_weight_map: tuple[SoundDefReturnDict],
        option,
        prefix: str,
):
    """Extract audio assets.

    Args:
        context (CardContext): Processing context.
        guid_weight_map (tuple[SoundDefReturnDict]): Guid + weight info.
        option (_type_): Directory name such as 'attack', 'death', etc.
        prefix (str): Filename prefix.

    Returns:
        list: A list of sound_units, each containing:
            {
                "base_guid": str,
                "weight": float,
                "locale_guid": { locale: guid },
                "locale_files": { locale: [file paths] }
            }
    """
    result = []
    save_dir = context.output / context.card_id / 'audio' / option
    if not context.no_assets:
        save_dir.mkdir(parents=True, exist_ok=True)
    
    for j, u in enumerate(guid_weight_map, start=1):
        base_guid = u['guid']
        
        if not base_guid:
            logging.warning(f'Card({context.card_id}) 不存在音频 {option}/{prefix}')
            return {}
        
        unit = {
            'base_guid': base_guid,
            'weight': u['weight'],
            'locale_guid': {},
            'locale_files': {},
        }
        
        for locale in context.locale_options:
            guid = base_guid
            bundle = context.asset_manifest.base_assets_catalog[guid]
            
            # 替换本地化 GUID
            if locale != 'enus' and base_guid in (map_ := context.asset_manifest.asset_catalog_locale[locale]):
                guid, bundle = map_[base_guid]['guid'], map_[base_guid]['bundle']
            
            # Unity 解析
            asset_unity3d = CommonUnity3d(context.input, bundle)
            obj = asset_unity3d.env.container[guid]
            samples = obj.deref_parse_as_object().samples
            
            # 提取 wav 文件
            files = []
            for i, data in enumerate(samples.values(), start=1):
                path = save_dir / f'{prefix}_{j}_{locale}{i}.wav'
                files.append(path.as_posix())
                if not context.no_assets:
                    with path.open('wb') as f:
                        f.write(data)
            
            # 存储新结构
            unit['locale_guid'][locale] = guid
            unit['locale_files'][locale] = files
        
        result.append(unit)
    
    return result


empty_card_sound_spell = {}


def extract_card_sound_spell(context: CardContext, guid: str, option: str, prefix: str):
    bundle = context.asset_manifest.base_assets_catalog[guid]
    card_sound_spell = CommonUnity3d(context.input, bundle).CardSoundSpell(
        guid,
        gameplay_audio=context.gameplay_audio
    )
    if not card_sound_spell:
        return empty_card_sound_spell
    if sound_def := card_sound_spell.get('normal', {}).get('sound_def'):
        del card_sound_spell['normal']['sound_def']
        card_sound_spell['normal']['sound_units'] = extract_asset(context, sound_def, option, f'{prefix}_normal')
    if specific := card_sound_spell.get('specific'):
        for i, unit in enumerate(specific, start=1):
            sound_def = unit['sound_def']
            del unit['sound_def']
            unit['sound_units'] = extract_asset(context, sound_def, option, f'{prefix}_specific_{i}')
    return card_sound_spell
