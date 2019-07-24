# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['exp.py'],
             pathex=['C:\\Users\\georg\\src\\symmetry'],
             binaries=[],
             datas=[('start.txt', '.'),('end.txt', '.'),('break.txt', '.'),('feedback_correct.txt', '.'),('feedback_incorrect.txt', '.'),('mask.png', '.')],
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
          name='exp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='exp')
