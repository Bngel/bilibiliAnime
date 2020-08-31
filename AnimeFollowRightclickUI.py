from PyQt5.QtWidgets import QWidget,QApplication,QPushButton
from PyQt5.QtGui import QPixmap,QPainter,QIcon
from PyQt5.QtCore import Qt
from AnimeFollow import Follow
from AnimeWatched import Watched
from AnimeMessageBox import Messagebox
import sys
import winsound

class FollowRightclick(QWidget):

    def __init__(self):
        super().__init__()
        right_bk_pic_path = './source/pic/rightclick_bk.png'
        right_bt_pic_3_path = './source/pic/right_3.png'
        right_bt_pic_2_path = './source/pic/right_2.png'
        right_bt_pic_3_1_path = './source/pic/right_3_1.png'
        right_bt_pic_3_2_path = './source/pic/right_3_2.png'
        right_bt_pic_2_1_path = './source/pic/right_2_1.png'
        right_bt_pic_2_2_path = './source/pic/right_2_2.png'
        rem_ico_path = './source/pic/rem.png'
        self.pix = QPixmap(right_bk_pic_path)
        self.resize(self.pix.width(),self.pix.height())
        self.pix = self.pix.scaled(int(self.pix.width()),int(self.pix.height()))
        self.setMask(self.pix.mask())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(rem_icon)
        self.delfollow = QPushButton(self)
        self.delfollow.setObjectName('DelFollow')
        self.delfollow.setGeometry(25, 50, 100, 40)
        self.delfollow.setStyleSheet('#DelFollow{border-image:url(%s)}'
                                     '#DelFollow:hover{border-image:url(%s)}'
                                     '#DelFollow:pressed{border-image:url(%s)}'
                                     % (right_bt_pic_3_path,right_bt_pic_3_1_path,right_bt_pic_3_2_path))
        self.delfollow.clicked.connect(self.deleteFollow)
        self.addwatched = QPushButton(self)
        self.addwatched.setObjectName('AddWatched')
        self.addwatched.setGeometry(25,100,100,40)
        self.addwatched.setStyleSheet('#AddWatched{border-image:url(%s)}' 
                                      '#AddWatched:hover{border-image:url(%s)}'
                                      '#AddWatched:pressed{border-image:url(%s)}'
                                      % (right_bt_pic_2_path,right_bt_pic_2_1_path,right_bt_pic_2_2_path))
        self.addwatched.clicked.connect(self.addWatched)
        self.rightclick_show = False
        self.title = ''
        self.msg = Messagebox()

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawPixmap(0,0,self.width(),self.height(),self.pix)

    def deleteFollow(self):
        follow = Follow()
        existed = follow.FollowDelete(self.title)
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

    def addWatched(self):
        watched = Watched()
        follow = Follow()
        existed = watched.WatchedInsert({'title':self.title})
        if existed:
            self.msg.setText('添加番剧成功')
            follow.FollowDelete(self.title)
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
    win = FollowRightclick()
    win.show()
    sys.exit(app.exec_())