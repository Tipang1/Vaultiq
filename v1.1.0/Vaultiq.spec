# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['D:/Benjamin/Documents/Projets code/Python/1 mois 1 fonction/2026/Vaultiq/v1.1.0/main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Benjamin/Documents/Projets code/Python/1 mois 1 fonction/2026/Vaultiq/v1.1.0/assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Vaultiq',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='D:/Benjamin/Documents/Projets code/Python/1 mois 1 fonction/2026/Vaultiq/v1.1.0/assets/icon.png',
)
