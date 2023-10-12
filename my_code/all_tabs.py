from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QTextEdit, QCheckBox
from my_code.FileWork import File

from my_code.screen_window import screen


class tab_hot_keys(QWidget):

    signal_start_thread_auto_join = Signal()
    signal_refresh_hot_keys = Signal()

    signal_command_eat = Signal()
    signal_command_lvl = Signal()

    def __init__(self, parent=None):
        super(tab_hot_keys, self).__init__(parent)

        self.directory = 'config.json'
        self.key_dict1 = "keyboards"
        self.key_dict2 = 'settings'
        self.key_dict3 = 'chekboxs'

        # Все HotKeys Qlabel (Нужны чисто для информации)
        self.label_left_click_hotkey = QLabel(self)
        self.label_left_click_hotkey.setText('Кнопка для ЛКМ:')
        self.label_left_click_hotkey.move(5, 10)

        self.label_scroll_slots = QLabel(self)
        self.label_scroll_slots.move(5, 50)
        self.label_scroll_slots.setText('Кнопка для скорола слотов:')

        self.label_bow_shoot = QLabel(self)
        self.label_bow_shoot.move(5, 90)
        self.label_bow_shoot.setText('Кнопка для лука:')

        self.label_right_click = QLabel(self)
        self.label_right_click.move(5, 130)
        self.label_right_click.setText('Кнопка для ПКМ:')

        # Чекбоксы для команд, которые будут работать в своем потоке

        self.command_eat_checkbox = QCheckBox(self)
        self.command_eat_checkbox.move(5, 195)
        self.command_eat_checkbox.setText('Прописывать команду /eat раз в минуту')
        self.command_eat_checkbox.clicked.connect(self.signal_command_eat.emit)


        self.command_lvl_checkbox = QCheckBox(self)
        self.command_lvl_checkbox.move(5, 215)
        self.command_lvl_checkbox.setText('Прописывать команду /lvl раз в 20 минут')
        self.command_lvl_checkbox.clicked.connect(self.signal_command_lvl.emit)


        # Чекбоксы для работы нумпадов

        self.left_click_checkbox = QCheckBox(self)
        self.left_click_checkbox.move(140, 30)
        self.left_click_checkbox.clicked.connect(self.block_hotkeys_with_checkbox)

        self.scroll_slots_checkbox = QCheckBox(self)
        self.scroll_slots_checkbox.move(140, 70)
        self.scroll_slots_checkbox.clicked.connect(self.block_hotkeys_with_checkbox)

        self.bow_shoot_checkbox = QCheckBox(self)
        self.bow_shoot_checkbox.move(140, 110)
        self.bow_shoot_checkbox.clicked.connect(self.block_hotkeys_with_checkbox)

        self.right_click_checkbox = QCheckBox(self)
        self.right_click_checkbox.move(140, 150)
        self.right_click_checkbox.clicked.connect(self.block_hotkeys_with_checkbox)

        # Стиль для чекбоксов
        self.blockStyle = '''
                QLineEdit {
                    color: rgb(255, 255, 255);
                    background-color: rgb(165, 165, 165);
                }
            '''


        # Все HotKeys settings Qlabel (Нужны чисто для информации)

        self.label_count_slots = QLabel(self)
        self.label_count_slots.move(200, 10)
        self.label_count_slots.setText('Кол-во слотов:')

        self.label_time_on_slot = QLabel(self)
        self.label_time_on_slot.move(200, 50)
        self.label_time_on_slot.setText('Время на 1 слот:')

        self.label_screen_time = QLabel(self)
        self.label_screen_time.move(200, 90)
        self.label_screen_time.setText('Время скрина (На проверку рестарта):')

        self.label_time_on_join = QLabel(self)
        self.label_time_on_join.move(200, 130)
        self.label_time_on_join.setText('Время, сколько длится рестарт (Делайте с запасом):')

        # Текст ошибки
        self.warning_label = QLabel(self)
        self.warning_label.setGeometry(5, 160, 300, 40)

        # Кнопка для обновления макросов (В случае ошибки и т.д.)
        self.refresh_hotkey_btn = QPushButton(self)
        self.refresh_hotkey_btn.setText('Обновить Горячии кнопки')
        self.refresh_hotkey_btn.move(25, 270)
        # Отправляет сигнал для запуска функции в основном классе на обновление хоткеев
        self.refresh_hotkey_btn.clicked.connect(self.signal_refresh_hot_keys.emit)

        # Кнопка для запуска/остановки потока на проверку рестарта
        self.auto_join_thread_btn = QPushButton(self)
        self.auto_join_thread_btn.setText('Запуск проверки рестарта')
        self.auto_join_thread_btn.move(220, 270)
        # Отправляет сигнал для запуска функции в основном классе
        self.auto_join_thread_btn.clicked.connect(self.signal_start_thread_auto_join.emit)

        # ЛАЙН Едиты для настройки ХОТКЕЕВ
        self.left_click_edit = QLineEdit(self)
        self.left_click_edit.setText(File.read_file(self.directory)[self.key_dict1]["left_click"])
        self.left_click_edit.move(5, 25)
        self.left_click_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'left_click', new_hotkey=self.left_click_edit.text()))

        self.scroll_slots_edit = QLineEdit(self)
        self.scroll_slots_edit.setText(File.read_file(self.directory)[self.key_dict1]["scroll_slots"])
        self.scroll_slots_edit.move(5, 65)
        self.scroll_slots_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'scroll_slots',
                                 new_hotkey=self.scroll_slots_edit.text()))

        self.bow_shoot_edit = QLineEdit(self)
        self.bow_shoot_edit.setText(File.read_file(self.directory)[self.key_dict1]["bow_shoot"])
        self.bow_shoot_edit.move(5, 105)
        self.bow_shoot_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'bow_shoot', new_hotkey=self.bow_shoot_edit.text()))

        self.right_click_edit = QLineEdit(self)
        self.right_click_edit.setText(File.read_file(self.directory)[self.key_dict1]["right_click"])
        self.right_click_edit.move(5, 145)
        self.right_click_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'right_click',
                                 new_hotkey=self.right_click_edit.text()))

        # ЛАЙН Едиты для настройки макросов
        self.count_slots_edit = QLineEdit(self)
        self.count_slots_edit.setText(File.read_file(self.directory)[self.key_dict2]["count_slots"])
        self.count_slots_edit.move(200, 25)
        self.count_slots_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict2, 'count_slots',
                                 new_hotkey=self.count_slots_edit.text()))

        self.time_on_slot_edit = QLineEdit(self)
        self.time_on_slot_edit.setText(File.read_file(self.directory)[self.key_dict2]["time_on_slot"])
        self.time_on_slot_edit.move(200, 65)
        self.time_on_slot_edit.textChanged.connect(lambda: File.rewrite(self.directory, self.key_dict2, 'time_on_slot',
                                                                        new_hotkey=self.time_on_slot_edit.text()))

        self.screen_time_edit = QLineEdit(self)
        self.screen_time_edit.setText(File.read_file(self.directory)[self.key_dict2]["screen_time"])
        self.screen_time_edit.move(200, 105)
        self.screen_time_edit.textChanged.connect(lambda: File.rewrite(self.directory, self.key_dict2, 'screen_time',
                                                                       new_hotkey=self.screen_time_edit.text()))

        self.time_on_join_edit = QLineEdit(self)
        self.time_on_join_edit.setText(File.read_file(self.directory)[self.key_dict2]["time_on_join"])
        self.time_on_join_edit.move(200, 145)
        self.time_on_join_edit.textChanged.connect(lambda: File.rewrite(self.directory, self.key_dict2, 'time_on_join',
                                                                        new_hotkey=self.time_on_join_edit.text()))
        # Загрузка чекбоксов
        self.load_checkboxs()

    # Загрузка состояния чекбоксов из конфига
    def load_checkboxs(self):
        if File.read_file('config.json')["chekboxs"]["left_click_checkbox"]:
            self.left_click_checkbox.setChecked(1)
            self.left_click_edit.setStyleSheet(self.blockStyle)
        if File.read_file('config.json')["chekboxs"]["scroll_slots_checkbox"]:
            self.scroll_slots_checkbox.setChecked(1)
            self.scroll_slots_edit.setStyleSheet(self.blockStyle)
        if File.read_file('config.json')["chekboxs"]["bow_shoot_checkbox"]:
            self.bow_shoot_checkbox.setChecked(1)
            self.bow_shoot_edit.setStyleSheet(self.blockStyle)
        if File.read_file('config.json')["chekboxs"]["right_click_checkbox"]:
            self.right_click_checkbox.setChecked(1)
            self.right_click_edit.setStyleSheet(self.blockStyle)

        # if File.read_file('config.json')["chekboxs"]["command_eat_checkbox"]:
        #     self.command_eat_checkbox.setChecked(1)
        # if File.read_file('config.json')["chekboxs"]["command_lvl_checkbox"]:
        #     self.command_lvl_checkbox.setChecked(1)

    # def rewrite_command_checkbox(self):
    #     File.rewrite(self.directory, self.key_dict3, 'command_eat_checkbox',
    #                  new_hotkey=self.command_eat_checkbox.isChecked())
    #     File.rewrite(self.directory, self.key_dict3, 'command_lvl_checkbox',
    #                  new_hotkey=self.command_lvl_checkbox.isChecked())

    # Блочим хоткеи по чекбоксам (Выглядит как высер хех)
    def block_hotkeys_with_checkbox(self):
        unblockStyle = '''
                QLineEdit {
                    color: rgb(0, 0, 0);
                    background-color: rgb(255, 255, 255);
                }
            '''
        self.signal_refresh_hot_keys.emit()
        if self.left_click_checkbox.isChecked():
            self.left_click_edit.setStyleSheet(self.blockStyle)
        else:
            self.left_click_edit.setStyleSheet(unblockStyle)
        if self.scroll_slots_checkbox.isChecked():
            self.scroll_slots_edit.setStyleSheet(self.blockStyle)
        else:
            self.scroll_slots_edit.setStyleSheet(unblockStyle)
        if self.bow_shoot_checkbox.isChecked():
            self.bow_shoot_edit.setStyleSheet(self.blockStyle)
        else:
            self.bow_shoot_edit.setStyleSheet(unblockStyle)
        if self.right_click_checkbox.isChecked():
            self.right_click_edit.setStyleSheet(self.blockStyle)
        else:
            self.right_click_edit.setStyleSheet(unblockStyle)
        # Перезапись в конфиге чекбоксов
        File.rewrite(self.directory, self.key_dict3, 'left_click_checkbox',
                     new_hotkey=self.left_click_checkbox.isChecked())
        File.rewrite(self.directory, self.key_dict3, 'scroll_slots_checkbox',
                     new_hotkey=self.scroll_slots_checkbox.isChecked())
        File.rewrite(self.directory, self.key_dict3, 'bow_shoot_checkbox',
                     new_hotkey=self.bow_shoot_checkbox.isChecked())
        File.rewrite(self.directory, self.key_dict3, 'right_click_checkbox',
                     new_hotkey=self.right_click_checkbox.isChecked())

