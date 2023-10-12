from PySide6.QtCore import QThread, Signal
from my_code.FileWork import File
from pyautogui import tripleClick, click, mouseUp, mouseDown
from keyboard import send, write

from my_code.screen_window import screen

from time import sleep


class Macros_right_click(QThread):

    def run(self):
        while True:
            click(button='right')
            sleep(0.01)


class Macros_left_click(QThread):

    def run(self):
        while True:
            tripleClick(button='left')
            sleep(0.1)


class Macros_bow_shoot(QThread):

    def run(self):
        while True:
            mouseDown(button='right')
            sleep(1.1)
            mouseUp(button='right')


class Macros_eat_command(QThread):

    def run(self):
        while True:
            sleep(60)
            send('t')
            sleep(0.5)
            write("/eat", delay=0.1)
            sleep(0.5)
            send('enter')


class Macros_lvl_command(QThread):

    def run(self):
        while True:
            sleep(1200)
            send('t')
            sleep(0.5)
            write("/lvl", delay=0.1)
            sleep(0.5)
            send('enter')


class Macros_scroll_slots(QThread):
    signal_stop_all_macros = Signal()

    def __init__(self, parent=None):
        super(Macros_scroll_slots, self).__init__(parent)
        self.directory = 'config.json'

    def run(self):
        x = 1
        list_slots = []
        while True:
            count_slots = int(File.read_file(self.directory)["settings"]["count_slots"])
            if x > int(count_slots):  # Проверка на то прошли ли все слоты по кругу
                x = 1
            send(str(x))
            x += 1
            if len(list_slots) == int(count_slots):  # После того как все слоты непригодны, вырубает все
                print('MACROS A-J: Выключаю все макросы потому, что все слоты сломаны')
                self.signal_stop_all_macros.emit()
                break
            if x - 1 in list_slots:  # Если слот в списке не жмет на него
                continue
            sleep(0.2)
            if screen.check_item() and x - 1 not in list_slots:  # Скринит предмет и проверяет на поломку
                list_slots.append(x - 1)
                print(f'MACROS A-J: Слоты, которые не используются - {list_slots}')
                continue
            sleep(int(File.read_file(self.directory)["settings"]["time_on_slot"]))
