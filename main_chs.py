

# -*- coding: utf-8 -*-
import sys
import PyQt5
import pinyin
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
import yaml
from util import HEROS

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main_chs.ui', self)

        self.boss_id = self.findChild(QSpinBox, 'boss_level')
        self.team_id = self.findChild(QSpinBox, 'team_id')
        self.reward_count = self.findChild(QSpinBox, 'boss_reward')
        self.bn_path = self.findChild(QLineEdit, 'bn_path')
        self.hs_path = self.findChild(QLineEdit, 'hs_path')
        self.bn_path_find = self.findChild(QToolButton, 'load_path')
        self.bn_path_find.clicked.connect(self.on_load_path_click_bn)
        self.hs_path_find = self.findChild(QToolButton, 'load_path2')
        self.hs_path_find.clicked.connect(self.on_load_path_click_hs)
        self.lang_dropdown = self.findChild(QComboBox, 'lang')
        self.lang_dropdown.addItem('EN-1024x768')
        self.lang_dropdown.addItem('ZH-1600x900')
        self.current_order = self.findChild(QLabel, 'current_order')

        self.save = self.findChild(QPushButton, 'save')  # Find the button
        self.save.clicked.connect(self.saveButtonPressed)  # Click event
        self.run = self.findChild(QPushButton, 'run')  # Find the button
        self.run.clicked.connect(self.runButtonPressed)  # Click event
        self.load = self.findChild(QPushButton, 'load')  # Find the button
        self.load.clicked.connect(self.load_config)  # Click event

        self.hero_dropdown = self.findChild(QComboBox, 'hero_list')
        heros_sorted = {k: v[0] for k, v in sorted(
            HEROS.items(), key=lambda item: pinyin.get(item[1][0], format="strip", delimiter=""))}
        for k, v in heros_sorted.items():
            self.hero_dropdown.addItem(v)

        self.hero_list = self.findChild(QListView, 'heros')
        self.slm = QStringListModel([])
        self.hero_list.setModel(self.slm)
        self.hero_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hero_list.clicked.connect(self.on_hero_clicked)
        self.hero_index = -1

        self.add = self.findChild(QPushButton, 'add')
        self.add.clicked.connect(self.addButtonPressed)  # Click event
        self.delete = self.findChild(QPushButton, 'del')
        self.delete.clicked.connect(self.delButtonPressed)  # Click event
        self.go_up = self.findChild(QPushButton, 'goup')
        self.go_up.clicked.connect(self.upButtonPressed)  # Click event
        self.delete = self.findChild(QPushButton, 'godown')
        self.delete.clicked.connect(self.downButtonPressed)  # Click event

        self.radio_buttons = []
        for radio_text in ['321', '312', '213', '231', '123', '132']:
            radio = self.findChild(QRadioButton, f'r{radio_text}')
            radio.toggled.connect(self.on_radio_click)
            self.radio_buttons.append(radio)


        self.auto_restart = self.findChild(QCheckBox, 'auto_restart')
        self.early_stop = self.findChild(QCheckBox, 'early_stop')

        self.show()

        self.skill_order = "1，2，3"
        self.bn_path_str = ""
        self.hs_path_str = ""
        self.hero_info = {}
        self.config = {}

    def load_config(self):
        with open('last_config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        for k, v in self.config.items():
            if k == 'boss_id':
                self.boss_id.setValue(v + 1)
            if k == 'team_id':
                self.team_id.setValue(v + 1)
            if k == 'reward_count':
                self.reward_count.setValue(v)
            if k == 'bn_path':
                self.bn_path.setText(v)
            if k == 'hs_path':
                self.hs_path.setText(v)
            if k == 'auto_restart':
                self.auto_restart.setChecked(v)
            if k == 'early_stop':
                self.early_stop.setChecked(v)
            if k == 'lang':
                self.lang.setCurrentText(v)
            if k == 'hero':
                hero_ordered = {k_: v_ for k_, v_ in sorted(v.items(), key=lambda item: item[1][-1])}
                self.hero_info = {}
                for k, v in hero_ordered.items():
                    self.hero_info[v[0]] = [k, v[1], v[2]]
                str_list = [v[0] for k, v in hero_ordered.items()]
                self.slm.setStringList(str_list)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_hero_clicked(self, index):
        self.hero_index = index.row()
        str_list = self.slm.stringList()
        if 0 <= self.hero_index < len(str_list):
            hero_name = str_list[self.hero_index]
            self.current_order.setText(self.hero_info[hero_name][-1])

    def on_load_path_click_hs(self):
        self.hs_path_str = QtWidgets.QFileDialog.getOpenFileName(self, 'Find Path of Hearthstone')[0]
        self.hs_path.setText(self.hs_path_str)

    def on_load_path_click_bn(self):
        self.bn_path_str = QtWidgets.QFileDialog.getOpenFileName(self, 'Find Path of BattleNet')[0]
        self.bn_path.setText(self.bn_path_str)

    def on_radio_click(self):
        bt = self.sender()
        if bt.isChecked():
            self.skill_order = bt.text()
            print(self.skill_order.split('，'))

    def upButtonPressed(self):
        str_list = self.slm.stringList()
        if 1 <= self.hero_index < len(str_list):
            str_list[self.hero_index], str_list[self.hero_index-1] = str_list[self.hero_index-1], str_list[self.hero_index]
            self.slm.setStringList(str_list)

    def downButtonPressed(self):
        str_list = self.slm.stringList()
        if 0 <= self.hero_index < len(str_list)-1:
            str_list[self.hero_index], str_list[self.hero_index+1] = str_list[self.hero_index+1], str_list[self.hero_index]
            self.slm.setStringList(str_list)

    def delButtonPressed(self):
        str_list = self.slm.stringList()
        if 0 <= self.hero_index < len(str_list):
            name_chs = str_list.pop(self.hero_index)
            self.slm.setStringList(str_list)
            del self.hero_info[name_chs]

    def addButtonPressed(self):
        str_list = self.slm.stringList()
        if self.hero_dropdown.currentText() not in str_list and len(str_list) <= 6:
            str_list.append(self.hero_dropdown.currentText())
            kv = [(k, v) for k, v in HEROS.items() if v[0] == self.hero_dropdown.currentText()]
            idx, (name_chs, name_eng) = kv[0]
            self.hero_info[name_chs] = [idx, name_eng, self.skill_order]
            self.slm.setStringList(str_list)

    def saveButtonPressed(self):
        self.config['boss_id'] = self.boss_id.value() - 1
        self.config['team_id'] = self.team_id.value() - 1
        self.config['reward_count'] = self.reward_count.value()
        self.config['bn_path'] = self.bn_path.text()
        self.config['hs_path'] = self.hs_path.text()
        self.config['auto_restart'] = self.auto_restart.isChecked()
        self.config['early_stop'] = self.early_stop.isChecked()
        self.config['lang'] = self.lang.currentText()

        new_hero_info = {}
        hero_order_list = self.slm.stringList()
        for k, v in self.hero_info.items():
            hero_index = hero_order_list.index(k)
            new_hero_info[v[0]] = [k, v[1], v[2], hero_index]
        self.config['hero'] = new_hero_info

        with open('last_config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f)
        print(self.config)

    def runButtonPressed(self):
        hero_text = ""
        for k, v in self.hero_info.items():
            hero_text += f"\t{k} Skill Order {v[-1]}\n"


        cfm_text = f'''
            Current Setting:\n
            Boss ID: {self.config['boss_id']+1}\n
            Team ID: {self.config['team_id']+1}\n
            Boss Reward: {self.config['reward_count']}\n
            BattleNet Path: {self.config['bn_path']}\n
            HearthStone Path: {self.config['hs_path']}\n
            Auto Restart: {self.config['auto_restart']}\n
            Early Stop: {self.config['early_stop']}\n
            Language & Resolution: {self.config['lang']}\n
            Heros:\n
            {hero_text}
        '''

        reply = QMessageBox.question(self, 'CONFIRM', cfm_text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            from lushi import run_from_gui
            self.saveButtonPressed()
            run_from_gui()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()
