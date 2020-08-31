from PyQt5.QtWidgets import QWidget,QApplication,QLabel,QListWidget,QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QPainter,QFontDatabase,QFont,QIcon
from AnimeTimeline import TimeLine
from AnimeDetailUI import Detail
from AnimeDataLoad import AnimeData
import sys

class TimelineWindow(QWidget):

    def __init__(self):
        super().__init__()
        timeline_bk_path = './source/pic/timeline_bk.png'
        hgzy_font_path = './source/font/HGZYT_CNKI.TTF'
        rem_ico_path = './source/pic/rem.png'
        fontId = QFontDatabase.addApplicationFont(hgzy_font_path)
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        self.index = -1
        self.pix = QPixmap(timeline_bk_path)
        self.resize(self.pix.width(),self.pix.height())
        self.pix = self.pix.scaled(int(self.pix.width()),int(self.pix.height()))
        self.setMask(self.pix.mask())
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.pix.width()) / 2, (screen.height() - self.pix.height()) / 2)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(rem_icon)
        self.m_DragPosition = None
        self.m_drag = False
        self.animelist = QListWidget(self)
        self.animelist.setObjectName('AnimeList')
        self.animelist.setStyleSheet('#AnimeList{background:transparent}')
        self.animelist.setGeometry(200,165,310,350)
        self.animelist.setFont(QFont(fontName,11,QFont.Light))
        self.detail = Detail(self.x()+50,self.y()-15)
        self.detail_show = False
        self.animelist.itemDoubleClicked.connect(self.DetailBt)
        self.TimeLabels_path = []
        self.TimeLabels_clicked_path = []
        self.weekanime = TimeLine().get_week_anime()
        for time in range(1,8):
            self.TimeLabels_path.append('./source/pic/week_day_%d.png' % time)
            self.TimeLabels_clicked_path.append('./source/pic/week_day_%d_clicked.png' % time)
        self.TimeLabels = []
        for time in range(7):
            self.TimeLabels.append(QDlabel(self))
        self.setTimeLabel()
        self.daylabel = QLabel(self)
        self.daylabel.setObjectName('DayLabel')
        self.daylabel.setGeometry(290,110,200,40)
        self.daylabel.setFont(QFont(fontName,13,QFont.Bold))
        self.setDaytext()
        self.timelineshow = False

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawPixmap(0,0,self.pix.width(),self.pix.height(),self.pix)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            if self.detail_show == True:
                self.detail.raise_()
            event.accept()
        elif event.button() == Qt.RightButton:
            if self.detail_show == True:
                self.detail.close()
                self.detail_show = False
            self.hide()
            self.timelineshow = False
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            self.detail.move(self.x()+50 - self.detail.pix.width(),self.y()-15)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    def closeEvent(self, event):
        self.detail.close()
        self.detail_show = False
        self.timelineshow = False

    def setTimeLabel(self):
        label_between = 60
        week_animes = self.weekanime
        start = week_animes[0]['day_of_week']-1
        for time in range(start,start+7):
            time_mod = time % 7
            self.TimeLabels[time_mod].setObjectName('DayLabel%d' % (time_mod+1))
            self.TimeLabels[time_mod].setStyleSheet('#DayLabel%d{border-image:url(%s)}' % (time_mod+1,self.TimeLabels_path[time_mod]))
            self.TimeLabels[time_mod].setGeometry(100,120 + label_between * (time-start),57,24)
        self.labelclick = week_animes[0]['day_of_week']
        self.TimeLabels[self.labelclick-1].setStyleSheet('#DayLabel%d{border-image:url(%s)}'
                                                         % (self.labelclick,self.TimeLabels_clicked_path[self.labelclick-1]))

    def setLabelClick(self, time_n):
        self.TimeLabels[self.labelclick-1].setStyleSheet(
            '#DayLabel%d{border-image:url(%s)}' % (self.labelclick, self.TimeLabels_path[self.labelclick-1]))
        self.TimeLabels[time_n].setStyleSheet('#DayLabel%d{border-image:url(%s)}'
                                                         % (time_n+1,self.TimeLabels_clicked_path[time_n]))

    def setDaytext(self):
        for animes in self.weekanime:
            if animes['day_of_week'] == self.labelclick:
                date = animes['date']
                day_of_week = self.labelclick
                self.animelist.clear()
                for anime in animes['seasons']:
                    item_text = ''
                    if anime['delay'] == 1:
                        item_text += anime['pub_time'] + ' ' + anime['delay_index'] + ' ' + anime['delay_reason'] + '\n' + anime['title']
                    else:
                        item_text += anime['pub_time'] + ' ' + anime['pub_index'] + '\n' + anime['title']
                    self.animelist.addItem(item_text)
                break
        week_day = ['周一','周二','周三','周四','周五','周六','周日']
        daytext = date + ' ' + week_day[day_of_week - 1]
        self.daylabel.setText(daytext)

    def GetDetail(self,title):
        dbsql = AnimeData()
        infos = dbsql.SqliteInfoSearch({'title':title})
        resinfo = []
        if infos:
            for info in infos:
                resinfo.append(info[0])
                resinfo.append(info[1])
                resinfo.append(info[2])
                resinfo.append(info[3])
                resinfo.append(info[4])
                resinfo.append(info[5])
                resinfo.append(info[6])
                resinfo.append(info[7])
        return resinfo

    def DelDetail(self):
        self.detail.animetitle.setParent(None)
        self.detail.animeintro.setParent(None)
        self.detail.animetags.setParent(None)
        self.detail.animeorder.setParent(None)
        self.detail.animeindexshow.setParent(None)
        self.detail.animeindexshowtext.setParent(None)
        self.detail.animetagstext.setParent(None)
        self.detail.animeordertext.setParent(None)
        self.detail.animetitletext.setParent(None)
        self.detail.animetagstext.setParent(None)
        self.detail.pic_label.setParent(None)

    def DetailBt(self):
        if self.detail_show == False:
            title = self.animelist.currentItem().text().split('\n')[1]
            info = self.GetDetail(title)
            self.detail.setInfo(info)
            self.index = self.animelist.currentIndex()
            self.detail.show()
            self.detail_show = True
        elif self.detail_show == True and self.index != self.animelist.currentIndex():
            self.detail.close()
            self.DelDetail()
            title = self.animelist.currentItem().text().split('\n')[1]
            info = self.GetDetail(title)
            self.index = self.animelist.currentIndex()
            self.detail.setInfo(info)
            self.detail.show()
        else:
            self.detail.close()
            self.DelDetail()
            self.index = -1
            self.detail_show = False

class QDlabel(QLabel):

    def __init__(self,parent):
        super(QDlabel,self).__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            time = int(self.objectName()[-1:])
            self.parent().setLabelClick(time - 1)
            self.parent().labelclick = time
            self.parent().setDaytext()
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TimelineWindow()
    win.show()
    sys.exit(app.exec_())