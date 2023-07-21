from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

from view.launchpads import LaunchPadListWindow
from view.launches import LaunchesListWindow
from view.missions import MissionsListWindow
from view.history import HistoryListWindow
from view.dragons import DragonsListWindow
from view.rockets import RocketsListWindow

class Label(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent = parent)
        self.p = QPixmap()

    def setPixmap(self, p):
        self.p = p
        self.update()

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SpaceX API Explorer')

        # Set the size of the main window
        self.setFixedSize(800, 800)

        # Create a central widget and a vertical layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Create a label for the image
        image_label = Label(self)
        pixmap = QPixmap("resources/images/spaceX_main.jpg")
        image_label.setPixmap(pixmap)

        # Set the size policy of the label to expanding
        image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add the image label to the layout
        layout.addWidget(image_label)

        # Create the first horizontal layout for the top row buttons
        buttons_row1_layout = QHBoxLayout()
        launchpads_list = QPushButton("Launchpads", self)
        launches_list = QPushButton("Launches", self)
        missions_list = QPushButton("Missions", self)
        buttons_row1_layout.addWidget(launchpads_list)
        buttons_row1_layout.addWidget(launches_list)
        buttons_row1_layout.addWidget(missions_list)

        # Create the second horizontal layout for the bottom row buttons
        buttons_row2_layout = QHBoxLayout()
        history_list = QPushButton("History", self)
        dragons_list = QPushButton("Dragons", self)
        rockets_list = QPushButton("Rockets", self)
        buttons_row2_layout.addWidget(history_list)
        buttons_row2_layout.addWidget(dragons_list)
        buttons_row2_layout.addWidget(rockets_list)

        # Add both horizontal layouts to the main vertical layout
        layout.addLayout(buttons_row1_layout)
        layout.addLayout(buttons_row2_layout)

        # Set the alignment of the buttons_layout to align the horizontal layouts to the top
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set the central widget in the main window
        self.setCentralWidget(central_widget)

        # Button actions
        launchpads_list.clicked.connect(self.launchpad_list_window)
        launches_list.clicked.connect(self.launches_list_window)
        missions_list.clicked.connect(self.missions_list_window)
        history_list.clicked.connect(self.history_list_window)
        dragons_list.clicked.connect(self.dragons_list_window)
        rockets_list.clicked.connect(self.rockets_list_window)

    def launchpad_list_window(self):
        self.launchpad_list_window = LaunchPadListWindow()
        self.launchpad_list_window.show()

    def launches_list_window(self):
        self.launches_list_window = LaunchesListWindow()
        self.launches_list_window.show()

    def missions_list_window(self):
        self.missions_list_window = MissionsListWindow()
        self.missions_list_window.show()

    def history_list_window(self):
        self.history_list_window = HistoryListWindow()
        self.history_list_window.show()

    def dragons_list_window(self):
        self.dragons_list_window = DragonsListWindow()
        self.dragons_list_window.show()

    def rockets_list_window(self):
        self.rockets_list_window = RocketsListWindow()
        self.rockets_list_window.show()
