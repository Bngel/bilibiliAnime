# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

py_files = [
'./AnimeMainUI.py','./AnimeDataLoad.py','./AnimeDetailUI.py',
'./AnimeFollow.py','./AnimeFollowIndexUI.py','./AnimeFollowRightclickUI.py',
'./AnimeIndexUI.py','./AnimeChooseUI.py','./AnimeMessageBox.py','./AnimeRecommend.py',
'./AnimeRightclickUI.py','./AnimeSpider.py','./AnimeTimeline.py','./AnimeTimelineIndexUI.py',
'./AnimeToolUI.py','./AnimeVersion.py','./AnimeWatched.py','./AnimeWatchedIndexUI.py',
'./AnimeWatchedRightclickUI.py','./ipSpider.py'
]

a = Analysis(py_files,
             pathex=['D:\\git\\Python\\项目\\blilibiliAnime'],
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

def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
a.datas += extra_datas('source')
a.datas += extra_datas('data')
a.datas += extra_datas('database')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='RemAnime',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='./source/pic/rem.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='AnimeMainUI')
