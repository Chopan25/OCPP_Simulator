import sys
from PyQt6 import QtWidgets
from window_controller import mainWindow

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = mainWindow()
        window.show()
        sys.exit(app.exec())
    except:
        print("main - Unexpected error:", sys.exc_info()[0])
        exit(1)
