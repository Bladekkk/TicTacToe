from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import Ui_MainWindow

class Widget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем системные рамки + кнопки: закрыть, свернуть
        self.setAttribute(Qt.WA_TranslucentBackground)  # Убираем фон который выходит за круглые рамки, чтобы выглядело красиво

        self._old_pos = None

        self.setWindowOpacity(0.75)  # Прозрачность окна (от 0 до 1, float)

        self.btnClose.clicked.connect(self.close)

        self.thread_handler = Updater(True)
        self.thread_handler.signal.connect(self.signal_handler)
        self.thread_handler.start()

        self.btn1.clicked.connect(lambda: self.btn_reload(self.btn1))
        self.btn2.clicked.connect(lambda: self.btn_reload(self.btn2))
        self.btn3.clicked.connect(lambda: self.btn_reload(self.btn3))
        self.btn4.clicked.connect(lambda: self.btn_reload(self.btn4))
        self.btn5.clicked.connect(lambda: self.btn_reload(self.btn5))
        self.btn6.clicked.connect(lambda: self.btn_reload(self.btn6))
        self.btn7.clicked.connect(lambda: self.btn_reload(self.btn7))
        self.btn8.clicked.connect(lambda: self.btn_reload(self.btn8))
        self.btn9.clicked.connect(lambda: self.btn_reload(self.btn9))
        self.reset.clicked.connect(lambda: self.btnReset())

        self.state = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, '9': None}
        self.turn = 'X'

    def check(self, char):
        l = self.state
        if l['1'] == char and l['2'] == char and l['3'] == char:
            return True
        elif l['4'] == char and l['5'] == char and l['6'] == char:
            return True
        elif l['7'] == char and l['8'] == char and l['9'] == char:
            return True
        elif l['1'] == char and l['4'] == char and l['7'] == char:
            return True
        elif l['2'] == char and l['5'] == char and l['8'] == char:
            return True
        elif l['3'] == char and l['6'] == char and l['9'] == char:
            return True
        elif l['1'] == char and l['5'] == char and l['9'] == char:
            return True
        elif l['3'] == char and l['5'] == char and l['7'] == char:
            return True
        else:
            return False

    def btn_reload(self, btn: QtWidgets.QPushButton):
        char = btn.text()
        if char == '' and str(self.label.text()).endswith('win!') is False:
            if self.turn == 'X':
                btn.setText('X')
                self.turn = 'O'
                position = btn.objectName()
                self.state[str(position).replace('btn', '')] = 'O'
            else:
                btn.setText('O')
                self.turn = 'X'
                position = btn.objectName()
                self.state[str(position).replace('btn', '')] = 'X'
        else:
            pass
        if self.checkFree() is False and self.check('X') is False and self.check('O') is False:
            self.label.setText('Nobody wins')
        else:
            self.label.setText(f"{self.turn}\'s turn!")
            res = self.check('O')
            if res:
                self.label.setText('X win!')
            res = self.check('X')
            if res:
                self.label.setText('O win!')
    def btnReset(self):
        for i in [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8, self.btn9]:
            i.setText('')
            self.label.setText('Start!')
        self.state = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, '9': None}

    def checkFree(self):
        free = False

        for i in self.state:
            if self.state[i] is None:
                free = True
                break

        return free

    # Следующие функции для того чтобы переносить окно за любое место
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return
        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def signal_handler(self, value: list) -> None:
        pass

class Updater(QThread):

    signal = QtCore.pyqtSignal(list)

    def __init__(self, status, parent=None):
        super(Updater, self).__init__(parent)
        self.status = status

    def run(self):
        self.signal.emit(['started'])
        while True:
            pass

# Запуск собственно
if __name__ == '__main__':
    app = QApplication([])

    w = Widget()
    w.show()

    app.exec()