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


def save_config(config):
    with open('main.ui', 'r') as f:
        ui_config = f.read()
    ui_config = re.sub(r'( name="bn_path">[\s\S]*?name="text">[\s\S]*?<string>).*?(</string>)', rf"\1{config['bn']}\2",
                       ui_config)
    ui_config = re.sub(r'( name="log_path">[\s\S]*?name="text">[\s\S]*?<string>).*?(</string>)',
                       rf"\1{config['log']}\2", ui_config)
    ui_config = re.sub(r'( name="team_id">[\s\S]*?name="value">[\s\S]*?<number).*?(</number>)',
                       rf"\1>{config['team_id']}\2", ui_config)
    ui_config = re.sub(r'( name="reward_count">[\s\S]*?name="value">[\s\S]*?<number).*?(</number>)',
                       rf"\1>{config['reward_count']}\2", ui_config)
    ui_config = re.sub(r'( name="hero_count">[\s\S]*?name="value">[\s\S]*?<number).*?(</number>)',
                       rf"\1>{config['hero_count']}\2", ui_config)
    ui_config = re.sub(r'( name="language">[\s\S]*?name="value">[\s\S]*?<number).*?(</number>)',
                       rf"\1>{config['language']}\2", ui_config)
    ui_config = re.sub(r'( name="boss_id">[\s\S]*?name="value">[\s\S]*?<number).*?(</number>)',
                       rf"\1>{config['boss_id']}\2", ui_config)
    ui_config = re.sub(r'( name="longest_waiting">[\s\S]*?name="value">[\s\S]*?<number).*?(</number>)',
                       rf"\1>{config['longest_waiting']}\2", ui_config)
    ui_config = re.sub(r'( name="delay">[\s\S]*?name="value">[\s\S]*?<double).*?(</double>)',
                       rf"\1>{config['delay']}\2", ui_config)
    ui_config = re.sub(r'( name="auto_restart">[\s\S]*?name="checked">[\s\S]*?<bool).*?(</bool>)',
                       rf"\1>{'true' if config['auto_restart'] else 'false'}\2", ui_config)
    ui_config = re.sub(r'( name="early_stop">[\s\S]*?name="checked">[\s\S]*?<bool).*?(</bool>)',
                       rf"\1>{'true' if config['early_stop'] else 'false'}\2", ui_config)
    with open('main.ui', 'w') as f:
        f.writelines(ui_config)


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

        self.log = self.findChild(QLineEdit, 'log_path')
        self.bn = self.findChild(QLineEdit, 'bn_path')
        self.language = self.findChild(QSpinBox, 'language')
        self.team_id = self.findChild(QSpinBox, 'team_id')
        self.boss_id = self.findChild(QSpinBox, "boss_id")
        self.hero_count = self.findChild(QSpinBox, "hero_count")
        self.reward_count = self.findChild(QSpinBox, "reward_count")
        self.delay = self.findChild(QDoubleSpinBox, "delay")
        self.confidence = self.findChild(QDoubleSpinBox, "confidence")
        self.longest_waiting = self.findChild(QSpinBox, "longest_waiting")
        self.early_stop = self.findChild(QCheckBox, "early_stop")
        self.auto_restart = self.findChild(QCheckBox, "auto_restart")

        log_rect = get_rect(ui_xml, "log_path")
        # self.input.setAcceptDrops(True)
        default_log = self.log.text()
        if default_log:
            self.log = DropLineEdit(self)
            self.log.setGeometry(QtCore.QRect(*log_rect))
            self.log.setText(default_log)
        else:
            self.log = DropLineEdit(self)
            self.log.setGeometry(QtCore.QRect(*log_rect))
            self.log.setPlaceholderText("Please input Power.log path")

        bn_rect = get_rect(ui_xml, "bn_path")
        default_bn = self.bn.text()
        if default_bn:
            self.bn = DropLineEdit(self)
            self.bn.setGeometry(QtCore.QRect(*bn_rect))
            self.bn.setText(default_bn)
        else:
            self.bn = DropLineEdit(self)
            self.bn.setGeometry(QtCore.QRect(*bn_rect))
            self.bn.setPlaceholderText("Please input Battle.net.exe path")

        self.show()

    def saveButtonPressed(self):
        # This is executed when the button is pressed
        self.basic_config = {
            'log': self.log.text(),
            'bn': self.bn.text(),
            'early_stop': self.early_stop.isChecked(),
            'auto_restart': self.auto_restart.isChecked(),
            'team_id': self.team_id.value(),
            'language': self.language.value(),
            'boss_id': self.boss_id.value(),
            'hero_count': self.hero_count.value(),
            'reward_count': self.reward_count.value(),
            'delay': self.delay.value(),
            'confidence': self.confidence.value(),
            'longest_waiting': self.longest_waiting.value()
        }
        print(self.basic_config)
        save_config(self.basic_config)

    def runButtonPressed(self):
        print('run')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
