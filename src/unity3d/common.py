import logging
import os
from functools import cached_property
from pathlib import Path
from typing import TypedDict, Optional, Sequence

import UnityPy

from helpers import safe_get
from typed_dicts import CardDefDict, CardSoundSpellDict


class CardSoundSpellReturnDict(TypedDict, total=False):
    normal: 'CardSoundSpellNormalReturnDict'
    specific: Optional[list['CardSpecificVoDataDict']]


class CardSoundSpellNormalReturnDict(TypedDict, total=False):
    sound_def: tuple['SoundDefReturnDict', ...]
    files: Sequence[str]


class CardSpecificVoDataReturnDict(TypedDict):
    m_CardId: str
    m_RequireTag: int
    m_SideToSearch: int
    m_TagValue: int
    m_ZonesToSearch: int


class CardSpecificVoDataDict(TypedDict, total=False):
    sound_def: tuple['SoundDefReturnDict', ...]
    GameStringKey: str
    GameStringValue: dict[str, str]
    condition: CardSpecificVoDataReturnDict
    files: Sequence[str]


class SoundDefReturnDict(TypedDict, total=False):
    guid: str
    weight: int


class CommonUnity3d:
    _instances = {}
    
    def __new__(cls, folder: os.PathLike[str] | str, filename: os.PathLike[str] | str):
        resolved_path = (Path(folder) / 'Data/Win' / filename).resolve()
        if resolved_path not in cls._instances:
            instance = super().__new__(cls)
            instance._instances[resolved_path] = instance
        return cls._instances[resolved_path]
    
    def __init__(self, folder: os.PathLike[str] | str, filename: os.PathLike[str] | str):
        unity3d_folder = Path(folder) / 'Data/Win'
        self._path = (unity3d_folder / filename).resolve().as_posix()
        self._filename: str = str(filename)
        self._unity3d_folder = unity3d_folder
    
    @cached_property
    def env(self):
        return UnityPy.load(self._path)
    
    def __repr__(self):
        return f'CommonUnity3d(path="{self._path}")'
    
    @cached_property
    def path_id(self):
        return {
            obj.path_id: obj
            for obj in self.env.objects
        }
    
    @property
    def container(self):
        return self.env.container
    
    def CardDef(self, guid: str) -> CardDefDict | None:
        game_object = self.container[guid].read_typetree()
        path_id = safe_get(game_object, 'm_Component', 1, 'component', 'm_PathID')
        if not path_id:
            return None
        return self.path_id[path_id].read_typetree()
    
    def CardSoundSpell(self, guid: str, gameplay_audio: dict[str, dict[str, str]]) -> CardSoundSpellReturnDict | None:
        if not guid:
            return None
        # 防止 UnityPy 空 PPtr (path_id==0) 或对象不存在导致 deref 报错
        if not (guid in self.container and getattr(self.container[guid], 'path_id', None)):
            return None
        game_object = self.container[guid].read_typetree()
        path_id = safe_get(game_object, 'm_Component', 1, 'component', 'm_PathID')
        if not path_id:
            return None
        card_sound_spell: CardSoundSpellDict = self.path_id[path_id].read_typetree()
        
        if 'm_CardSoundData' not in card_sound_spell:
            logging.warning(f'guid {guid} in {self._filename} 不是 CardSoundSpell')
            return None
        result = {}
        path_id = safe_get(card_sound_spell, 'm_CardSoundData', 'm_AudioSource', 'm_PathID')
        if sound_def := self._sound_def(path_id):
            result['normal'] = {'sound_def': sound_def}
        if 'm_CardSpecificVoDataList' in card_sound_spell:
            specific = []
            for data in card_sound_spell['m_CardSpecificVoDataList']:
                path_id = safe_get(data,'m_AudioSource', 'm_PathID')
                if not path_id:
                    continue
                sound_def = self._sound_def(path_id)
                if not sound_def:
                    continue
                specific.append({
                    'sound_def': sound_def,
                    'GameStringKey': (key := data.get('m_GameStringKey')),
                    'GameStringValue': {
                        locale: text
                        for locale, text in gameplay_audio.get(key, {}).items()
                    },
                    'condition': {
                        'm_CardId': data.get('m_CardId'),
                        'm_RequireTag': data.get("m_RequireTag"),
                        'm_SideToSearch': data.get("m_SideToSearch"),
                        'm_TagValue': data.get("m_TagValue"),
                        'm_ZonesToSearch': data.get("m_ZonesToSearch"),
                    },
                    
                })
            if specific:
                result['specific'] = specific
        return result  # noqa
    
    def _sound_def(self, path_id: int) -> tuple[SoundDefReturnDict, ...]:
        if not path_id:
            return tuple()
        audio_source = safe_get(self.path_id, path_id)
        if not audio_source:
            return tuple()
        else:
            audio_source = audio_source.read_typetree()
        path_id = safe_get(audio_source, 'm_GameObject', 'm_PathID')
        if not path_id:
            return tuple()
        game_object = safe_get(self.path_id, path_id)
        if not game_object:
            return tuple()
        else:
            game_object = game_object.read_typetree()
        
        path_id = safe_get(game_object, 'm_Component', 2, 'component', 'm_PathID')
        if not path_id:
            return tuple()
        sound_def = self.path_id.get(path_id)
        if not sound_def:
            return tuple()
        else:
            sound_def = sound_def.read_typetree()
        if text := sound_def.get('m_AudioClip'):
            return ({'guid': text.split(':')[-1], 'weight': 1},)
        elif random_clips := sound_def.get('m_RandomClips'):
            return tuple(
                {'guid': guid.split(':')[-1], 'weight': u['m_Weight']}
                for u in random_clips if (guid := u.get('m_Clip', None))
            )
        else:
            return tuple()
