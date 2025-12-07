import json
import logging
from pathlib import Path
from typing import Callable

import UnityPy.classes

from unity3d.common import CommonUnity3d, CardSoundSpellReturnDict
from typed_dicts.card_def import CardDefEffectDefDict


def get_guid(source: str) -> str | None:
    if isinstance(source, str) and len(parts := source.split(':')) > 1:
        return parts[1]
    return None


def parse_card_sound_spell(context, guid):
    bundle = context.asset_manifest.base_assets_catalog[guid]
    card_sound_spell = CommonUnity3d(context.input, bundle).CardSoundSpell(guid)
    return card_sound_spell


def parse_audio_struct(context, effect_def: CardDefEffectDefDict):
    struct = {}
    if (guid := get_guid(effect_def['m_SpellPath'])) and (card_sound_spell := parse_card_sound_spell(context, guid)):
        struct['spell']: CardSoundSpellReturnDict = card_sound_spell
    if sound_spell := effect_def['m_SoundSpellPaths']:
        sound_spells = tuple(
            card_sound_spell
            for guid in sound_spell
            if (process_guid := get_guid(guid)) and (card_sound_spell := parse_card_sound_spell(context, process_guid))
        )
        if sound_spells:
            struct['sound_spells']: tuple[CardSoundSpellReturnDict] = sound_spells
    return struct


def extract_asset(context, base_guid: str, save_callback: Callable[[UnityPy.classes.PPtr, str], None]):
    for locale in context.locale_options:
        guid = base_guid
        bundle = context.asset_manifest.base_assets_catalog[guid]
        if locale != 'enus' and base_guid in (map_ := context.asset_manifest.asset_catalog_locale[locale]):
            guid, bundle = map_[base_guid]['guid'], map_[base_guid]['bundle']
        
        asset_unity3d = CommonUnity3d(context.input, bundle)
        obj = asset_unity3d.env.container[guid]
        save_callback(obj, locale)


def extract_sound(context, guid: str, save_dir: Path, prefix: str):
    result = []
    if not guid:
        return result
    
    def save(obj: UnityPy.classes.PPtr, locale: str):
        samples = obj.deref_parse_as_object().samples
        for i, data in enumerate(samples.values(), start=1):
            filename = f'{prefix}_{locale}{i}.wav'
            result.append(filename)
            with (save_dir / filename).open('wb') as f:
                f.write(data)
    
    extract_asset(context, guid, save)
    return result


def extract_card_sound_spell_data(context, struct: CardSoundSpellReturnDict, save_dir: Path, prefix: str):
    if guid := struct.get('normal', {}).get('guid'):
        struct['normal']['files'] = extract_sound(context, guid, save_dir, f'{prefix}_normal')
    if specific := struct.get('specific'):
        for i, unit in enumerate(specific, start=1):
            unit['files'] = extract_sound(context, unit['guid'], save_dir, f'{prefix}_specific_{i}')


def extract_audio(context, effect_def: CardDefEffectDefDict, option: str):
    not_exist_error_info = f'Card({context.card_id}) 不存在音频 {option}'
    if not effect_def:
        logging.warning(not_exist_error_info)
        return
    struct = parse_audio_struct(context, effect_def)
    if not struct:
        logging.warning(not_exist_error_info)
        return
    save_dir = context.output / context.card_id / f'{option}_audio'
    save_dir.mkdir(parents=True, exist_ok=True)
    
    if spell := struct.get('spell'):
        extract_card_sound_spell_data(context, spell, save_dir, 'spell')
    if sound_spells := struct.get('sound_spells'):  # noqa
        sound_spells: tuple[CardSoundSpellReturnDict]
        for i, unit in enumerate(sound_spells, start=1):
            extract_card_sound_spell_data(context, unit, save_dir, f'sound_spell_{i}')
    
    with (save_dir / 'struct.json').open('w') as f:
        json.dump(struct, f, indent=2)


def extract_audio_list(context, effect_defs: list[CardDefEffectDefDict], option: str):
    for i, effect_def in enumerate(effect_defs, start=1):
        extract_audio(context, effect_def, f'{option}{i}')
