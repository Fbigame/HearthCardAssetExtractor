from typing import Optional, TypedDict


class CardDefGameObjectDict(TypedDict, total=False):
    m_FileID: Optional[int]
    m_PathID: Optional[int]


class CardDefDiamondPlaneRttCearColorDict(TypedDict, total=False):
    r: Optional[float]
    g: Optional[float]
    b: Optional[float]
    a: Optional[float]


class CardDefCustomDeckPortraitDict(TypedDict, total=False):
    screens: Optional[list[int]]
    values: list[CardDefGameObjectDict]


class CardDefEffectDefDict(TypedDict, total=False):
    m_SpellPath: Optional[str]
    m_SoundSpellPaths: list[str]





class CardDefSpellTableOverridesDict(TypedDict, total=False):
    m_Type: Optional[int]
    m_SpellPrefabName: Optional[str]


class CardDefCustomHeroTraySettingsDict(TypedDict, total=False):
    m_Board: Optional[int]
    m_Tint: Optional[CardDefDiamondPlaneRttCearColorDict]


class CardDefEmoteDefsDict(TypedDict, total=False):
    m_emoteType: Optional[int]
    m_emoteSpellPath: Optional[str]
    m_emoteSoundSpellPath: Optional[str]
    m_emoteGameStringKey: Optional[str]


class CardDefSpecialEventsDict(TypedDict, total=False):
    EventType: Optional[int]
    m_SceneMode: Optional[int]
    m_Scenario: Optional[int]
    m_PortraitTextureOverride: Optional[str]
    m_PremiumPortraitMaterialOverride: Optional[str]
    m_PremiumUberShaderAnimationOverride: Optional[str]
    m_PremiumPortraitTextureOverride: Optional[str]



