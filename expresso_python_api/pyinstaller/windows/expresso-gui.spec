# -*- mode: python -*-
a = Analysis(['C:\\Users\\xisco\\Work\\expresso_device_software\\expresso_python_api\\expresso\\bin\\expresso-gui'],
             pathex=['C:\\Users\\xisco\\Work\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('build\\pyi.win32\\expresso-gui', 'expresso-gui.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False )
