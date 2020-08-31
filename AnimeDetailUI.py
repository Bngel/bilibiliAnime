from PyQt5.QtWidgets import QWidget,QApplication,QLabel,QFrame,QPushButton
from PyQt5.QtGui import QPixmap,QPainter,QFontDatabase,QFont,QIcon
from PyQt5.QtCore import Qt,QThread
import requests
import sys
import webbrowser

class Detail(QWidget):

    def __init__(self,win_x,win_y):
        super().__init__()
        detail_pic_bk_path = './source/pic/Anime_details_bk.png'
        rem_ico_path = './source/pic/rem.png'
        self.pix = QPixmap(detail_pic_bk_path)
        self.resize(self.pix.width(), self.pix.height())
        self.pix = self.pix.scaled(int(self.pix.width()), int(self.pix.height()))
        self.setMask(self.pix.mask())
        self.move(win_x-self.pix.width(),win_y)
        self.setWindowFlags(Qt.FramelessWindowHint)  # | QtCore.Qt.WindowStaysOnTopHint
        self.setAttribute(Qt.WA_TranslucentBackground) # 窗口透明抗锯齿
        rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(rem_icon)

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawPixmap(0,0,self.pix.width(),self.pix.height(),self.pix)

    def setInfo(self,info):
        hgzy_font_path = './source/font/HGZY_CNKI.TTF'
        no_pic_path = './source/pic/no_pic.png'
        jump_pic_path = './source/pic/jump_to_bili.png'
        jump_pic_path_1 = './source/pic/jump_to_bili_1.png'
        jump_pic_path_2 = './source/pic/jump_to_bili_2.png'
        fontId = QFontDatabase.addApplicationFont(hgzy_font_path)
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        #print(info)
        self.pic_size = (210,280)
        self.title = info[0]
        self.order = info[1]
        self.intro = info[2]
        self.index_show = info[3]
        self.tags = info[4]
        self.vip = info[5]
        self.url = info[6]
        self.link = info[7]
        self.img = Img(self.pic_size[0],self.pic_size[1],self.url)
        self.img.run(no_pic_path)
        label_height = 100
        label_width = 340
        label_start_x = 340
        label_start_y = 85
        label_between = 70
        self.pic_label = QLabel(self)
        self.pic_label.setObjectName('PicLabel')
        self.pic_label.setText('')
        self.pic_label.setGeometry(105,100,self.pic_size[0],self.pic_size[1])
        self.pic_label.setPixmap(self.img.img)
        self.animetitle = QLabel(self)
        self.animetitle.setObjectName('DetailTitle')
        self.animetitle.setFont(QFont(fontName,12,QFont.Light))
        self.animetitle.setText('番剧名称')
        self.animetitle.setGeometry(label_start_x,label_start_y+20,label_width,label_height)
        self.animetitle.setStyleSheet('#DetailTitle{color:#FFFFFF}')
        self.animetitle.setMaximumWidth(label_width)
        self.animetitle.adjustSize()
        self.animetitletext = QLabel(self)
        self.animetitletext.setObjectName('TitleText')
        self.animetitletext.setFont(QFont(fontName,12,QFont.Light))
        self.animetitletext.setText(self.title)
        self.animetitletext.setGeometry(label_start_x,self.animetitle.y()+self.animetitle.height()+10,label_width,label_height+label_between)
        self.animetitletext.setWordWrap(True)
        self.animetitletext.setMaximumWidth(label_width)
        self.animetitletext.adjustSize()
        self.animeorder = QLabel(self)
        self.animeorder.setObjectName('DetailOrder')
        self.animeorder.setFont(QFont(fontName,12,QFont.Light))
        self.animeorder.setText('追番人数')
        self.animeorder.setGeometry(label_start_x,self.animetitletext.y()+self.animetitletext.height()+10,label_width,label_height)
        self.animeorder.setStyleSheet('#DetailOrder{color:#FFFFFF}')
        self.animeorder.setMaximumWidth(label_width)
        self.animeorder.adjustSize()
        self.animeordertext = QLabel(self)
        self.animeordertext.setObjectName('OrderText')
        self.animeordertext.setFont(QFont(fontName, 12, QFont.Light))
        self.animeordertext.setText(self.order)
        self.animeordertext.setGeometry(label_start_x, self.animeorder.y()+self.animeorder.height()+10, label_width, label_height)
        self.animeordertext.setWordWrap(True)
        #self.animeordertext.setMaximumWidth(label_width)
        self.animeordertext.adjustSize()
        self.animetags = QLabel(self)
        self.animetags.setObjectName('DetailTags')
        self.animetags.setFont(QFont(fontName, 12, QFont.Light))
        self.animetags.setText('番剧风格')
        self.animetags.setGeometry(label_start_x,self.animeordertext.y()+self.animeordertext.height()+10,label_width,label_height)
        self.animetags.setStyleSheet('#DetailTags{color:#FFFFFF}')
        self.animetags.setMaximumWidth(label_width)
        self.animetags.adjustSize()
        self.animetagstext = QLabel(self)
        self.animetagstext.setObjectName('TagsText')
        self.animetagstext.setFont(QFont(fontName, 12, QFont.Light))
        self.animetagstext.setText(self.tags)
        self.animetagstext.setGeometry(label_start_x, self.animetags.y()+self.animetags.height()+10, label_width, label_height)
        self.animetagstext.setWordWrap(True)
        self.animetagstext.setMaximumWidth(label_width)
        self.animetagstext.adjustSize()
        self.animeindexshow = QLabel(self)
        self.animeindexshow.setObjectName('DetailIndex')
        self.animeindexshow.setFont(QFont(fontName, 12, QFont.Light))
        self.animeindexshow.setText('番剧时间')
        self.animeindexshow.setGeometry(label_start_x, self.animetagstext.y() + self.animetagstext.height() + 10,label_width, label_height)
        self.animeindexshow.setStyleSheet('#DetailIndex{color:#FFFFFF}')
        self.animeindexshow.setMaximumWidth(label_width)
        self.animeindexshow.adjustSize()
        self.animeindexshowtext = QLabel(self)
        self.animeindexshowtext.setObjectName('IndexText')
        self.animeindexshowtext.setFont(QFont(fontName, 10, QFont.Light))
        self.animeindexshowtext.setText(self.index_show)
        self.animeindexshowtext.setGeometry(label_start_x, self.animeindexshow.y() + self.animeindexshow.height() + 10, label_width,label_height)
        self.animeindexshowtext.setWordWrap(True)
        self.animeindexshowtext.setMaximumWidth(label_width)
        self.animeindexshowtext.adjustSize()
        self.animeintro = QLabel(self)
        self.animeintro.setObjectName('DetailIntro')
        self.animeintro.setFont(QFont(fontName, 13, QFont.Light))
        self.animeintro.setGeometry(105,self.pic_label.y()+self.pic_label.height()+10,label_width+10,label_height)
        self.animeintro.setStyleSheet('#DetailIntro{color:#fd8a9c}')
        self.animeintro.setText('番剧介绍\n(悬停此处可查看)')
        self.animeintro.setFrameShape(QFrame.Box)
        self.animeintro.setLineWidth(5)
        self.animeintro.setToolTip(self.intro)
        self.animeintro.adjustSize()
        self.jumpanime = QPushButton(self)
        self.jumpanime.setObjectName('JumptoBili')
        self.jumpanime.setGeometry(175,self.animeintro.y()+self.animeintro.height()+15,64,64)
        self.jumpanime.setStyleSheet('#JumptoBili{border-image:url(%s)}'
                                     '#JumptoBili:hover{border-image:url(%s)}'
                                     '#JumptoBili:pressed{border-image:url(%s)}'
                                     % (jump_pic_path,jump_pic_path_1,jump_pic_path_2))
        self.jumpanime.setCursor(Qt.PointingHandCursor)
        self.jumpanime.clicked.connect(self.JumptoBili)

    def JumptoBili(self):
        webbrowser.open(self.link)

