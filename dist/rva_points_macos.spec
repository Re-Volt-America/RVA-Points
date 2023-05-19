# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['../rva_points.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='rva_points',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='rva_points')
app = BUNDLE(coll,
             name='RVA Points.app',
             icon='../icons/icon.icns',
             bundle_identifier=None,
             info_plist={
             'NSPrincipleClass': 'NSApplication',
             'NSAppleScriptEnabled': 'False',
             'NSHighResolutionCapable': 'True',
             'NSRequiresAquaSystemAppearance': 'False',
             'CFBundleDocumentTypes': [],
             'CFBundleName': 'RVA Points'
             })
