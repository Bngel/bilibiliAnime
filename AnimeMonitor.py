from PyQt5.QtWidgets import QWidget,QLabel,QApplication
from PyQt5.QtGui import QPixmap,QFont,QFontDatabase
from PyQt5.QtCore import Qt,QTimer
from AnimeTimeline import TimeLine
import sys
import time

class Monitor(QWidget):

    def __init__(self):
        super(Monitor, self).__init__()
        tool_bk_pic_path = './source/pic/tool_bk.png'
        hgzy_font_path = './source/font/HGZYT_CNKI.TTF'
        fontId = QFontDatabase.addApplicationFont(hgzy_font_path)
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        self.pix = QPixmap(tool_bk_pic_path)
        self.setGeometry(200,50,2500,200)
        self.setMask(self.pix.mask())
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.textlabel = QLabel(self)
        self.textlabel.setObjectName('TextLabel')
        self.textlabel.setText('')
        self.textlabel.resize(2500,200)
        self.textlabel.setFont(QFont(fontName,23,QFont.Bold))
        self.textlabel.setStyleSheet('#TextLabel{color:#F5A647}')
        self.opa = 1
        self.timeline = TimeLine()
        self.titles = self.timeline.get_today_anime()
        self.timer = QTimer()
        self.timer.timeout.connect(self.anime_monitor)
        self.timer.start(1000*60)
        self.opatime = QTimer()
        self.opatime.timeout.connect(self.anime_hide)

    def anime_monitor(self):
        cur_time = time.localtime()
        hour_min = '%02d:%02d' % (cur_time.tm_hour,cur_time.tm_min)
        for anime in self.titles:
            if hour_min in anime:
                self.textlabel.setText('开播啦!\t' + anime)
                self.opatime.start(100)
        print(hour_min)

    def anime_hide(self):
        self.show()
        if self.opa >= 1:
            self.opa += 0.02
            self.setWindowOpacity(self.opa)
            if self.opa >= 2:
                self.opa = 0.9
        elif self.opa > 0 and self.opa < 1:
            self.opa -= 0.02
            self.setWindowOpacity(self.opa)
        else:
            self.opatime.stop()
            self.opa = 1
            self.textlabel.setText('')
            self.setWindowOpacity(self.opa)
            self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Monitor()
    win.show()
    sys.exit(app.exec_())