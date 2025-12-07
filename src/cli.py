import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

from parse_args import parse_args, HearthstoneExtractContext
from unity3d import AssetManifest, CommonUnity3d
from utils import extract_image, extract_audio, extract_audio_list


@dataclass
class Context:
    input: Path
    output: Path
    logger: logging.Logger
    asset_manifest: AssetManifest
    locale_options: tuple[str, ...]
    card_id: str


def get_guid(source: str) -> str | None:
    if isinstance(source, str) and len(parts := source.split(':')) > 1:
        return parts[1]
    return None


def extract_card(context: HearthstoneExtractContext, card_id: str):
    if not (guid := context.asset_manifest.cards_map[card_id]):
        context.logger.warning(f'Card({card_id}) 不存在 CardDef')
        return
    bundle = context.asset_manifest.base_assets_catalog[guid]
    card_def = CommonUnity3d(context.input_path, bundle).CardDef(guid)
    base_context = Context(
        input=context.input_path,
        output=context.output_path,
        logger=context.logger,
        asset_manifest=context.asset_manifest,
        locale_options=context.locale_options,
        card_id=card_id
    )
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
            case _:
                raise argparse.ArgumentTypeError(f'unknown audio option: {option}')


def main():
    context = parse_args()
    for card_id in context.card_ids:
        try:
            extract_card(context, card_id)
        except Exception as e:
            context.logger.critical(f'Card({card_id}) 解析失败： {str(e)}', exc_info=True)


if __name__ == '__main__':
    main()
