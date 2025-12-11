import argparse
import json
from typing import Sequence

from helpers import CardContext
from helpers import load_strings_gameplay_audio
from typed_dicts import CardDefDict
from .effect_def import extract_effect_def, extract_effect_defs
from .emote import extract_audio_emote


def extract_audios(context: CardContext, card_def: CardDefDict, options: Sequence[str]):
    struct = {}
    if not options:
        return struct
    context.gameplay_audio = load_strings_gameplay_audio(context.input, context.locale_options)
    for option in options:
        match option:
            case 'additional-play':
                struct[option] = extract_effect_defs(context, card_def['m_AdditionalPlayEffectDefs'], option)
            case 'attack':
                struct[option] = extract_effect_def(context, card_def['m_AttackEffectDef'], option)
            case 'death':
                struct[option] = extract_effect_def(context, card_def['m_DeathEffectDef'], option)
            case 'lifetime':
                struct[option] = extract_effect_def(context, card_def['m_LifetimeEffectDef'], option)
            case 'trigger':
                struct[option] = extract_effect_defs(context, card_def['m_TriggerEffectDefs'], option)
            case 'sub-option':
                struct[option] = extract_effect_defs(context, card_def['m_SubOptionEffectDefs'], option)
            case 'reset-game':
                struct[option] = extract_effect_defs(context, card_def['m_ResetGameEffectDefs'], option)
            case 'sub-spell':
                struct[option] = extract_effect_defs(context, card_def['m_SubSpellEffectDefs'], option)
            case 'emote':
                struct[option] = extract_audio_emote(context, card_def['m_EmoteDefs'])
            case 'play':
                struct[option] = extract_effect_def(context, card_def['m_PlayEffectDef'], 'play')
            case _:
                raise argparse.ArgumentTypeError(f'unknown audio option: {option}')
    
    if context.enable_sub_struct:
        path = context.output / context.card_id / 'audio' / 'struct.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(struct, f, indent=2, ensure_ascii=context.ensure_ascii)
    return struct
