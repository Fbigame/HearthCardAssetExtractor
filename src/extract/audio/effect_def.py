import json
import logging

from helpers import get_guid
from context import CardContext
from typed_dicts.card_def import CardDefEffectDefDict
from .card_sound_spell import extract_card_sound_spell, empty_card_sound_spell


def extract_effect_defs(context: CardContext, effect_defs: list[CardDefEffectDefDict], option: str):
    if not effect_defs:
        logging.warning(f'Card({context.card_id}) 不存在音频{option}')
        return []
    struct = [
        extract_effect_def(context, effect_def, f'{option}', f'effect_def_{i}_')
        for i, effect_def, in enumerate(effect_defs, start=1)
    ]
    if context.enable_sub_struct:
        path = context.output / context.card_id / 'audio' / option / 'struct.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(struct, f, indent=2, ensure_ascii=context.ensure_ascii)
    
    return struct


def extract_effect_def(context: CardContext, effect_def: CardDefEffectDefDict, option: str, prefix=""):
    not_exist_error_info = f'Card({context.card_id}) 不存在音频 {option} {prefix[:-1]}'
    if not effect_def:
        logging.warning(not_exist_error_info)
        return {}
    # 解析effect_def
    struct = {'spell': empty_card_sound_spell, 'sound_spells': []}
    if (
            (guid := get_guid(effect_def.get('m_SpellPath')))
            and (card_sound_spell := extract_card_sound_spell(context, guid, option, f'{prefix}spell'))
    ):
        struct['spell'] = card_sound_spell
    if sound_spells := effect_def.get('m_SoundSpellPaths'):
        struct['sound_spells'] = [
            card_sound_spell
            for i, guid in enumerate(sound_spells, start=1)
            if ((process_guid := get_guid(guid)) and (card_sound_spell := extract_card_sound_spell(
                context,
                process_guid,
                option,
                f'{prefix}sound_spell_{i}'
            )))
        
        ]
    
    if not struct:
        logging.warning(not_exist_error_info)
        return {}
    
    if not prefix and context.enable_sub_struct:
        # 没prefix说明是直接生成的，需要创建struct.json
        path = context.output / context.card_id / 'audio' / option / 'struct.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(struct, f, indent=2, ensure_ascii=context.ensure_ascii)
    
    return struct
