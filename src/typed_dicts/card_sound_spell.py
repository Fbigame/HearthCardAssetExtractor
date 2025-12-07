from typing import List, Optional, TypedDict


class CardSoundSpellAudioSourceDict(TypedDict, total=False):
    m_FileID: Optional[int]
    m_PathID: Optional[int]


class CardSoundSpellCardSpecificVoDataDict(TypedDict, total=False):
    m_AudioSource: CardSoundSpellAudioSourceDict
    m_CardId: Optional[str]
    m_GameStringKey: Optional[str]
    m_RequireTag: Optional[int]
    m_SideToSearch: Optional[int]
    m_TagValue: Optional[int]
    m_ZonesToSearch: Optional[List[int]]


class CardSoundSpellCardSoundDataDict(TypedDict, total=False):
    m_AudioSource: CardSoundSpellAudioSourceDict


class CardSoundSpellDict(TypedDict, total=False):
    """m_CardSpecificVoDataList来自CardSpecificVoSpell但是它也有m_CardSoundData"""
    m_CardSoundData: CardSoundSpellCardSoundDataDict
    m_CardSpecificVoDataList: List[CardSoundSpellCardSpecificVoDataDict]
