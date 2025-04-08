# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\nortt.html', '.'), ('C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\login.html', '.'), ('C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\nortt.css', '.'), ('C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\nortt.js', '.'), ('C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\nortt.ico', '.'), ('C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\background.png', '.'), ('C:\\Users\\qwe\\Desktop\\FlaskApiSystem3\\nortt.yaml', '.')],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
