import sys

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from my_code.FileWork import File
from my_code.main_window import MainWindow

# Запуск основного окна и всего кода
if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QtGui.QIcon(File.resource_path('app.ico')))
    print(File.resource_path('app.ico'))

    w = MainWindow()
    w.show()
    sys.exit(app.exec())
