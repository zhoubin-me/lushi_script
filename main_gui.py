# -*- coding: utf-8 -*-
import re
import sys

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *


def get_rect(strings="", name=""):  # to find QLineEdit location
    res = re.findall(rf'<widget class="QLineEdit" name="{name}">(.*?)</widget>', strings)[0]
    x = re.findall(r'<x>(\d+)</x>', res)[0]
    y = re.findall(r'<y>(\d+)</y>', res)[0]
    width = re.findall(r'<width>(\d+)</width>', res)[0]
    height = re.findall(r'<height>(\d+)</height>', res)[0]
    return [int(x), int(y), int(width), int(height)]


class DropLineEdit(QLineEdit):  # get file path by using mouse
    def __init__(self, parent=None):
        super(DropLineEdit, self).__init__(parent)
        # self.setAcceptDrops(True)
        self.setDragEnabled(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasText():
            file_path = e.mimeData().text()
            file_path = file_path.split('\n')
            # print(filePath[0])  # only read the first file
            file_path = file_path[0].split('///')  # remove file:///
            self.setText(file_path[1])  # save file path into QLineEdit
        else:
            e.ignore()


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.save = self.findChild(QPushButton, 'Save')  # Find the button
        self.save.clicked.connect(
            self.saveButtonPressed)  # Remember to pass the definition/method, not the return value!

        self.run = self.findChild(QPushButton, 'Run')  # Find the button
        self.run.clicked.connect(self.runButtonPressed)

        with open('main.ui', 'r') as f:
            ui_xml = f.read().replace('\n', "")

        log_rect = get_rect(ui_xml, "log_path")
        self.log = self.findChild(QLineEdit, 'log_path')
        # self.input.setAcceptDrops(True)
        self.log = DropLineEdit(self)
        self.log.setGeometry(QtCore.QRect(*log_rect))
        self.log.setPlaceholderText("Please input Power.log path")

        bn_rect = get_rect(ui_xml, "bn_path")
        self.bn = self.findChild(QLineEdit, 'bn_path')
        self.bn = DropLineEdit(self)
        self.bn.setGeometry(QtCore.QRect(*bn_rect))
        self.bn.setPlaceholderText("Please input Battle.net.exe path")

        self.language = self.findChild(QSpinBox, 'language')
        self.team_id = self.findChild(QSpinBox, 'team_id')
        self.boss_id = self.findChild(QSpinBox, "boss_id")
        self.hero_count = self.findChild(QSpinBox, "hero_count")
        self.reward_count = self.findChild(QSpinBox, "reward_count")
        self.delay = self.findChild(QDoubleSpinBox, "delay")
        self.confidence = self.findChild(QDoubleSpinBox, "confidence")
        self.longest_waiting = self.findChild(QDoubleSpinBox, "longest_waiting")
        self.early_stop = self.findChild(QCheckBox, "early_stop")
        self.auto_restart = self.findChild(QCheckBox, "auto_restart")

        self.show()

    def saveButtonPressed(self):
        # This is executed when the button is pressed
        print('Power.log:\t' + self.log.text())
        print('Battle.net:\t' + self.bn.text())
        print("early_stop:\t", end="")
        print(self.early_stop.isChecked())
        print("auto_restart:\t", end="")
        print(self.auto_restart.isChecked())
        print("delay:\t", end="")
        print(self.delay.value())
        print("boss_id:\t", end="")
        print(self.boss_id.value())

    def runButtonPressed(self):
        print('run')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
