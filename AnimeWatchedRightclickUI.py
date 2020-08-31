from PyQt5.QtWidgets import QWidget,QApplication,QPushButton
from PyQt5.QtGui import QPixmap,QPainter,QIcon
from PyQt5.QtCore import Qt
from AnimeFollow import Follow
from AnimeWatched import Watched
from AnimeMessageBox import Messagebox
import sys
import winsound

class WatchedRightclick(QWidget):

    def __init__(self):
        super().__init__()
        right_bk_pic_path = './source/pic/rightclick_bk.png'
        right_bt_pic_4_path = './source/pic/right_4.png'
        right_bt_pic_5_path = './source/pic/right_5.png'
        right_bt_pic_4_1_path = './source/pic/right_4_1.png'
        right_bt_pic_4_2_path = './source/pic/right_4_2.png'
        right_bt_pic_5_1_path = './source/pic/right_5_1.png'
        right_bt_pic_5_2_path = './source/pic/right_5_2.png'
        rem_ico_path = './source/pic/rem.png'
        self.pix = QPixmap(right_bk_pic_path)
        self.resize(self.pix.width(),self.pix.height())
        self.pix = self.pix.scaled(int(self.pix.width()),int(self.pix.height()))
        self.setMask(self.pix.mask())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(rem_icon)
        self.setWindowIcon(rem_icon)
        self.addfollow = QPushButton(self)
        self.addfollow.setObjectName('AddFollow')
        self.addfollow.setGeometry(25, 50, 100, 40)
        self.addfollow.setStyleSheet('#AddFollow{border-image:url(%s)}'
                                     '#AddFollow:hover{border-image:url(%s)}'
                                     '#AddFollow:pressed{border-image:url(%s)}'
                                     % (right_bt_pic_4_path,right_bt_pic_4_1_path,right_bt_pic_4_2_path))
        self.addfollow.clicked.connect(self.deleteWatched)
        self.delwatched = QPushButton(self)
        self.delwatched.setObjectName('DelWatched')
        self.delwatched.setGeometry(25,100,100,40)
        self.delwatched.setStyleSheet('#DelWatched{border-image:url(%s)}' 
                                      '#DelWatched:hover{border-image:url(%s)}'
                                      '#DelWatched:pressed{border-image:url(%s)}'
                                      % (right_bt_pic_5_path,right_bt_pic_5_1_path,right_bt_pic_5_2_path))
        self.delwatched.clicked.connect(self.addFollow)
        self.rightclick_show = False
        self.title = ''
        self.msg = Messagebox()

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawPixmap(0,0,self.width(),self.height(),self.pix)

    def deleteWatched(self):
        watched = Watched()
        existed = watched.WatchedDelete(self.title)
        if existed:
            self.msg.setText('删除番剧成功')
            winsound.MessageBeep(1000)
            self.msg.show()
        else:
            self.msg.setText('番剧不存在')
            winsound.MessageBeep(1000)
            self.msg.show()
        self.close()
        self.rightclick_show = False
        #follow.FollowShow()

    def addFollow(self):
        follow = Follow()
        watched = Watched()
        existed = follow.FollowInsert({'title':self.title})
        if existed:
            self.msg.setText('添加追番成功')
            watched.WatchedDelete(self.title)
            winsound.MessageBeep(1000)
            self.msg.show()
        else:
            self.msg.setText('番剧已存在')
            winsound.MessageBeep(1000)
            self.msg.show()
        self.close()
        self.rightclick_show = False
        #watched.WatchedShow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WatchedRightclick()
    win.show()
    sys.exit(app.exec_())