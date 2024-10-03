from PIL import Image, ImageChops
from pyautogui import screenshot as scr

from my_code.FileWork import File


class screen:

    @staticmethod
    def screenshot(x, y, wid, height, name):  # Скринит экран upd:монитор не должен быть выкл
        scr(f"{name}.png", region=(x, y, wid, height))
        Image.open(f"{name}.png").convert("RGB").save(f"{name}.png")

    @staticmethod
    def check_item():  # Сравнивает пиксели на экране
        directory = 'config.json'
        print('Screen-Window: Скриню и проверяю предмет')
        screen.screenshot(x=File.coords("screens_coords", "screenshot_item", directory)[0],
                          y=File.coords("screens_coords", "screenshot_item", directory)[1],
                          wid=File.coords("screens_coords", "screenshot_item", directory)[2],
                          height=File.coords("screens_coords", "screenshot_item", directory)[3],
                          name=f'img_item')
        image = Image.open('img_item.png')
        width = image.size[0]  # Определяем ширину
        height = image.size[1]  # Определяем высоту
        pix = image.load()  # Выгружаем значения пикселей
        for x in range(width):
            for y in range(height):
                r = pix[x, y][0]  # узнаём значение красного цвета пикселя
                g = pix[x, y][1]  # зелёного
                b = pix[x, y][2]  # синего
                if 160 < r < 180 and g == 0 and b == 0:  # Нашел поломку
                    print('Screen-Window: Была найдена поломка на предмете')
                    return True

    @staticmethod
    def difference_images(img1='img1.png', img2='img2.png'):  # Проверка на то был ли рестарт
        image_1 = Image.open(img1)
        image_2 = Image.open(img2)
        result = ImageChops.difference(image_1, image_2).getbbox()
        if result is None:
            print('Screen-Window: Нашел сравнения для авто-входа')
            return True
        else:
            return False
