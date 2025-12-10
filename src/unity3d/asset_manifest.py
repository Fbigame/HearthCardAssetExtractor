import argparse
import logging
import os
from functools import cached_property
from pathlib import Path
from typing import TypedDict

import UnityPy


class AssetManifest:
    _instances = {}
    
    def __new__(cls, folder: os.PathLike[str] | str):
        folder = Path(folder).resolve() / 'Data/Win'
        if folder not in cls._instances:
            instance = super().__new__(cls)
            instance._instances[folder] = instance
        return cls._instances[folder]
    
    def __init__(self, folder: os.PathLike[str] | str):
        self._unity3d_folder = Path(folder) / 'Data/Win'
    
    @cached_property
    def _main_env(self):
        return UnityPy.load((self._unity3d_folder / 'asset_manifest.unity3d').as_posix())
    
    @cached_property
    def cards_map(self):
        # note-mini-guid -> card-def-guid 部分卡牌不存在这个映射, id not in cards_map
        data = self._main_env.container['Assets/AssetManifest/AssetMaps/cards_map.asset'].read_typetree()['map']
        return {k: v.split(':')[1] for k, v in zip(data['keys'], data['values'])}
    
    @cached_property
    def base_assets_catalog(self):
        data = self._main_env.container['Assets/AssetManifest/base_assets_catalog.asset'].read_typetree()
        return {u['guid']: data['m_bundleNames'][u['bundleId']] for u in data['m_assets']}
    
    @cached_property
    def asset_catalog_locale(self):
        return AssetCatalogLocale(self._unity3d_folder)


class AssetLocaleEntry(TypedDict):
    guid: str
    bundle: str


class AssetLocaleMap(TypedDict):
    __root__: dict[str, AssetLocaleEntry]


class AssetCatalogLocale:
    def __init__(self, folder: os.PathLike[str] | str):
        self._unity3d_folder = Path(folder).resolve()
        self._cache = {}
    
    def __getitem__(self, locale: str) -> dict[str, AssetLocaleEntry]:
        locale = locale.lower()
        if locale in self._cache:
            return self._cache[locale]
        path = self._unity3d_folder / f'asset_manifest_{locale[:2]}{locale[-2:].upper()}.unity3d'
        
        result = {}
        if not path.exists():
            logging.warning(f"File not found: {path}. Make sure the locale '{locale}' is correct.")
        else:
            env = UnityPy.load(path.as_posix())
            data = env.container[f'Assets/AssetManifest/asset_catalog_locale_{locale}.asset'].read_typetree()
            
            result = {
                u['baseGuid']: {
                    'guid': u['guid'],
                    'bundle': data['m_bundleNames'][u['bundleId']],
                }
                for u in data['m_assets']
            }
        self._cache[locale] = result
        return result
