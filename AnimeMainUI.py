import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QApplication,QDesktopWidget,QSystemTrayIcon,QMenu,QAction,qApp
from PyQt5.QtGui import QPixmap,QPainter,QCursor,QIcon
from AnimeToolUI import ToolWindow
from AnimeMonitor import Monitor

class RemMainWindow(QWidget):

    def __init__(self):
        super().__init__()
        rem_bk_pic_path = './source/pic/rem_bk.png'
        rem_ico_path = './source/pic/rem.png'
        self.pix = QPixmap(rem_bk_pic_path)
        self.resize(self.pix.width(),self.pix.height())
        self.pix = self.pix.scaled(int(self.pix.width()),int(self.pix.height()))
        self.setMask(self.pix.mask())
        screen = QDesktopWidget().screenGeometry()
        self.move(screen.width()-self.pix.width()*2,screen.height()-self.pix.height()*2)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.rem_icon = QIcon(QPixmap(rem_ico_path))
        self.setWindowIcon(self.rem_icon)
        self.m_DragPosition = None
        self.tool = ToolWindow(self.x() + self.width(), self.y())
        self.tool_enable = False
        self.monitor = Monitor()

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.drawPixmap(0,0,self.pix.width(),self.pix.height(),self.pix)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            if self.tool_enable:
                self.tool.raise_()
        if event.button() == Qt.RightButton:
            if self.tool_enable == True:
                self.tool.close()
                self.tool_enable = False
            self.trayEvent()

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos()-self.m_DragPosition)
            self.tool.move(self.x() + self.width(), self.y())
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, event):
        if self.tool_enable == False:
            self.tool.show()
            self.tool_enable = True
        else:
            self.tool.close()
            self.tool_enable = False

    def closeEvent(self, event):
        if self.tool_enable == True:
            self.tool.close()

    def trayEvent(self):
        self.hide()
        self.mSysTrayIcon = QSystemTrayIcon(self)
        self.mSysTrayIcon.setIcon(self.rem_icon)
        self.mSysTrayIcon.setToolTip("追番小工具")
        self.mSysTrayIcon.activated.connect(self.onActivated)
        self.tray_menu = QMenu(QApplication.desktop())
        self.quitAction = QAction(u'退出',self,triggered=qApp.quit)
        self.tray_menu.addAction(self.quitAction)
        self.mSysTrayIcon.setContextMenu(self.tray_menu)
        self.mSysTrayIcon.show()

    def onActivated(self, reason):
        if reason == self.mSysTrayIcon.Trigger:
            self.show()
            self.mSysTrayIcon.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RemMainWindow()
    win.show()
    sys.exit(app.exec_())