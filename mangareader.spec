# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['reader.py'],
             pathex=['D:\\Documents\\GitHub\\html-mangareader'],
             binaries=[],
             datas=[('mangareader\\styles.css', 'mangareader'), ('mangareader\\menu.svg', 'mangareader'), ('mangareader\\menu-light.svg', 'mangareader'), ('mangareader\\scroll.svg', 'mangareader'), ('mangareader\\scroll-light.svg', 'mangareader'), ('mangareader\\boot.template.html', 'mangareader'), ('mangareader\\doc.template.html', 'mangareader'), ('mangareader\\img.template.html', 'mangareader'), ('mangareader\\scripts.js', 'mangareader'), ('mangareader\\roboto-regular.woff2', 'mangareader'), ('mangareader\\roboto-bold.woff2', 'mangareader'), ('mangareader\\zenscroll.js', 'mangareader'), ('version', '.'), ('unrar.exe', '.')],
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
          name='mangareader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='icon\\air1.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='mangareader')
