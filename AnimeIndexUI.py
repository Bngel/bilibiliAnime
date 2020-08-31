from PyQt5.QtWidgets import QWidget,QDesktopWidget,QApplication,QListWidget,QListWidgetItem,QPushButton,QLabel
from PyQt5.QtGui import QPixmap,QPainter,QFont,QIcon,QFontDatabase
from PyQt5.QtCore import Qt,QSize
import sys
from AnimeChooseUI import Choose
from AnimeDataLoad import AnimeData
from AnimeDetailUI import Detail
from AnimeVersion import Version
import pyperclip
from AnimeRightclickUI import Rightclick

class AnimeIndexWindow(QWidget):

    def __init__(self):
        super().__init__()
        anime_bk_pic_path = './source/pic/anime_bk.png'
        search_1_pic_path = './source/pic/next.png'
        search_2_pic_path = './source/pic/next_1.png'
        search_3_pic_path = './source/pic/next_2.png'
        hgzy_font_path = './source/font/HGZYT_CNKI.TTF'
        rem_ico_path = './source/pic/rem.png'
        self.pix = QPixmap(anime_bk_pic_path)
        self.resize(self.pix.width(),self.pix.height())
        self.pix = self.pix.scaled(int(self.pix.width()), int(self.pix.height()))
        self.setMask(self.pix.mask())
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.pix.width()) / 2, (screen.height() - self.pix.height()) / 2)
        self.setWindowFlags(Qt.FramelessWindowHint)  # | QtCore.Qt.WindowStaysOnTopHint
        self.setAttribute(Qt.WA_TranslucentBackground) # 窗口透明抗锯齿
        rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(rem_icon)
        self.m_DragPosition = None
        fontId = QFontDatabase.addApplicationFont(hgzy_font_path)
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        self.animelist = QDListWidget(self)
        self.animelist.setObjectName('AnimeListWidget')
        self.animelist.setGeometry(17,280,self.pix.width()-34,self.pix.height()-280-50)
        self.animelist.setStyleSheet('#AnimeListWidget{background:transparent;}')
        self.animelist.setFont(QFont(fontName,15,QFont.Light))
        self.animelist.setIconSize(QSize(100,100))
        self.InitData()
        ver = Version()
        self.version = QDLabel(self, ver.cur_link)
        self.version.setObjectName('VersionLabel')
        self.version.setGeometry(15, self.pix.height() - 75, 600, 100)
        self.version.setText('当前数据库版本号:' + ver.cur_version)
        if ver.judge_version():
            self.version.setToolTip('数据库为最新版本,无需更新')
        else:
            self.version.setToolTip('数据库版本已过期,请自行下载新数据库.(双击获取下载链接)')
        self.version.setFont(QFont(fontName,10,QFont.Light))
        self.search = QPushButton(self)
        self.search.setObjectName('Search')
        self.search.setStyleSheet("#Search{border-image: url(%s)}"
                                  "#Search:hover{border-image: url(%s)}" 
                                  "#Search:pressed{border-image: url(%s)}"
                                  % (search_1_pic_path,search_2_pic_path,search_3_pic_path))
        self.search.setGeometry(self.pix.width()-self.search.width(),self.pix.height()-self.search.height()-10
                                ,self.search.width()-20,self.search.height())
        self.choose = Choose(self.x()+self.width(),self.y()+self.height())
        self.choose_show = False
        self.choose_info = {}
        self.search.clicked.connect(self.SearchBt)
        self.detail = Detail(self.x(),self.y())
        self.detail_show = False
        self.animelist.itemDoubleClicked.connect(self.DetailBt)
        self.animelist.installEventFilter(self)
        self.rightclick = Rightclick()
        self.animeshow = False

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawPixmap(0,0,self.pix.width(),self.pix.height(),self.pix)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            if self.choose_show == True:
                self.choose.raise_()
            if self.detail_show == True:
                self.detail.raise_()
            event.accept()
        elif event.button() == Qt.RightButton:
            if self.detail_show == True:
                self.detail.close()
                self.detail_show = False
            if self.choose_show == True:
                self.choose.close()
                self.choose_show = False
            self.hide()
            self.animeshow = False
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            self.choose.move(self.x() + self.width(), self.y()+self.height()-self.choose.pix.height())
            self.detail.move(self.x()-self.detail.pix.width(),self.y())
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    def closeEvent(self, event):
        self.detail.close()
        self.detail_show = False
        self.choose.close()
        self.choose_show = False
        self.animeshow = False

    def InitData(self):
        dbsql = AnimeData()
        self.infos = dbsql.SqliteInfoSelect()
        self.animelist.clear()
        if self.infos:
            for info in self.infos:
                self.animelist.addItem(QListWidgetItem(QIcon('./source/pic/bili.png'), info[0]))

    def ChooseData(self):
        self.choose_info = {}
        title = self.choose.titletext.text()
        if title != '':
            self.choose_info['title'] = title
        order = self.choose.ordertext.text()
        if order != '':
            self.choose_info['order'] = int(order)
        index_show = ''
        index_season = self.choose.animecombo_season.currentText()
        index_year = self.choose.timetext.text()
        if index_year != '':
            index_show += index_year + '年'
        if index_season != '不筛选':
            index_show += index_season
        if index_show != '':
            self.choose_info['index_show'] = index_show
        novip = self.choose.animevip.checkState()
        if novip == 1:
            self.choose_info['vip'] = 1
        elif novip == 2:
            self.choose_info['vip'] = 0
        finish = self.choose.animefinish.checkState()
        if finish == 1:
            self.choose_info['finish'] = 0
        elif finish == 2:
            self.choose_info['finish'] = 1
        tags = []
        for i in range(3):
            tag = self.choose.animetags[i].currentText()
            if tag != '不筛选':
                tags.append(tag)
        if tags != []:
            self.choose_info['tag'] = tags

    def ShowData(self):
        dbsql = AnimeData()
        self.infos = dbsql.SqliteInfoSearch(self.choose_info)
        self.animelist.clear()
        if self.infos:
            for info in self.infos:
                self.animelist.addItem(QListWidgetItem(QIcon('./source/pic/bili.png'), info[0]))
        else:
            self.InitData()

    def SearchBt(self):
        if self.choose_show == False:
            self.choose.show()
            self.choose_show = True
        else:
            self.choose.close()
            self.ChooseData()
            self.ShowData()
            self.choose_show = False

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
            info = self.GetDetail(self.animelist.currentItem().text())
            self.animelist.index = self.animelist.currentIndex()
            self.detail.setInfo(info)
            self.detail.show()
            self.detail_show = True
        elif self.detail_show == True and self.animelist.index != self.animelist.currentIndex():
            self.detail.close()
            self.DelDetail()
            info = self.GetDetail(self.animelist.currentItem().text())
            self.animelist.index = self.animelist.currentIndex()
            self.detail.setInfo(info)
            self.detail.show()
        else:
            self.detail.close()
            self.DelDetail()
            self.animelist.index = -1
            self.detail_show = False

