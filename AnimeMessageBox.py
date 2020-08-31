from PyQt5.QtWidgets import QWidget,QApplication,QLabel
from PyQt5.QtGui import QPixmap,QPainter,QFontDatabase,QFont,QIcon
from PyQt5.QtCore import Qt
import sys

class Messagebox(QWidget):

    def __init__(self):
        super().__init__()
        msg_box_bk_pic_path = './source/pic/MessageBox.png'
        hgzy_font_path = './source/font/HGZY_CNKI.TTF'
        rem_ico_path = './source/pic/rem.png'
        fontId = QFontDatabase.addApplicationFont(hgzy_font_path)
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        self.pix = QPixmap(msg_box_bk_pic_path)
        self.resize(self.pix.width(),self.pix.height())
        self.pix = self.pix.scaled(int(self.pix.width()),int(self.pix.height()))
        #self.move(parent.x()+(parent.width()-self.pix.width())/2,self.y()+(parent.height()-self.pix.height())/2)
        self.setMask(self.pix.mask())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(rem_icon)
        self.msgtext = QLabel(self)
        self.msgtext.setObjectName('MsgLabel')
        self.msgtext.setFont(QFont(fontName,10,QFont.Light))
        self.msgtext.setGeometry(40,78,self.width(),self.height()-100)
        self.msgtext.setStyleSheet('#MsgLabel{color:#e368b9}')
        self.m_DragPosition = None
        self.m_drag = False

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawPixmap(0,0,self.pix.width(),self.pix.height(),self.pix)

    def mouseDoubleClickEvent(self, event):
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    def setText(self,msg):
        self.msgtext.setText('       ' + msg + '\n\n' + '<<双击窗口关闭提示框>>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Messagebox()
    win.show()
    sys.exit(app.exec_())