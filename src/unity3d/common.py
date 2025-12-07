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
    m_GameStringKey: str
    m_RequireTag: int
    m_SideToSearch: int
    m_TagValue: int
    m_ZonesToSearch: int


class CardSpecificVoDataDict(TypedDict, total=False):
    guid: str
    condition: CardSpecificVoDataReturnDict
    files: Sequence[str]


class CommonUnity3d:
    _instances = {}
    
    def __new__(cls, folder: os.PathLike[str] | str, filename: os.PathLike[str] | str):
        resolved_path = (Path(folder) / filename).resolve()
        if resolved_path not in cls._instances:
            instance = super().__new__(cls)
            instance._instances[resolved_path] = instance
        return cls._instances[resolved_path]
    
    def __init__(self, folder: os.PathLike[str] | str, filename: os.PathLike[str] | str):
        self._unity3d_folder = folder
        self._path = (Path(folder) / filename).resolve().as_posix()
    
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
    
    def CardSoundSpell(self, guid: str) -> CardSoundSpellReturnDict:
        game_object = self.container[guid].read_typetree()
        path_id = game_object['m_Component'][1]['component']['m_PathID']
        card_sound_spell: CardSoundSpellDict = self.path_id[path_id].read_typetree()
        
        result = {}
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
                import logging
                specific.append({
                    'guid': audio_guid.split(':')[-1],
                    'condition': {
                        'm_CardId': data['m_CardId'],
                        'm_GameStringKey': data["m_GameStringKey"],
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
