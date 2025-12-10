import json
import logging

from extract.card import extract_card
from parse_args import parse_args


def main():
    context = parse_args()
    struct = {}
    for card_id in context.card_ids:
        try:
            struct[card_id] = extract_card(context, card_id)
        except Exception as e:
            logging.critical(f'Card({card_id}) 解析失败： {str(e)}', exc_info=True)
            struct[card_id] = {}
    if context.merged_struct:
        path = context.output_path / 'struct.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(struct, f, indent=2, ensure_ascii=context.ensure_ascii)


if __name__ == '__main__':
    main()
