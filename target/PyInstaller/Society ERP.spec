# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['D:\\Sudhanshu\\pycharm\\societyERP\\src\\main\\python\\Society_ERP\\ui.py'],
             pathex=['D:\\Sudhanshu\\pycharm\\societyERP\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['D:\\Sudhanshu\\pycharm\\venv_society\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['D:\\Sudhanshu\\pycharm\\societyERP\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [('v', None, 'OPTION')],
          exclude_binaries=True,
          name='Society ERP',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True , icon='D:\\Sudhanshu\\pycharm\\societyERP\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='Society ERP')
