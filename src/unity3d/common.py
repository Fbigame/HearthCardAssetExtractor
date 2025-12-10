import logging
import os
from functools import cached_property
from pathlib import Path
from typing import TypedDict, Optional, Sequence

import UnityPy

from typed_dicts import CardDefDict, CardSoundSpellDict


class CardSoundSpellReturnDict(TypedDict, total=False):
    normal: 'CardSoundSpellNormalReturnDict'
    specific: Optional[list['CardSpecificVoDataDict']]


class CardSoundSpellNormalReturnDict(TypedDict, total=False):
    guid: str
    files: Sequence[str]


class CardSpecificVoDataReturnDict(TypedDict):
    m_CardId: str
    m_RequireTag: int
    m_SideToSearch: int
    m_TagValue: int
    m_ZonesToSearch: int


class CardSpecificVoDataDict(TypedDict, total=False):
    guid: str
    GameStringKey: str
    GameStringValue: dict[str, str]
    condition: CardSpecificVoDataReturnDict
    files: Sequence[str]


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
    
    def CardDef(self, guid: str) -> CardDefDict:
        game_object = self.container[guid].read_typetree()
        path_id = game_object['m_Component'][1]['component']['m_PathID']
        return self.path_id[path_id].read_typetree()
    
    def CardSoundSpell(self, guid: str, gameplay_audio: dict[str, dict[str, str]]) -> CardSoundSpellReturnDict | None:
        game_object = self.container[guid].read_typetree()
        path_id = game_object['m_Component'][1]['component']['m_PathID']
        card_sound_spell: CardSoundSpellDict = self.path_id[path_id].read_typetree()
        
        result = {}
        if 'm_CardSoundData' not in card_sound_spell:
            logging.info(f'guid {guid} in {self._filename} 不是 CardSoundSpell')
            return None
        path_id = card_sound_spell['m_CardSoundData']['m_AudioSource']['m_PathID']
        if audio_guid := self._sound_def(path_id):
            result['normal'] = {'guid': audio_guid}
        if 'm_CardSpecificVoDataList' in card_sound_spell:
            specific = []
            for data in card_sound_spell['m_CardSpecificVoDataList']:
                path_id = data['m_AudioSource']['m_PathID']
                audio_guid = self._sound_def(path_id)
                if not audio_guid:
                    continue
                specific.append({
                    'guid': audio_guid.split(':')[-1],
                    'GameStringKey': (key := data['m_GameStringKey']),
                    'GameStringValue': {
                        locale: text
                        for locale, text in gameplay_audio.get(key, {}).items()
                    },
                    'condition': {
                        'm_CardId': data['m_CardId'],
                        'm_RequireTag': data["m_RequireTag"],
                        'm_SideToSearch': data["m_SideToSearch"],
                        'm_TagValue': data["m_TagValue"],
                        'm_ZonesToSearch': data["m_ZonesToSearch"],
                    },
                    
                })
            if specific:
                result['specific'] = specific
        return result  # noqa
    
    def _sound_def(self, path_id: int) -> Optional[str]:
        audio_source = self.path_id[path_id].read_typetree()
        path_id = audio_source['m_GameObject']['m_PathID']
        game_object = self.path_id[path_id].read_typetree()
        path_id = game_object['m_Component'][2]['component']['m_PathID']
        sound_def = self.path_id[path_id].read_typetree()
        text: str = sound_def['m_AudioClip']
        if text:
            return text.split(':')[1]
        else:
            return None
