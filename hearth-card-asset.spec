# -*- mode: python ; coding: utf-8 -*-
import os
import UnityPy

def get_unitypy_path() -> str:
    return os.path.dirname(UnityPy.__file__)

unitypy_path = get_unitypy_path()
unitypy_resources_src = os.path.join(unitypy_path, 'resources')

a = Analysis(
    ['src\\cli.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        (unitypy_resources_src, 'UnityPy/resources')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='hearth-card-asset',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
