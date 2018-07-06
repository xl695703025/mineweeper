import random

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

LEVELS = [
    (8, 10),
    (16, 40),
    (24, 99)
]

class Pos(QWidget):
    def __init__(self,window, x, y, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))
        self.is_mine = False  # 是否是雷
        self.adjacent_n = 0 # 周边的雷数

        self.is_revealed = False  # 是否已翻转
        self.is_flagged = False  # 是否已做标记
        self.x = x
        self.y = y
        self.window=window

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rectArea = event.rect()
        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray

        painter.fillRect(rectArea, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(rectArea)

        if self.is_revealed:
            if self.is_mine:
                pen = QPen(QColor('#3F51B5'))
                painter.setPen(pen)
                f = painter.font()
                f.setBold(True)
                painter.setFont(f)
                painter.drawText(rectArea, Qt.AlignHCenter | Qt.AlignVCenter, 'M')
            elif self.adjacent_n > 0:
                pen = QPen(QColor('#f44336'))
                painter.setPen(pen)
                f = painter.font()
                f.setBold(True)
                painter.setFont(f)
                painter.drawText(rectArea, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))
        elif self.is_flagged:
            painter.drawPixmap(rectArea, QPixmap(QImage("./images/flag.png")))


    def reveal_it(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal_it()
            self.window.safeNum-=1

    def flag_it(self):
        self.is_flagged = True
        self.update()

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            if(self.window.start==False):
                self.window.start=True
                self.window.timer.start()
                self.window.init()
            self.click()
            if self.is_mine :
                QMessageBox.information(self, "提示信息", "GameOver~!", QMessageBox.Yes)
            elif self.adjacent_n==0:
                self.safeArea(self.x,self.y)
            if self.window.safeNum==0:
                self.window.timer.stop()
                QMessageBox.information(self, "提示信息", "You Win~!完成时间为"+str(self.window.count)+"s", QMessageBox.Yes)
        elif (event.button() == Qt.RightButton and not self.is_revealed):
            if self.is_flagged:
                self.is_flagged=False
                self.window.n_mines = self.window.n_mines + 1
                self.window.lbl_mines.setText("%03d" % self.window.n_mines)
                self.update()
            else:
                self.flag_it()
                self.window.n_mines=self.window.n_mines-1
                self.window.lbl_mines.setText("%03d" % self.window.n_mines)
    def  safeArea(self,x,y):
        if (x > 0):
            w=self.window.grid_mines.itemAtPosition(y, x-1).widget()
            if(w.is_revealed==False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x,w.y)
        if (x < self.window.b_size - 1):
            w = self.window.grid_mines.itemAtPosition(y, x +1).widget()
            if (w.is_revealed == False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x, w.y)
        if (y > 0):
            w = self.window.grid_mines.itemAtPosition(y-1, x ).widget()
            if (w.is_revealed == False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x, w.y)
        if (y < self.window.b_size - 1):
            w = self.window.grid_mines.itemAtPosition(y+1, x ).widget()
            if (w.is_revealed == False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x, w.y)

        if (x > 0 and y > 0):
            w=self.window.grid_mines.itemAtPosition(y-1, x-1).widget()
            if (w.is_revealed == False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x, w.y)
        if (x < self.window.b_size - 1 and y < self.window.b_size - 1):
            w=self.window.grid_mines.itemAtPosition(y+1, x+1).widget()
            if (w.is_revealed == False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x, w.y)
        if (x > 0 and y < self.window.b_size - 1):
            w=self.window.grid_mines.itemAtPosition(y+1, x-1).widget()
            if (w.is_revealed == False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x, w.y)
        if (x <self.window.b_size - 1 and y > 0):
            w=self.window.grid_mines.itemAtPosition(y-1, x+1).widget()
            if (w.is_revealed == False):
                self.window.safeNum -= 1
                w.is_revealed = True
                w.update()
                if (w.adjacent_n == 0):
                    self.safeArea(w.x, w.y)
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.b_size, self.n_mines = LEVELS[0]
        self.start=False
        self.safeNum=self.b_size*self.b_size-self.n_mines

        hb1 = QHBoxLayout()
        # hb1 will contain lbl_mines, btn_start, lbl_clock
        #剩余地雷数
        self.lbl_mines = QLabel()
        self.lbl_mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        font = self.lbl_mines.font()
        font.setPointSize(24)
        font.setWeight(75)
        self.lbl_mines.setFont(font)
        self.lbl_mines.setText("%03d" % self.n_mines)
        hb1.addWidget(self.lbl_mines)

        #笑脸
        self.btn_start = QPushButton()
        self.btn_start.setFixedSize(QSize(32, 32))
        self.btn_start.setIconSize(QSize(32, 32))
        self.btn_start.setIcon(QIcon("./images/smiley.png"))
        self.btn_start.setFlat(True)
        self.btn_start.pressed.connect(lambda : self.reset())
        hb1.addWidget(self.btn_start)

        # 设置时间
        self.timer = QTimer()
        self.count = 0
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda: self.showNum())

        self.lbl_clock = QLabel()
        self.lbl_clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.lbl_clock.setFont(font)
        self.lbl_clock.setText("%03d"%self.count)
        hb1.addWidget(self.lbl_clock)

        # hb1 will contain hb1, grid
        vb = QVBoxLayout()
        vb.addLayout(hb1)


        self.grid_mines = QGridLayout()
        self.grid_mines.setSpacing(3)

        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w_mine = Pos(self,x, y)
                self.grid_mines.addWidget(w_mine, y, x)

        vb.addLayout(self.grid_mines)
        win = QWidget()
        win.setLayout(vb)
        self.setCentralWidget(win)

    def showNum(self):
        self.count += 1
        self.lbl_clock.setText("%03d"%self.count)

    def reset(self):
        self.b_size, self.n_mines = LEVELS[0]
        self.start = False
        self.count=0
        self.safeNum=self.b_size*self.b_size-self.n_mines
        self.timer.stop()
        self.lbl_mines.setText("%03d" %self.n_mines)
        self.lbl_clock.setText("%03d" % self.count)
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w=self.grid_mines.itemAtPosition(y,x).widget()
                w.is_mine = False
                w.adjacent_n = 0
                w.is_revealed = False
                w.is_flagged = False
                w.update()


    def init(self):
        mines=[]
        for i in range(self.n_mines):
            x=random.randint(0,self.b_size-1)
            y=random.randint(0,self.b_size-1)
            while ([x,y] in mines):
                x = random.randint(0, self.b_size - 1)
                y = random.randint(0, self.b_size - 1)
            mines.append([x,y])
            w=self.grid_mines.itemAtPosition(y, x).widget()
            w.is_mine=True
            if(x>0):
                self.grid_mines.itemAtPosition(y, x-1).widget().adjacent_n+=1
            if(x<self.b_size-1):
                self.grid_mines.itemAtPosition(y, x+1).widget().adjacent_n +=1
            if(y>0):
                self.grid_mines.itemAtPosition(y-1, x ).widget().adjacent_n += 1
            if(y<self.b_size-1):
                self.grid_mines.itemAtPosition(y+1, x).widget().adjacent_n += 1

            if (x>0 and y >0):
                self.grid_mines.itemAtPosition(y -1, x-1).widget().adjacent_n += 1
            if (x>0 and y < self.b_size - 1):
                self.grid_mines.itemAtPosition(y + 1, x-1).widget().adjacent_n += 1
            if (x<self.b_size - 1 and y < self.b_size - 1):
                self.grid_mines.itemAtPosition(y + 1, x+1).widget().adjacent_n += 1
            if (x<self.b_size - 1 and y >0):
                self.grid_mines.itemAtPosition(y -1, x+1).widget().adjacent_n += 1


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec_()