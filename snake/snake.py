from PyQt4 import QtCore
from PyQt4.QtCore import Qt, QTimer
from PyQt4.QtGui import QApplication, QMainWindow, QPixmap, QImage
import sys
import random

from ui_mainwindow import Ui_MainWindow

# ----------------------------------------------------------------------------------------------------------------------

WHITE = QtCore.Qt.white
BLACK = QtCore.Qt.black

WIDTH, HEIGHT = 200, 100
FACTOR = 4

RIGHT = 1,0
LEFT = -1,0
UP = 0,-1
DOWN = 0,1

def move_pixel(pixel, direction):
    dx, dy = direction
    x, y = pixel
    return (x+dx)%WIDTH, (y+dy)%HEIGHT

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.image = QImage(WIDTH, HEIGHT, QImage.Format_RGB32)
        self.clear_canvas()
        self.refresh_canvas()
        self.input_key = None

        self.game_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        self.startButton.clicked.connect(self.start_game)
        self.speedSpinbox.valueChanged.connect(self.set_game_speed)

        self.start_game()

    def clear_canvas(self):
        self.image.fill(WHITE)

    def draw_on_canvas(self, x, y, color):
        self.image.setPixel(x, y, color)

    def refresh_canvas(self):
        self.pixmap = QPixmap.fromImage(self.image)
        self.canvasLabel.setPixmap(self.pixmap.scaled(FACTOR*WIDTH, FACTOR*HEIGHT, Qt.KeepAspectRatio))

    def keyPressEvent(self, event):
        self.input_key = event.key()

    def get_game_speed(self):
        return 1000 // self.speedSpinbox.value()

    def set_game_speed(self):
        if self.game_running:
            self.timer.stop()
            self.timer.start(self.get_game_speed())
            self.canvasLabel.setFocus()

    # -------------------------------------------

    def start_game(self):
        self.scoreSpinbox.setValue(0)
        self.game_running = True
        self.direction = RIGHT
        self.snake = [(50,50)]
        for i in range(5):
            self.snake.append(move_pixel(self.snake[-1], LEFT))

        self.snake_size = len(self.snake)

        self.food = 100, 50

        self.timer.start(self.get_game_speed())

    def tick(self):
        # game logic
        self.handle_direction()
        self.move_snake()
        self.eat_food()
        self.handle_ouroboros()

        # drawing logic
        self.clear_canvas()
        self.draw_game()

        # finalize
        self.refresh_canvas()
        self.input_key = None

    def eat_food(self):
        if self.snake[0] == self.food:
            while True:
                self.food = random.randrange(0, WIDTH), random.randrange(0, HEIGHT)
                if self.food not in self.snake:
                    break

            self.scoreSpinbox.setValue(self.scoreSpinbox.value() + 1)

            self.snake_size += 3
            print("food eaten")

    def handle_ouroboros(self):
        if self.snake[0] in self.snake[1:]:
            print("game over")
            self.timer.stop()
            self.game_running = False

    def handle_direction(self):
        k = self.input_key

        if k == QtCore.Qt.Key_W and self.direction != DOWN:
            self.direction = UP
        elif k == QtCore.Qt.Key_S and self.direction != UP:
            self.direction = DOWN
        elif k == QtCore.Qt.Key_A and self.direction != RIGHT:
            self.direction = LEFT
        elif k == QtCore.Qt.Key_D and self.direction != LEFT:
            self.direction = RIGHT

    def move_snake(self):
        self.snake.insert(0, move_pixel(self.snake[0], self.direction))
        self.snake = self.snake[:self.snake_size]

    def draw_game(self):
        for x, y in self.snake:
            self.draw_on_canvas(x, y, BLACK)

        x, y = self.food
        self.draw_on_canvas(x, y, BLACK)

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
