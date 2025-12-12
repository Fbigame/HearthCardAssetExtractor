from dataclasses import dataclass
from pathlib import Path

from unity3d import AssetManifest


@dataclass
class CardContext:
    input: Path
    output: Path
    asset_manifest: AssetManifest
    locale_options: tuple[str, ...]
    card_id: str
    ensure_ascii: bool
    enable_sub_struct: bool
    no_assets: bool
    merged_struct: bool
    gameplay_audio: dict[str, dict[str, str]] | None = None
