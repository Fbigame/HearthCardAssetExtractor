import argparse
import logging

from parse_args import parse_args, HearthstoneExtractContext
from unity3d import CommonUnity3d
from utils.extract_audio import extract_audio, extract_audio_list, extract_audio_emote
from utils.extract_image import extract_image
from utils.helper import Context, get_guid, load_emote_type, load_strings_gameplay_audio


def extract_card(context: HearthstoneExtractContext, card_id: str):
    if not (guid := context.asset_manifest.cards_map[card_id]):
        logging.warning(f'Card({card_id}) 不存在 CardDef')
        return
    bundle = context.asset_manifest.base_assets_catalog[guid]
    card_def = CommonUnity3d(context.input_path, bundle).CardDef(guid)
    base_context = Context(
        input=context.input_path,
        output=context.output_path,
        asset_manifest=context.asset_manifest,
        locale_options=context.locale_options,
        card_id=card_id,
        ensure_ascii=context.ensure_ascii,
        gameplay_audio=load_strings_gameplay_audio(context.input_path, context.locale_options)
    )
    if 'emote' in context.audio_options:
        emote_type = load_emote_type(context.input_path)
    else:
        emote_type = {}
    
    for option in context.image_options:
        match option:
            case 'normal':
                guid = get_guid(card_def['m_PortraitTexturePath'])
                extract_image(base_context, guid=guid, name='normal')
            case 'signature':
                guid = get_guid(card_def['m_SignaturePortraitTexturePath'])
                extract_image(base_context, guid=guid, name='signature')
            case _:
                raise argparse.ArgumentTypeError(f'unknown image option: {option}')
    
    for option in context.audio_options:
        match option:
            case 'additional-play':
                extract_audio_list(base_context, card_def['m_AdditionalPlayEffectDefs'], option)
            case 'attack':
                extract_audio(base_context, card_def['m_AttackEffectDef'], option)
            case 'death':
                extract_audio(base_context, card_def['m_DeathEffectDef'], option)
            case 'lifetime':
                extract_audio(base_context, card_def['m_LifetimeEffectDef'], option)
            case 'trigger':
                extract_audio_list(base_context, card_def['m_TriggerEffectDefs'], option)
            case 'sub-option':
                extract_audio_list(base_context, card_def['m_SubOptionEffectDefs'], option)
            case 'reset-game':
                extract_audio_list(base_context, card_def['m_ResetGameEffectDefs'], option)
            case 'sub-spell':
                extract_audio_list(base_context, card_def['m_SubSpellEffectDefs'], option)
            case 'emote':
                extract_audio_emote(base_context, card_def['m_EmoteDefs'], emote_type)
            case _:
                raise argparse.ArgumentTypeError(f'unknown audio option: {option}')


def main():
    context = parse_args()
    for card_id in context.card_ids:
        try:
            extract_card(context, card_id)
        except Exception as e:
            logging.critical(f'Card({card_id}) 解析失败： {str(e)}', exc_info=True)


if __name__ == '__main__':
    main()
