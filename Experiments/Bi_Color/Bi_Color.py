import sys
import serial
import winsound
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QColor
from win32api import GetSystemMetrics
from threading import Timer
import numpy as np
import time
import datetime

class Color(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Color Detection'
        self.left = 0
        self.top = 0
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

        self.setWindowTitle(self.title)
        self.setStyleSheet('Background-color: rgb(0, 0, 0)')
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.Flabel = QLabel(self)
        self.Flabel.setGeometry(int(self.width/2)-200, int(self.height/2)-200, 400, 400)
        self.pixmap1 = QPixmap('K:/OneDrive - iitkgp.ac.in/PhD/Experiments/Color Detection/Bi_Color/Fixation2.png')
        self.Flabel.setPixmap(self.pixmap1)
        self.Flabel.setScaledContents(True)
        self.Flabel.setAlignment(Qt.AlignCenter)
        self.Flabel.setVisible(False)

        self.baseline_timer = QTimer(self)
        self.fixation_timer = QTimer(self)
        self.marker_timer = QTimer(self)
        self.sound_timer = QTimer(self)

        self.Clabel = QLabel(self)
        self.Clabel.setGeometry(self.left, self.top, self.width, self.height)
        self.Clabel.setStyleSheet('background-color: rgb(0, 0, 0)')
        self.Clabel.setVisible(False)

        self.setCursor(Qt.BlankCursor)

        self.marker_list = [1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 2,
                            1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2] # 50 items

        self.i = 0

        self.event_list = []

        self.session_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.filename = 'Bi_Color/events_' + str(self.session_time) + '.txt'

    def keyPressEvent(self, e):
        print(e.key())
        if e.key() == 16777220:  # press enter to call start function
            # winsound.Beep(300, 200)
            self.start()

        if e.key() == 16777216:  # press Esc to exit the program
            # print("Experiment Completed.....")
            # open file in write mode
            self.event_list.append([time.time(), 'end'])
            with open(self.filename, 'w') as fp:
                for item in self.event_list:
                    fp.write("%s,%s\n" % (str(item[0]), item[1]))
            fp.close()
            print(self.event_list)
            # winsound.Beep(300, 200)
            sys.exit()

    def start(self):
        # print("Experiment Started.....")
        self.event_list.append([time.time(), 'start'])
        self.baseline()

    def baseline(self):
        # print('I am baseline at : ', time.time())
        self.event_list.append([time.time(), 'baseline'])
        self.baseline_timer.singleShot(10000, self.sound)
        self.Clabel.setVisible(False)

    def sound(self):
        self.event_list.append([time.time(), 'beep'])
        self.sound_timer.singleShot(1000, self.fixation)
        winsound.Beep(500, 1000)

    def fixation(self):
        # print('I am fixation at : ', time.time())
        self.event_list.append([time.time(), 'fixation'])
        self.fixation_timer.singleShot(3000, self.marker)
        self.Flabel.setVisible(True)
        self.Clabel.setVisible(False)

    def marker(self):
        # print('I am marker at : ', time.time())
        self.Flabel.setVisible(False)
        self.marker_timer.singleShot(5000, self.fixation)
        self.Flabel.setVisible(False)
        if not self.Clabel.isVisible():
            self.Clabel.setVisible(True)
        self.bicolor()

    def bicolor(self):
        self.Flabel.setVisible(False)
        print(self.i)
        if self.i < len(self.marker_list):
            if self.marker_list[self.i] == 1:
                # print('I am bi-color at : ', time.time())
                self.event_list.append([time.time(), 'red'])
                self.Clabel.setStyleSheet('background-color: rgb(255, 0, 0)')
            elif self.marker_list[self.i] == 2:
                self.event_list.append([time.time(), 'blue'])
                self.Clabel.setStyleSheet('background-color: rgb(0, 0, 255)')
            else:
                self.event_list.append([time.time(), 'black'])
                self.Clabel.setStyleSheet('background-color: rgb(0, 0, 0)')
            self.i = self.i + 1
        else:
            print("Experiment Completed.....")
            # open file in write mode
            self.event_list.append([time.time(), 'end'])
            with open(self.filename, 'w') as fp:
                for item in self.event_list:
                    # print(item)
                    # write each item on a new line
                    fp.write("%s,%s\n" % (str(item[0]), item[1]))
            fp.close()
            print(self.event_list)
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Color()
    demo.showFullScreen()
    app.exec()