class QDLabel(QLabel):

    def __init__(self,parent,link):
        super(QDLabel,self).__init__(parent)
        self.link = link

    def mouseDoubleClickEvent(self, event):
        if self.text() == '数据库版本已过期,请自行下载新数据库.(双击获取下载链接)':
            pyperclip.copy(self.link)
            self.setText('下载链接已置入剪贴板')
            event.accept()

class QDListWidget(QListWidget):

    def __init__(self,parent):
        super(QDListWidget, self).__init__(parent)
        self.rightclick_show = False
        self.index = -1

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            row = self.currentIndex().row()
            if row != -1:
                if self.parent().rightclick.rightclick_show == False:
                    self.parent().rightclick.move(event.globalPos())
                    self.parent().rightclick.title = self.currentItem().text()
                    self.parent().rightclick.show()
                    self.parent().rightclick.rightclick_show = True
                else:
                    self.parent().rightclick.close()
                    self.parent().rightclick.move(event.globalPos())
                    self.parent().rightclick.title = self.currentItem().text()
                    self.parent().rightclick.show()
        if event.button() == Qt.LeftButton:
            super().mousePressEvent(event)

    def focusInEvent(self, event):
        self.parent().rightclick.close()
        self.parent().rightclick_show = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AnimeIndexWindow()
    win.show()
    sys.exit(app.exec_())