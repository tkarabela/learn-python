from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QMainWindow, QPixmap, QImage
import sys
import random

from ui_mainwindow import Ui_MainWindow

# ----------------------------------------------------------------------------------------------------------------------

WHITE = QtCore.Qt.white
BLACK = QtCore.Qt.black

WIDTH, HEIGHT = 200, 100
FACTOR = 4

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.image = QImage(WIDTH, HEIGHT, QImage.Format_RGB32)
        self.clear_canvas()
        self.refresh_canvas()
        self.input_key = None

        self.startButton.clicked.connect(self.start_game)

    def clear_canvas(self):
        self.image.fill(WHITE)

    def draw_on_canvas(self, x, y, color):
        self.image.setPixel(x, y, color)

    def refresh_canvas(self):
        self.pixmap = QPixmap.fromImage(self.image)
        self.canvasLabel.setPixmap(self.pixmap.scaled(FACTOR*WIDTH, FACTOR*HEIGHT, Qt.KeepAspectRatio))

    def keyPressEvent(self, event):
        self.input_key = event.key()

    # -------------------------------------------

    def start_game(self):
        # TODO: initialization logic

        self.draw_on_canvas(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), BLACK)
        self.tick()

    def tick(self):
        # TODO: game logic

        self.refresh_canvas()
        self.input_key = None

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
