# -*- mode: python -*-

block_cipher = None


a = Analysis(['expresso_gui.py'],
             pathex=['C:\\Users\\Saumya\\V_expresso\\expresso_python_api\\expresso\\gui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='expresso_gui',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