class Img(QThread):

    def __init__(self,pic_x,pic_y,url):
        super().__init__()
        self.pic_x = pic_x
        self.pic_y = pic_y
        self.url = url

    def run(self,pic):
        if self.url:
            response = requests.get(self.url)
            self.img = QPixmap()
            self.img.loadFromData(response.content)
            self.img = self.img.scaled(self.pic_x, self.pic_y)
        else:
            self.img = QPixmap(pic)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    infos = ['辉夜大小姐想让我告白？～天才们的恋爱头脑战～','836.5 万','大正时期，日本。心地善良的卖炭少年·炭治郎，有一天他的家人被鬼杀死了。\n而唯一幸存下来的妹妹——祢豆子变成了鬼。被绝望的现实打垮的炭治郎，为了寻找让妹妹变回人类的方法，决心朝着“鬼杀队”的道路前进。\n人与鬼交织的悲哀的兄妹的故事，现在开始！'
        ,'2019年4月7日开播 已完结, 全26话','漫画改 战斗 热血 声控',1,'https://i0.hdslb.com/bfs/bangumi/9d9cd5a6a48428fe2e4b6ed17025707696eab47b.png','https://www.bilibili.com/bangumi/media/md22718131/']
    win = Detail(1419,1187)
    win.show()
    sys.exit(app.exec_())