##########################
class tab_join_coords(QWidget):

    def __init__(self, parent=None):
        super(tab_join_coords, self).__init__(parent)

        # Конфиг
        self.directory = 'config.json'
        # Ключ для авто-входа
        self.key_dict1 = 'join_coords'
        # Ключ для скриншотов
        self.key_dict2 = 'screens_coords'

        self.Test_line_edit = QLineEdit(self)
        self.Test_line_edit.move(245, 140)

        # Текст над едитами нужен для информации

        self.label_coords_image_go_to_menu = QLabel(self)
        self.label_coords_image_go_to_menu.move(5, 0)
        self.label_coords_image_go_to_menu.setText('Координаты кнопки "Вернуться в игру"')

        self.label_coords_refresh_edit = QLabel(self)
        self.label_coords_refresh_edit.move(5, 40)
        self.label_coords_refresh_edit.setText('Координаты кнопки "Обновить"')

        self.label_coords_server_edit = QLabel(self)
        self.label_coords_server_edit.move(5, 80)
        self.label_coords_server_edit.setText('Координаты для выбора сервера')

        self.label_coords_join = QLabel(self)
        self.label_coords_join.move(5, 120)
        self.label_coords_join.setText('Координаты кнопки "войти":')

        self.label_setting_go_to_menu = QLabel(self)
        self.label_setting_go_to_menu.move(245, 0)
        self.label_setting_go_to_menu.setText('Параметры картинки для сравнения:')

        self.label_setting_image_item = QLabel(self)
        self.label_setting_image_item.move(245, 40)
        self.label_setting_image_item.setText('Параметры картинки для проверки прочности:')

        ######################################
        self.pixmap1 = QPixmap(str('img1.png'))
        self.pixmap2 = QPixmap(str('img2.png'))
        self.pixmap3 = QPixmap(str('img_item.png'))

        self.image_go_to_menu = QLabel(self)
        self.image_go_to_menu.setGeometry(10, 160, 400, 60)
        self.image_go_to_menu.setPixmap(self.pixmap1)

        self.image_compare = QLabel(self)
        self.image_compare.setGeometry(10, 220, 400, 60)
        self.image_compare.setPixmap(self.pixmap2)

        self.image_item = QLabel(self)
        self.image_item.setGeometry(10, 290, 400, 60)
        self.image_item.setPixmap(self.pixmap3)

        self.create_screenshot_btn = QPushButton(self)
        self.create_screenshot_btn.setText('Create Screen')
        self.create_screenshot_btn.move(110, 300)
        self.create_screenshot_btn.clicked.connect(self.create_screen_img1)

        self.create_img_item_btn = QPushButton(self)
        self.create_img_item_btn.setText('Create ITEM')
        self.create_img_item_btn.move(200, 300)
        self.create_img_item_btn.clicked.connect(self.debug_img_item)

        ####################################################

        # ЛАЙН Едиты для настройки координат авто-входа в игру
        self.go_to_menu_edit = QLineEdit(self)
        self.go_to_menu_edit.setText(File.read_file(self.directory)[self.key_dict1]["go_to_menu"])
        self.go_to_menu_edit.move(5, 20)
        self.go_to_menu_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'go_to_menu', new_hotkey=self.go_to_menu_edit.text()))

        self.refresh_edit = QLineEdit(self)
        self.refresh_edit.setText(File.read_file(self.directory)[self.key_dict1]["refresh"])
        self.refresh_edit.move(5, 60)
        self.refresh_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'refresh', new_hotkey=self.refresh_edit.text()))

        self.server_edit = QLineEdit(self)
        self.server_edit.setText(File.read_file(self.directory)[self.key_dict1]["server"])
        self.server_edit.move(5, 100)
        self.server_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'server', new_hotkey=self.server_edit.text()))

        self.join_edit = QLineEdit(self)
        self.join_edit.setText(File.read_file(self.directory)[self.key_dict1]["join"])
        self.join_edit.move(5, 140)
        self.join_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict1, 'join', new_hotkey=self.join_edit.text()))

        # ЛАЙН Едиты для настройки координат скриншотов
        self.sreenshot_menu_edit = QLineEdit(self)
        self.sreenshot_menu_edit.setText(File.read_file(self.directory)[self.key_dict2]["sreenshot_menu"])
        self.sreenshot_menu_edit.move(245, 20)
        self.sreenshot_menu_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict2, 'sreenshot_menu',
                                 new_hotkey=self.sreenshot_menu_edit.text()))

        self.screenshot_item_edit = QLineEdit(self)
        self.screenshot_item_edit.setText(File.read_file(self.directory)[self.key_dict2]["screenshot_item"])
        self.screenshot_item_edit.move(245, 60)
        self.screenshot_item_edit.textChanged.connect(
            lambda: File.rewrite(self.directory, self.key_dict2, 'screenshot_item',
                                 new_hotkey=self.screenshot_item_edit.text()))

    # Функция для создания скрина с которым будут сравнивать
    def create_screen_img1(self):
        x = File.coords("screens_coords", "sreenshot_menu", self.directory)[0]
        y = File.coords("screens_coords", "sreenshot_menu", self.directory)[1]
        wid = File.coords("screens_coords", "sreenshot_menu", self.directory)[2]
        height = File.coords("screens_coords", "sreenshot_menu", self.directory)[3]
        name = 'img1'
        screen.screenshot(x=x, y=y, wid=wid, height=height, name=name)
        self.pixmap1 = QPixmap(str('img1.png'))
        self.image_go_to_menu.setPixmap(self.pixmap1)

    def debug_img_item(self):
        x = File.coords("screens_coords", "screenshot_item", self.directory)[0]
        y = File.coords("screens_coords", "screenshot_item", self.directory)[1]
        wid = File.coords("screens_coords", "screenshot_item", self.directory)[2]
        height = File.coords("screens_coords", "screenshot_item", self.directory)[3]
        name = 'img_item'
        screen.screenshot(x=x, y=y, wid=wid, height=height, name=name)
        self.pixmap3 = QPixmap(str('img_item.png'))
        self.image_item.setPixmap(self.pixmap3)


class tab_logs(QWidget):

    def __init__(self, parent=None):
        super(tab_logs, self).__init__(parent)

        self.label_logs = QTextEdit(self)
        self.label_logs.setReadOnly(True)
        self.label_logs.setGeometry(5, 5, 495, 330)
