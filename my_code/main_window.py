from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from keyboard import add_hotkey, unhook_all
from PySide6.QtWidgets import QMainWindow, QApplication, QTabWidget
import sys
from pyautogui import click

from my_code.All_macros import Macros_right_click, Macros_left_click, Macros_bow_shoot, Macros_scroll_slots, \
    Macros_eat_command, Macros_lvl_command
from my_code.FileWork import File
from my_code.auto_join import check_restart
from my_code.all_tabs import tab_hot_keys, tab_join_coords, tab_logs


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Переменные нужные для запусков, макросов после рестарта
        self.right_click = False
        self.left_click = False
        self.bow_shoot = False
        self.scroll = False
        # Настройки основного окна
        self.setGeometry(1300, 120, 510, 370)

        flags = self.windowFlags() | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)

        # Создание ТабВиджета, нужен для нескольких вкладок
        self.tabwidget = QTabWidget()
        # Нужно чтобы данный виджет нормально скейлился в окне (И я не задавал ему геометрию)
        self.setCentralWidget(self.tabwidget)

        # Создание и настройка таба с хоткеями
        self.tab_hot_keys = tab_hot_keys()
        self.tab_hot_keys.signal_refresh_hot_keys.connect(self.add_all_hotkeys)
        self.tab_hot_keys.signal_start_thread_auto_join.connect(self.run_check_restart)
        self.tab_hot_keys.signal_command_eat.connect(self.start_command_eat)
        self.tab_hot_keys.signal_command_lvl.connect(self.start_command_lvl)

        # Создание таба с настройками координат
        self.tab_join_coords = tab_join_coords()

        # Создание таба с логами
        self.tab_logs = tab_logs()

        # Добавление табов
        self.tabwidget.addTab(self.tab_hot_keys, 'Основа')
        self.tabwidget.addTab(self.tab_join_coords, 'Настройки')
        self.tabwidget.addTab(self.tab_logs, 'Логи')

        # Функция добавления всех хоткеев

        self.add_all_hotkeys()

        # Функция создания всех потоков
        self.create_all_thread()

        # Сообщение для логов
        self.add_logs_text(f'[Main] {datetime.now().strftime("%H:%M:%S / %d.%m.%Y")} - Программа запущена')

    def debag_screeonshot_on_coords_tab(self):
        pixmap2 = QPixmap(str('img2.png'))
        self.tab_join_coords.image_compare.setPixmap(pixmap2)

    def add_logs_text(self, new_text):

        self.tab_logs.label_logs.append(new_text)

    def create_all_thread(self):
        print('ALL_TH: Создание всех потоков')
        # Поток на проверку рестартов (Сравнения одной картинки с другой)
        self.thread_check_restart = check_restart()
        # Конект для логов
        self.thread_check_restart.signal_add_logs.connect(self.add_logs_text)
        self.thread_check_restart.signal_stop_all_macros.connect(self.stop_all_macro)
        # Конектиться для изменения картинки в табе с кордами, при работе потока
        self.thread_check_restart.signal_image.connect(self.debag_screeonshot_on_coords_tab)
        # Конект сигнала для запуска макросов, которые были включены до рестарта
        self.thread_check_restart.signal_start_macro_after_join.connect(self.start_macros_after_auto_join)
        # Потоки для макросов
        self.thread_right_click = Macros_right_click()
        self.thread_left_click = Macros_left_click()
        self.thread_bow_shoot = Macros_bow_shoot()
        # Поток для скрола слотов
        self.thread_scroll_slots = Macros_scroll_slots()
        # Конект для выключения всех потоков, когда все слоты будут сломаны
        self.thread_scroll_slots.signal_stop_all_macros.connect(self.stop_all_macro)
        # Поток для команды /eat
        self.thread_command_eat = Macros_eat_command()
        # Поток для команды /lvl
        self.thread_command_lvl = Macros_lvl_command()
        print('ALL_TH: Все потоки были созданы')

    def run_check_restart(self):
        if not self.thread_check_restart.isRunning():
            print('TH-auto_join: ЗАПУСКАЮ')
            self.thread_check_restart.start()
            self.tab_hot_keys.auto_join_thread_btn.setText('Остановить проверку')
        elif self.thread_check_restart.isRunning():
            self.thread_check_restart.terminate()
            self.tab_hot_keys.auto_join_thread_btn.setText('Запуск проверки рестарта')
            print('TH-auto_join: ОФНУЛ')

    def add_all_hotkeys(self):
        print('Hot_Key: Подгрузка хоткеев')
        var_count_hotkey = 0
        # Нужно, чтобы хоткеи не стакались и норм обновлялись
        unhook_all()
        try:
            if not self.tab_hot_keys.right_click_checkbox.isChecked():
                add_hotkey(File.read_file('config.json')["keyboards"]["right_click"], self.start_right_click)
                var_count_hotkey += 1
            if not self.tab_hot_keys.left_click_checkbox.isChecked():
                add_hotkey(File.read_file('config.json')["keyboards"]["left_click"], self.start_left_click)
                var_count_hotkey += 1
            if not self.tab_hot_keys.bow_shoot_checkbox.isChecked():
                add_hotkey(File.read_file('config.json')["keyboards"]["bow_shoot"], self.start_bow_shoot)
                var_count_hotkey += 1
            if not self.tab_hot_keys.scroll_slots_checkbox.isChecked():
                add_hotkey(File.read_file('config.json')["keyboards"]["scroll_slots"], self.start_scroll_slots)
                var_count_hotkey += 1
            print('Hot_Key: Хоткеи загрузились')
            self.tab_hot_keys.warning_label.setText(f'Загружено хоткеев - {var_count_hotkey}')
        except:
            unhook_all()
            print('Hot_Key: Хоткеи не загрузились (ОШИБКА)')
            self.tab_hot_keys.warning_label.setText('ОШИБКА ПРИ ЗАГРУЗКЕ ХОТКЕЕВ')

    def start_command_eat(self):
        if not self.thread_command_eat.isRunning():
            print('MACROS: Начинаю юзать команду /eat')
            self.thread_command_eat.start()
        elif self.thread_command_eat.isRunning():
            print('MACROS: Начинаю юзать команду /eat')
            self.thread_command_eat.terminate()

    def start_command_lvl(self):
        if not self.thread_command_lvl.isRunning():
            print('MACROS: Начинаю юзать команду /lvl')
            self.thread_command_lvl.start()
        elif self.thread_command_lvl.isRunning():
            print('MACROS: Начинаю юзать команду /lvl')
            self.thread_command_lvl.terminate()

    def start_right_click(self):
        if not self.thread_right_click.isRunning():
            print('MACROS: Начинаю кликать ПКМ')
            self.thread_right_click.start()
        elif self.thread_right_click.isRunning():
            print('MACROS: Перестаю кликать ПКМ')
            self.thread_right_click.terminate()

    def start_left_click(self):
        if not self.thread_left_click.isRunning():
            print('MACROS: Начинаю кликать ЛКМ')
            self.thread_left_click.start()
        elif self.thread_left_click.isRunning():
            print('MACROS: Перестаю кликать ЛКМ')
            self.thread_left_click.terminate()

    def start_bow_shoot(self):
        if not self.thread_bow_shoot.isRunning():
            print('MACROS: Начинаю стрелять')
            self.thread_bow_shoot.start()
        elif self.thread_bow_shoot.isRunning():
            print('MACROS: Перестаю стрелять')
            self.thread_bow_shoot.terminate()
            click(button='right')

    def start_scroll_slots(self):
        if not self.thread_scroll_slots.isRunning():
            print('MACROS: Запускаю скролл слотов')
            self.thread_scroll_slots.start()
        elif self.thread_scroll_slots.isRunning():
            print('MACROS: Офаю скролл слотов')
            self.thread_scroll_slots.terminate()

    def stop_all_macro(self, check='False'):
        if check == 'True':
            print('MACROS: Проверка на работающие макросы')
            if self.thread_right_click.isRunning():
                print('MACROS: ПКМ был запущен')
                self.right_click = True
            if self.thread_left_click.isRunning():
                print('MACROS: ЛКМ был запущен')
                self.left_click = True
            if self.thread_bow_shoot.isRunning():
                print('MACROS: Лук был запущен')
                self.bow_shoot = True
            if self.thread_scroll_slots.isRunning():
                print('MACROS: Скролл был запущен')
                self.scroll = True
        print('ALL_TH: ОФАЮ ВСЕ ПОТОКИ')
        self.thread_right_click.terminate()
        self.thread_left_click.terminate()
        self.thread_bow_shoot.terminate()
        self.thread_scroll_slots.terminate()

    def start_macros_after_auto_join(self):
        print('MACROS: Запуск макросов после рестарта')
        if self.right_click:
            self.start_right_click()
        if self.left_click:
            self.start_left_click()
        if self.bow_shoot:
            self.start_bow_shoot()
        if self.scroll:
            self.start_scroll_slots()
        self.right_click = False
        self.left_click = False
        self.bow_shoot = False
        self.scroll = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
