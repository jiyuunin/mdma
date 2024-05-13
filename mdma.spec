a = Analysis(
    ['mdma/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('mdma/config.yml', '.'),
        ('mdma/fonts/*', '.'),
        ('mdma/graphics/*', '.')
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
    # For some reason, PyInstaller does not include the data files without this
    # line.
    Tree('mdma/'),
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='mdma',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='mdma/graphics/icon.ico'
)
