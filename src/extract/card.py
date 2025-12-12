import json
import logging

from context import CardContext
from parse_args import HearthstoneExtractContext
from unity3d import CommonUnity3d
from .audio import extract_audios
from .image import extract_images


def extract_card(
        context: HearthstoneExtractContext,
        card_id: str,

):
    if not (guid := context.asset_manifest.cards_map[card_id]):
        logging.warning(f'Card({card_id}) 不存在 CardDef')
        return
    bundle = context.asset_manifest.base_assets_catalog[guid]
    
    card_def = CommonUnity3d(context.input_path, bundle).CardDef(guid)
    card_context = CardContext(
        input=context.input_path,
        output=context.output_path,
        asset_manifest=context.asset_manifest,
        locale_options=context.locale_options,
        card_id=card_id,
        ensure_ascii=context.ensure_ascii,
        enable_sub_struct=context.enable_sub_struct,
        no_assets=context.no_assets,
        merged_struct=context.merged_struct,
    )
    struct = {
        'image': extract_images(card_context, card_def, context.image_options),
        'audio': extract_audios(card_context, card_def, context.audio_options),
    }
    if not context.merged_struct or context.enable_sub_struct:
        path = context.output_path / card_id / 'struct.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(struct, f, indent=2, ensure_ascii=context.ensure_ascii)

    return struct
