import sys

from PySide6.QtWidgets import QApplication

from my_code.main_window import MainWindow

# Запуск основного окна и всего кода
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())