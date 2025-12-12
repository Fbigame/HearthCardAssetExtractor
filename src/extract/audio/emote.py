import json
import logging

from helpers import load_emote_type, get_guid
from context import CardContext
from typed_dicts.card_def import CardDefEmoteDefsDict
from .card_sound_spell import extract_card_sound_spell, empty_card_sound_spell


def extract_audio_emote(context: CardContext, emote_defs: list[CardDefEmoteDefsDict]):
    if not emote_defs:
        logging.warning(f'Card({context.card_id}) 不存在音频 emote')
        return
    struct = []
    emote_type = load_emote_type(context.input)
    for emote_def in emote_defs:
        emote_type_code = emote_def.get('m_emoteType')
        name = emote_type.get(emote_type_code, f'type_{emote_type_code}')
        unit = {
            'emote_type': emote_type_code,
            'emote_type_name': name,
            'GameStringKey': (key := emote_def.get('m_emoteGameStringKey')),
            'GameStringValue': {
                locale: text
                for locale, text in context.gameplay_audio.get(key, {}).items()
            },
            'sound_spell': empty_card_sound_spell,
            'spell': empty_card_sound_spell,
        }
        append_flag = False
        if (
                (guid := get_guid(emote_def.get('m_emoteSoundSpellPath')))
                and (card_sound_spell := extract_card_sound_spell(context, guid, 'emote', f'{name}_sound_spell'))
        ):
            unit['sound_spell'] = card_sound_spell
            append_flag = True
        if (
                (guid := get_guid(emote_def.get('m_emoteSpellPath')))
                and (card_sound_spell := extract_card_sound_spell(context, guid, 'emote', f'{name}_spell'))
        ):
            unit['spell'] = card_sound_spell
            append_flag = True
        if append_flag:
            struct.append(unit)
    if context.enable_sub_struct:
        path = context.output / context.card_id / 'audio' / 'emote' / 'struct.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(struct, f, indent=2, ensure_ascii=context.ensure_ascii)
    return struct
