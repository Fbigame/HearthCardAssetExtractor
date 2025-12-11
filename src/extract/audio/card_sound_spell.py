import logging

from helpers import CardContext
from unity3d import CommonUnity3d


def extract_asset(
        context: CardContext,
        base_guid: str,
        option,
        prefix: str,
):
    if not base_guid:
        logging.warning(f'Card({context.card_id}) 不存在音频 {option}/{prefix}')
        return {}
    result = {}
    save_dir = context.output / context.card_id / 'audio' / option
    if not context.no_assets:
        save_dir.mkdir(parents=True, exist_ok=True)
    for locale in context.locale_options:
        guid = base_guid
        files = []
        bundle = context.asset_manifest.base_assets_catalog[guid]
        if locale != 'enus' and base_guid in (map_ := context.asset_manifest.asset_catalog_locale[locale]):
            guid, bundle = map_[base_guid]['guid'], map_[base_guid]['bundle']
        
        asset_unity3d = CommonUnity3d(context.input, bundle)
        obj = asset_unity3d.env.container[guid]
        samples = obj.deref_parse_as_object().samples
        for i, data in enumerate(samples.values(), start=1):
            path = save_dir / f'{prefix}_{locale}{i}.wav'
            files.append(path.as_posix())
            if not context.no_assets:
                with path.open('wb') as f:
                    f.write(data)
        result[locale] = {
            'guid': guid,
            'files': files,
        }
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
    if guid := card_sound_spell.get('normal', {}).get('guid'):
        del card_sound_spell['normal']['guid']
        card_sound_spell['normal']['guid_file_map'] = extract_asset(context, guid, option, f'{prefix}_normal')
    if specific := card_sound_spell.get('specific'):
        for i, unit in enumerate(specific, start=1):
            guid = unit['guid']
            del unit['guid']
            unit['guid_file_map'] = extract_asset(context, guid, option, f'{prefix}_specific_{i}')
    return card_sound_spell
