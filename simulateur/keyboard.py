# Simulateur du clavier de la rendeuse
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from enum import Enum

direction = None


class Direction(Enum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3


class ButtonValider(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Valider")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    def magic(self):
        print("Action Validée")


class ButtonCancel(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Annuler")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    def magic(self):
        print("Action annulée")


class Joystick(QWidget):
    def __init__(self, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(100, 100)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.__maxDistance = 50
        self.summ = 0.0

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.__maxDistance, -self.__maxDistance, self.__maxDistance * 2,
                        self.__maxDistance * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)
        return QRectF(-20, -20, 40, 40).translated(self._center())

    def _center(self):
        return QPointF(self.width() / 2, self.height() / 2)

    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if (limitLine.length() > self.__maxDistance):
            limitLine.setLength(self.__maxDistance)
        return limitLine.p2()

    def joystickDirection(self):
        if not self.grabCenter:
            return 0
        normVector = QLineF(self._center(), self.movingOffset)
        currentDistance = normVector.length()
        angle = normVector.angle()

        distance = min(currentDistance / self.__maxDistance, 1.0)
        if 45 <= angle < 135:
            pass
            #return (Direction.Up, distance)
        elif 135 <= angle < 225:
            if distance <= 0.33:
                return -0.1
            elif distance <= 0.66:
                return -0.2
            else:
                return -0.5
            #return (Direction.Left, distance)
        elif 225 <= angle < 315:
            pass
            #return (Direction.Down, distance)
        if distance <= 0.33:
            return 0.1
        elif distance <= 0.66:
            return 0.2
        else:
            return 0.5
        #return (Direction.Right, distance)

    def mousePressEvent(self, ev):
        self.grabCenter = self._centerEllipse().contains(ev.pos())
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, event):
        self.grabCenter = False
        self.movingOffset = QPointF(0, 0)
        self.update()

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            # print("Moving")
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
        self.summ = self.summ + self.joystickDirection()
        if self.summ > 0.0:
            self.summ = 0.0
        print(self.summ)
        #print(self.joystickDirection())


if __name__ == '__main__':
    # Create main application window
    app = QApplication([])
    app.setStyle(QStyleFactory.create("Cleanlooks"))
    mw = QMainWindow()
    mw.setWindowTitle('Qt5 Clavier - Codename Neptune')

    # Create and set widget layout
    # Main widget container
    cw = QWidget()
    ml = QGridLayout()
    cw.setLayout(ml)
    mw.setCentralWidget(cw)
    mw.resize(500, 220)
    # Create joystick
    joystick = Joystick()
    buttonC = ButtonCancel()
    buttonV = ButtonValider()
    # ml.addLayout(joystick.get_joystick_layout(),0,0)
    ml.addWidget(buttonC, 0, 0)
    ml.addWidget(joystick, 0, 1)
    ml.addWidget(buttonV, 0, 2)

    mw.show()

    ## Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QApplication.instance().exec_()
