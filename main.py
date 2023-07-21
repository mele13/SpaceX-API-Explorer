from PyQt6.QtWidgets import QApplication
from view.mainwindow import MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()    
