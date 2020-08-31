from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
import sys
from PIL import Image
from AnimeIndexUI import AnimeIndexWindow
from AnimeFollowIndexUI import FollowIndexWindow
from AnimeWatchedIndexUI import WatchedIndexWindow
from AnimeTimelineIndexUI import TimelineWindow

class ToolWindow(QWidget):

    def __init__(self,start_x,start_y):
        super().__init__()
        tool_bk_pic_path = './source/pic/tool_bk.png'
        anime_pic_path = './source/pic/Anime.png'
        follow_pic_path = './source/pic/Follow.png'
        watched_pic_path = './source/pic/Watched.png'
        timeline_pic_path = './source/pic/Timeline.png'
        rem_ico_path = './source/pic/rem.png'
        tool_pic = Image.open(anime_pic_path)
        tool_size = tool_pic.size
        tool_bk_pic = Image.open(tool_bk_pic_path)
        tool_bk_size = tool_bk_pic.size
        pic_between = 20

        self.setObjectName('ToolWindow')
        self.setGeometry(start_x,start_y,tool_bk_size[1],tool_bk_size[0])

        self.animelist = QPushButton(self)
        self.animelist.setObjectName('AnimeList')
        self.animelist.setStyleSheet('#AnimeList\n{border-image:url(%s);\n}' % anime_pic_path)
        self.animelist.setGeometry(QtCore.QRect(0, tool_size[1]*0, tool_size[0], tool_size[1]))
        self.animelist.setCursor(Qt.PointingHandCursor)
        self.animelist.clicked.connect(self.AnimeListBt)
        self.animelist.setToolTip('番剧索引')
        self.followlist = QPushButton(self)
        self.followlist.setObjectName('FollowList')
        self.followlist.setStyleSheet('#FollowList\n{border-image:url(%s);\n}' % follow_pic_path)
        self.followlist.setGeometry(QtCore.QRect(0, tool_size[1]+pic_between, tool_size[0], tool_size[1]))
        self.followlist.setCursor(Qt.PointingHandCursor)
        self.followlist.clicked.connect(self.FollowListBt)
        self.followlist.setToolTip('追番列表')
        self.watchedlist = QPushButton(self)
        self.watchedlist.setObjectName('WatchedList')
        self.watchedlist.setStyleSheet('#WatchedList\n{border-image:url(%s);\n}' % watched_pic_path)
        self.watchedlist.setGeometry(QtCore.QRect(0, (tool_size[0]+pic_between)*2, tool_size[0], tool_size[1]))
        self.watchedlist.setCursor(Qt.PointingHandCursor)
        self.watchedlist.clicked.connect(self.WatchedListBt)
        self.watchedlist.setToolTip('"完追"列表')
        self.timelinelist = QPushButton(self)
        self.timelinelist.setObjectName('TimelineList')
        self.timelinelist.setStyleSheet('#TimelineList\n{border-image:url(%s);\n}' % timeline_pic_path)
        self.timelinelist.setGeometry(QtCore.QRect(0, (tool_size[0]+pic_between)*3, tool_size[0], tool_size[1]))
        self.timelinelist.setCursor(Qt.PointingHandCursor)
        self.timelinelist.clicked.connect(self.TimelineBt)
        self.timelinelist.setToolTip('每日新番表')

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(rem_icon)

        self.anime = AnimeIndexWindow()
        self.follow = FollowIndexWindow()
        self.watched = WatchedIndexWindow()
        self.timeline = TimelineWindow()

    def AnimeListBt(self):
        if self.anime.animeshow == False:
            self.anime.show()
            self.anime.animeshow = True
        else:
            self.anime.close()
            self.anime.animeshow = False

    def FollowListBt(self):
        if self.follow.followshow == False:
            self.follow.show()
            self.follow.followshow = True
        else:
            self.follow.close()
            self.follow.followshow = False

    def WatchedListBt(self):
        if self.watched.watchedshow == False:
            self.watched.show()
            self.watched.watchedshow = True
        else:
            self.watched.close()
            self.watched.watchedshow = False

    def TimelineBt(self):
        if self.timeline.timelineshow == False:
            self.timeline.show()
            self.timeline.timelineshow = True
        else:
            self.timeline.close()
            self.timeline.timelineshow = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ToolWindow(1000,200)
    win.show()
    sys.exit(app.exec_())