class CardDefDict(TypedDict, total=False):
    m_GameObject: CardDefGameObjectDict
    m_Enabled: Optional[int]
    m_Script: CardDefGameObjectDict
    m_Name: Optional[str]
    m_Portrait: CardDefGameObjectDict
    m_PortraitTexturePath: Optional[str]
    m_PremiumPortraitMaterialPath: Optional[str]
    m_PremiumUberShaderAnimationPath: Optional[str]
    m_PremiumPortraitTexturePath: Optional[str]
    m_SignaturePortraitTexturePath: Optional[str]
    m_SignaturePortraitMaterialPath: Optional[str]
    m_SignatureUberShaderAnimationPath: Optional[str]
    m_DiamondPlaneRTT_Hand: Optional[str]
    m_DiamondPlaneRTT_Play: Optional[str]
    m_DiamondBackground_Hand: Optional[str]
    m_DiamondBackground_Play: Optional[str]
    m_DiamondPlaneRTT_CearColor: CardDefDiamondPlaneRttCearColorDict
    m_DiamondPortraitTexturePath: Optional[str]
    m_DiamondModel: Optional[str]
    m_LegendaryModel: Optional[str]
    m_MobileLegendaryModel: Optional[str]
    m_PreferredActorPortraitIndex: Optional[int]
    m_DeckCardBarPortrait: CardDefGameObjectDict
    m_SignatureDeckCardBarPortrait: CardDefGameObjectDict
    m_EnchantmentPortrait: CardDefGameObjectDict
    m_HistoryTileHalfPortrait: CardDefGameObjectDict
    m_HistoryTileFullPortrait: CardDefGameObjectDict
    m_HistoryTileFullSignaturePortrait: CardDefGameObjectDict
    m_HistoryTileHalfSignaturePortrait: CardDefGameObjectDict
    m_LeaderboardTileFullPortrait: CardDefGameObjectDict
    m_CustomDeckPortrait: CardDefCustomDeckPortraitDict
    m_DeckPickerPortrait: CardDefCustomDeckPortraitDict
    m_BattlegroundHeroBuddyPortraitTexturePath: Optional[str]
    m_BattlegroundHeroBuddyPortraitMaterial: CardDefGameObjectDict
    m_BattlegroundsQuestRewardsMaterial: CardDefGameObjectDict
    m_BattlegroundsTrinketMaterial: CardDefGameObjectDict
    m_BattlegroundAnomalyMedallionMaterial: CardDefGameObjectDict
    m_BattlegroundSpellOnBoardMaterial: CardDefGameObjectDict
    m_CustomRenderDisplayOverride: Optional[str]
    m_LockedClassPortrait: CardDefGameObjectDict
    m_PracticeAIPortrait: CardDefGameObjectDict
    m_DeckBoxPortrait: CardDefGameObjectDict
    m_MercenaryBarPortrait: CardDefGameObjectDict
    m_MercenaryCoinPortrait: CardDefGameObjectDict
    m_MercenaryMapBossCoinPortrait: CardDefGameObjectDict
    m_TeamTray: CardDefGameObjectDict
    m_AlwaysRenderPremiumPortrait: Optional[int]
    m_CardSilhouetteOverride: Optional[int]
    m_FrameMeshOverride: CardDefGameObjectDict
    m_IgnoreLegendaryPortraitForDeckCollection: Optional[int]
    m_UseLegendaryPortraitForHistoryTile: Optional[int]
    m_PlayEffectDef: CardDefEffectDefDict
    m_AdditionalPlayEffectDefs: list[CardDefEffectDefDict]
    m_AttackEffectDef: CardDefEffectDefDict
    m_DeathEffectDef: CardDefEffectDefDict
    m_LifetimeEffectDef: CardDefEffectDefDict
    m_TriggerEffectDefs: list[CardDefEffectDefDict]
    m_SubOptionEffectDefs: list[CardDefEffectDefDict]
    m_ResetGameEffectDefs: list[CardDefEffectDefDict]
    m_SubSpellEffectDefs: list[CardDefEffectDefDict]
    m_CustomSummonSpellPath: Optional[str]
    m_GoldenCustomSummonSpellPath: Optional[str]
    m_DiamondCustomSummonSpellPath: Optional[str]
    m_CustomSpawnSpellPath: Optional[str]
    m_GoldenCustomSpawnSpellPath: Optional[str]
    m_DiamondCustomSpawnSpellPath: Optional[str]
    m_CustomDeathSpellPath: Optional[str]
    m_GoldenCustomDeathSpellPath: Optional[str]
    m_DiamondCustomDeathSpellPath: Optional[str]
    m_CustomDiscardSpellPath: Optional[str]
    m_GoldenCustomDiscardSpellPath: Optional[str]
    m_DiamondCustomDiscardSpellPath: Optional[str]
    m_CustomKeywordSpellPath: Optional[str]
    m_CustomChoiceRevealSpellPath: Optional[str]
    m_CustomChoiceConcealSpellPath: Optional[str]
    m_SpellTableOverrides: list[CardDefSpellTableOverridesDict]
    m_CollectionHeroDefPath: Optional[str]
    m_CustomHeroArmorSpell: Optional[str]
    m_SocketInEffectFriendly: Optional[str]
    m_SocketInEffectOpponent: Optional[str]
    m_SocketInEffectFriendlyPhone: Optional[str]
    m_SocketInEffectOpponentPhone: Optional[str]
    m_SocketInOverrideHeroAnimation: Optional[int]
    m_SocketInParentEffectToHero: Optional[int]
    m_CustomHeroTray: Optional[str]
    m_CustomHeroTrayGolden: Optional[str]
    m_DisablePremiumHeroTray: Optional[int]
    m_HeroFrameFriendlyPath: Optional[str]
    m_HeroFrameEnemyPath: Optional[str]
    m_CustomHeroTraySettings: list[CardDefCustomHeroTraySettingsDict]
    m_CustomHeroPhoneTray: Optional[str]
    m_CustomHeroPhoneManaGem: Optional[str]
    m_AnnouncerLinePath: Optional[str]
    m_AnnouncerLineBeforeVersusPath: Optional[str]
    m_AnnouncerLineAfterVersusPath: Optional[str]
    m_HeroPickerSelectedPrefab: Optional[str]
    m_EmoteDefs: list[CardDefEmoteDefsDict]
    m_LegendaryHeroSkinConfig: CardDefGameObjectDict
    m_StoreItemDisplayPath: Optional[str]
    m_CustomHeroFramePrefab: Optional[str]
    m_CustomHeroInfoFramePrefab: Optional[str]
    m_SuppressDeathrattleDeath: Optional[int]
    m_SuppressPlaySoundsOnSummon: Optional[int]
    m_SuppressPlaySoundsDuringMulligan: Optional[int]
    m_SpecialEvents: list[CardDefSpecialEventsDict]
    m_petDataAssetPath: Optional[str]
    m_petVariantDataAssetPath: Optional[str]
