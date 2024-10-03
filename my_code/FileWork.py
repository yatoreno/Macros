import json
import os
import sys

from pygame import mixer


class File:
    @staticmethod
    def read_file(directory):  # Читает и достает инфу из конфига
        #directory = File.resource_path(directory)
        with open(directory, "r", encoding='utf-8') as f:
            cfg = json.load(f)
            return cfg

    @staticmethod
    def coords(key1, key2, directory):  # Достает из конфига корды
        coord = File.read_file(directory)[key1][key2]
        return coord.split(' ')

    @staticmethod
    def resource_path(relative_path):  # Метод для получения директории файла, если он находится запакованный внутри exe
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    # Функция для перезаписи элементов в конфиге
    # key_dict1 - это раздел в конфиге
    # key_dict2 - это ключ, который нужен для получения значения
    @staticmethod
    def rewrite(directory, key_dict1, key_dict2, new_hotkey: str):
        #directory = File.resource_path(directory)
        dictionary = File.read_file(directory)
        dictionary[key_dict1][key_dict2] = new_hotkey
        with open(directory, "w", encoding='utf-8') as f:
            json.dump(dictionary, f, indent=4, ensure_ascii=False)
        print(f'Перезапись хоткея на "{new_hotkey}" ключа {key_dict2}, директории {directory}')

    # Функция для воспроизведения звуков
    @staticmethod
    def play_sound(directory):
        directory = File.resource_path(directory)
        mixer.init()
        mixer.music.load(File.resource_path(directory))
        mixer.music.play()
