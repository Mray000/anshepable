import sys
import inspect
import os.path
import json
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QHeaderView, QTableWidgetItem,  QPushButton, QLabel
from PyQt5.QtCore import QEvent, QObject, Qt, QUrl, QSize
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5 import QtMultimedia

from gui import Ui_MainWindow
from json_parsing import TableWithJson
from game_judge import PendingGame
from parsing.main_scratcher import main
from db_connection import DbConnection

# if database is not available you should decomment this piece of code

# main()


def make_constants(field):
    field.ENGLISH_LAYOUT = {
        'err': [field.a_backspace],
        'a': [field.a_a],
        'b': [field.a_b],
        'c': [field.a_c],
        'd': [field.a_d],
        'e': [field.a_e],
        'f': [field.a_f],
        'g': [field.a_g],
        'h': [field.a_h],
        'i': [field.a_i],
        'j': [field.a_j],
        'k': [field.a_k],
        'l': [field.a_l],
        'm': [field.a_m],
        'n': [field.a_n],
        'o': [field.a_o],
        'p': [field.a_p],
        'q': [field.a_q],
        'r': [field.a_r],
        's': [field.a_s],
        't': [field.a_t],
        'u': [field.a_u],
        'v': [field.a_v],
        'w': [field.a_w],
        'x': [field.a_x],
        'y': [field.a_y],
        'z': [field.a_z],
        'A': [field.a_a, field.a_shift],
        'B': [field.a_b, field.a_shift],
        'C': [field.a_c, field.a_shift],
        'D': [field.a_d, field.a_shift],
        'E': [field.a_e, field.a_shift],
        'F': [field.a_f, field.a_shift],
        'G': [field.a_g, field.a_shift],
        'H': [field.a_h, field.a_shift],
        'I': [field.a_i, field.a_shift],
        'J': [field.a_j, field.a_shift],
        'K': [field.a_k, field.a_shift],
        'L': [field.a_l, field.a_shift],
        'M': [field.a_m, field.a_shift],
        'N': [field.a_n, field.a_shift],
        'O': [field.a_o, field.a_shift],
        'P': [field.a_p, field.a_shift],
        'Q': [field.a_q, field.a_shift],
        'R': [field.a_r, field.a_shift],
        'S': [field.a_s, field.a_shift],
        'T': [field.a_t, field.a_shift],
        'U': [field.a_u, field.a_shift],
        'V': [field.a_v, field.a_shift],
        'W': [field.a_w, field.a_shift],
        'X': [field.a_x, field.a_shift],
        'Y': [field.a_y, field.a_shift],
        'Z': [field.a_z, field.a_shift],
        ',': [field.a_comma],
        '(': [field.a_nine, field.a_shift],
        '"': [field.a_oneap, field.a_shift],
        "'": [field.a_oneap],
        ':': [field.a_doubledot],
        '1': [field.a_one],
        '2': [field.a_two],
        '3': [field.a_three],
        '4': [field.a_four],
        '5': [field.a_five],
        '6': [field.a_six],
        '7': [field.a_seven],
        '8': [field.a_eight],
        '9': [field.a_nine],
        '0': [field.a_zero],
        ')': [field.a_zero, field.a_shift],
        ';': [field.a_doubledot, field.a_shift],
        '-': [field.a_def],
        '~': [field.e_apostrophe, field.a_shift],
        '.': [field.a_dot],
        '!': [field.a_one, field.a_shift],
        '$': [field.a_four, field.a_shift],
        ' ': [field.a_space],
        '?': [field.a_slesh, field.a_shift],
    }

    field.RUSSIAN_LAYOUT = {
        'err': [field.r_backspace],
        ',': [field.r_dot, field.r_lshift],
        '(': [field.r_nine, field.r_lshift],
        '"': [field.r_two, field.r_lshift],
        ':': [field.r_six, field.r_lshift],
        '1': [field.r_one],
        '2': [field.r_two],
        '3': [field.r_three],
        '4': [field.r_four],
        '5': [field.f_five],
        '6': [field.r_six],
        '7': [field.r_seven],
        '8': [field.r_eight],
        '9': [field.r_nine],
        '0': [field.r_zero],
        ')': [field.r_zero, field.r_lshift],
        ';': [field.r_four, field.r_lshift],
        '-': [field.r_def],
        '~': [field.r_apostrophe, field.r_lshift],
        '.': [field.r_dot],
        '!': [field.r_one, field.r_lshift],
        ' ': [field.r_space],
        '?': [field.r_seven, field.r_lshift],
        'ё': [field.r_apostrophe],
        'й': [field.r_yi],
        'ц': [field.r_ce],
        'у': [field.r_u],
        'к': [field.r_k],
        'е': [field.r_e],
        'н': [field.r_n],
        'г': [field.r_g],
        'ш': [field.r_sh],
        'щ': [field.r_che_2],
        'з': [field.r_z],
        'х': [field.r_h],
        'ъ': [field.r_solid],
        'ф': [field.r_f],
        'ы': [field.r_ui],
        'в': [field.r_v],
        'а': [field.r_a],
        'п': [field.r_p],
        'р': [field.r_r],
        'о': [field.r_o],
        'л': [field.r_l],
        'д': [field.r_de],
        'ж': [field.r_ze],
        'э': [field.r_eo],
        'я': [field.r_ya],
        'ч': [field.r_che],
        'с': [field.r_s],
        'м': [field.r_m],
        'и': [field.r_i],
        'т': [field.r_t],
        'ь': [field.r_soft],
        'б': [field.r_b],
        'ю': [field.r_yu],
        'Ё': [field.r_apostrophe, field.r_lshift],
        'Й': [field.r_yi, field.r_lshift],
        'Ц': [field.r_ce, field.r_lshift],
        'У': [field.r_u, field.r_lshift],
        'К': [field.r_k, field.r_lshift],
        'Е': [field.r_e, field.r_lshift],
        'Н': [field.r_n, field.r_lshift],
        'Г': [field.r_g, field.r_lshift],
        'Ш': [field.r_sh, field.r_lshift],
        'Щ': [field.r_che_2, field.r_lshift],
        'З': [field.r_z, field.r_lshift],
        'Х': [field.r_h, field.r_lshift],
        'Ъ': [field.r_solid, field.r_lshift],
        'Ф': [field.r_f, field.r_lshift],
        'Ы': [field.r_ui, field.r_lshift],
        'В': [field.r_v, field.r_lshift],
        'А': [field.r_a, field.r_lshift],
        'П': [field.r_p, field.r_lshift],
        'Р': [field.r_r, field.r_lshift],
        'О': [field.r_o, field.r_lshift],
        'Л': [field.r_l, field.r_lshift],
        'Д': [field.r_de, field.r_lshift],
        'Ж': [field.r_ze, field.r_lshift],
        'Э': [field.r_eo, field.r_lshift],
        'Я': [field.r_ya, field.r_lshift],
        'Ч': [field.r_che, field.r_lshift],
        'С': [field.r_s, field.r_lshift],
        'М': [field.r_m, field.r_lshift],
        'И': [field.r_i, field.r_lshift],
        'Т': [field.r_t, field.r_lshift],
        'Ь': [field.r_soft, field.r_lshift],
        'Б': [field.r_b, field.r_lshift],
        'Ю': [field.r_yu, field.r_lshift],
    }

    field.NAMES = {
        'basic english': "Стандартный английский",
        'hard russian': "Сложный русский",
        'long english': 'Длинный английский',
        'long russian': 'Длинный русский',
        'numbers': 'Числа',
        'basic russian': 'Стандартный русский'
    }

    field.ENGLISH = 1
    field.RUSSIAN = 2


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Изображение
        self.pixmap = QPixmap('./uploads/tutorial3.jpg')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        # self.image = QLabel(self)

        self.image.setPixmap(self.pixmap)

        self.gridLayout_2.addWidget(self.image, 4, 0, 1, 1)

        self.good_education = QLabel(self.info)
        self.good_education.setMaximumSize(QSize(16777215, 50))
        self.good_education.setStyleSheet(
            "font-size: 25px; font-weight: 900;\n")
        self.good_education.setAlignment(Qt.AlignCenter)
        self.good_education.setObjectName("good_education")
        self.gridLayout_2.addWidget(self.good_education, 5, 0, 1, 1)
        self.good_education.setText("Удачного обучения!")
        self.setWindowTitle("Ansheapable")
        self.load_mp3('uploads/super_angry.mp3')
        # making constants
        make_constants(self)
        self.json = TableWithJson('./parsing/user_info.json')
        self.json.read_file()
        self.create_piechart()
        self.reset_table()
        # widgets which are common for the choose panel
        self.choose_area = [self.choose_hard_russian,
                            self.choose_long_english,
                            self.choose_basic_english,
                            self.choose_basic_russian,
                            self.choose_title,
                            self.choose_long_russian,
                            self.choose_numbers]
        # widgets which are common for the writing field
        self.tr_area = [self.tr_back_label,
                        self.tr_english_layout,
                        self.tr_info_panel,
                        self.tr_russian_layout,
                        self.tr_back_label,
                        self.tr_text_field,
                        self.tr_writing_area,
                        self.tr_title,
                        self.tr_first_letter,
                        self.tr_come_back]

        self.rez_area = [self.rez_title,
                         self.rez_mistakes,
                         self.rez_main_text,
                         self.rez_new_game,
                         self.rez_empty_filler]
        self.tr_come_back.clicked.connect(self.come_back)
        self.rez_new_game.clicked.connect(self.to_main_window)
        self.hide_elements(self.tr_area)
        self.hide_elements(self.rez_area)
        # add click listener to our buttons
        for item in self.choose_area:
            obj_type = type(item)
            if obj_type == QPushButton:
                item.clicked.connect(self.open_writin_panel)

        self.db_eventor = DbConnection('./parsing/db.sqlite')
        # self.db_eventor.random_text('hard russian')

    def hide_elements(self, elements):
        ''' hide group of elements '''
        for element in elements:
            element.hide()

    def show_elements(self, elements):
        ''' show group of elements '''
        for element in elements:
            element.show()

    def open_writin_panel(self):
        self.hide_elements(self.choose_area)
        self.hide_elements(self.rez_area)
        self.show_elements(self.tr_area)

        name = self.sender().objectName()

        row_name = ' '.join(name.split('_')[1:])

        if 'russian' in name:
            self.tr_english_layout.hide()
            self.cur_language = self.RUSSIAN
        else:
            self.cur_language = self.ENGLISH
            self.tr_russian_layout.hide()

        text = self.db_eventor.random_text(row_name)
        self.tr_title.setText(self.NAMES[row_name])
        self.game_trainer = PendingGame(self, text, row_name)
        self.tr_text_field.setText(text)

    def to_main_window(self):
        self.hide_elements(self.tr_area)
        self.hide_elements(self.rez_area)
        self.show_elements(self.choose_area)

    def come_back(self):
        self.hide_elements(self.tr_area)
        self.hide_elements(self.rez_area)
        self.show_elements(self.choose_area)
        self.game_trainer.ending_without_result()

    def create_piechart(self):
        ''' creating piechart '''
        # adding objects into the series
        meta = []
        data = self.json.get_data()
        for key in self.NAMES.keys():
            meta.append([self.NAMES[key], data[key]['counter']])

        self.field = self.horizontalLayout_12

        self.series = QPieSeries()
        # adding data in series
        for name, value in meta:
            self.series.append(name, value)
        # creating qchart
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Статистика по количеству")
        # and adding animations and view
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # at all we have a widget which are going to be pushed in your field
        self.field.addWidget(self.chart_view)

    def reset_table(self):
        ''' update a info table '''
        dat = self.json.get_data()
        self.basic_russian_max_2.setText(
            str(dat['basic russian']['max_speed']))
        self.basic_russian_avg_2.setText(
            str(dat['basic russian']['avg_value']))
        self.basic_russian_counter_2.setText(
            str(dat['basic russian']['counter']))

        self.basic_english_max_2.setText(
            str(dat['basic english']['max_speed']))
        self.basic_english_avg_2.setText(
            str(dat['basic english']['avg_value']))
        self.basic_english_counter_2.setText(
            str(dat['basic english']['counter']))

        self.long_russian_max_2.setText(str(dat['long russian']['max_speed']))
        self.long_russian_avg_2.setText(str(dat['long russian']['avg_value']))
        self.long_russian_counter_2.setText(
            str(dat['long russian']['counter']))

        self.long_english_max_2.setText(str(dat['long english']['max_speed']))
        self.long_english_avg_2.setText(str(dat['long english']['avg_value']))
        self.long_english_counter_2.setText(
            str(dat['long english']['counter']))

        self.hard_russian_max_2.setText(str(dat['hard russian']['max_speed']))
        self.hard_russian_avg_2.setText(str(dat['hard russian']['avg_value']))
        self.hard_russian_counter_2.setText(
            str(dat['hard russian']['counter']))

        self.numbers_max_2.setText(str(dat['numbers']['max_speed']))
        self.numbers_avg_2.setText(str(dat['numbers']['avg_value']))
        self.numbers_counter_2.setText(str(dat['numbers']['counter']))

    def load_mp3(self, filename):
        ''' loading shep '''

        fn = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(fn))

        cur_dir = path

        # print(sys.argv)
        media = QUrl.fromLocalFile(cur_dir + '/' + filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
