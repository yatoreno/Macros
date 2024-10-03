import pyautogui
import datetime

from PySide6.QtCore import QThread, Signal
from my_code.FileWork import File
from my_code.screen_window import screen

from time import sleep


class check_restart(QThread):
    signal_stop_all_macros = Signal(str)

    signal_image = Signal()

    signal_start_macro_after_join = Signal()

    signal_add_logs = Signal(str)

    def __init__(self, parent=None):
        super(check_restart, self).__init__(parent)
        self.directory = 'config.json'

    def run(self):
        print('TH-auto_join: ЗАПУСТИЛОСЬ')
        while True:
            sleep(int(File.read_file(self.directory)["settings"]["screen_time"]))
            screen.screenshot(x=File.coords("screens_coords", "sreenshot_menu", self.directory)[0],
                              # Скринит кнопку гл. меню
                              y=File.coords("screens_coords", "sreenshot_menu", self.directory)[1],
                              wid=File.coords("screens_coords", "sreenshot_menu", self.directory)[2],
                              height=File.coords("screens_coords", "sreenshot_menu", self.directory)[3],
                              name='img2')
            sleep(0.25)
            print('TH-auto_join: Работаю')
            # Отправляет сигнал на установку скрина
            self.signal_image.emit()
            if screen.difference_images():
                print(f'TH-auto_join: {datetime.datetime.now()} - [Рестарт] Замечены одинаковые картинки')
                self.signal_add_logs.emit(f'TH-auto_join: [Рестарт] - {datetime.datetime.now().strftime("%H:%M:%S")}')
                self.signal_stop_all_macros.emit('True')
                auto_join()
                # Сигнал для запуска макросов, которые были запущены до рестарта
                self.signal_start_macro_after_join.emit()


class auto_join:

    def __init__(self):
        self.directory = 'config.json'
        self.join()

    def custom_click(self):  # Обычный клик
        sleep(0.5)
        pyautogui.mouseDown(button='left')
        sleep(0.5)
        pyautogui.mouseUp(button='left')
        sleep(0.5)

    def join(self):  # АВТОПЕРЕЗАХОД
        print('Аuto_Join: Начинаю заходить на сервер')
        pyautogui.moveTo(int(File.coords("join_coords", 'go_to_menu', self.directory)[0]),
                         int(File.coords("join_coords", 'go_to_menu', self.directory)[1]))
        self.custom_click()
        pyautogui.moveTo(int(File.coords("join_coords", 'refresh', self.directory)[0]),
                         int(File.coords("join_coords", 'refresh', self.directory)[1]))
        self.custom_click()
        print('Аuto_Join: Начинаю ждать', int(File.read_file('config.json')["settings"]["time_on_join"]), 'секунд(ы)')
        sleep(int(File.read_file('config.json')["settings"]["time_on_join"]))
        self.custom_click()
        pyautogui.moveTo(int(File.coords("join_coords", 'server', self.directory)[0]),
                         int(File.coords("join_coords", 'server', self.directory)[1]))
        self.custom_click()
        pyautogui.moveTo(int(File.coords("join_coords", 'join', self.directory)[0]),
                         int(File.coords("join_coords", 'join', self.directory)[1]))
        self.custom_click()
        print('Аuto_Join: Ожидаю 15 сек, пока осуществляется вход на сервер')
        sleep(10)
        print('Аuto_Join: Вход выполнен')
