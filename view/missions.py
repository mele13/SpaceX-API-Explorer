import json
import sys
import os

sys.path.append("controller")
sys.path.append("model")

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QApplication, QWidget, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

from spacex_api_client import SpaceXAPIClient
from mission import Mission

downloads_path = "./resources/downloads/missions/"

class MissionsListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Missions Details')

        self.spacex_api_client = SpaceXAPIClient()

        # Create a widget to display the list of missions
        self.mission_list_widget = QListWidget()

        # Initialize the details windows dictionary
        self.details_windows = {}

        # Load launchpads information from api
        missions = self.load_missions()

        # Add a button to download launchpads data in JSON
        self.download_button = QPushButton("Download detailed data")
        self.download_button.clicked.connect(lambda: self.download_json(missions))

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.mission_list_widget)
        main_layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Show information of the clicked mission
        self.mission_list_widget.itemClicked.connect(self.show_missions_details)
        
    def load_missions(self):
        missions = self.spacex_api_client.get_missions()

        # Get missions information from the obtained data
        for missions_data in missions:

            name = missions_data['mission_name']

            mission = Mission(
                name = name,
                manufacturers = missions_data['manufacturers'],
                payloads = missions_data['payload_ids'],
                wikipedia = missions_data['wikipedia'],
                website = missions_data['website'],
                twitter = missions_data['twitter'],
                description = missions_data['description'],
            )

            # Create a QListWidgetItem with launch information
            item = QListWidgetItem(f'{name}')
            item.setData(Qt.ItemDataRole.UserRole, mission)
            self.mission_list_widget.addItem(item)
        
        return missions

    def show_missions_details(self, item):
        # Retrieve the launch from the selected item
        mission = item.data(Qt.ItemDataRole.UserRole)

        # Check if the details window already exists
        if mission in self.details_windows:
            details_window = self.details_windows[mission]
            details_window.show()
        else:
            # Create and show the MissionDetailsWindow with the mission details
            details_window = MissionDetailsWindow(mission)
            self.details_windows[mission] = details_window
            details_window.show()

    def download_json(self, launches):
        # Convert the launchpad data to JSON format
        json_data = self.mission_to_json(launches)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, 'missions_detailed_data.json')

        # Save the JSON data to a file
        with open(filename, "w") as json_file:
            json_file.write(json_data)
        
        # Show confirmation dialog with file path
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Download Completed")
        message_box.setText(f"JSON file has been downloaded to:\n{filename}")
        message_box.exec()

    def mission_to_json(self, launches):
        # Convert the dictionary to JSON format
        json_data = json.dumps(launches, indent=2)

        return json_data


class MissionDetailsWindow(QMainWindow):
    def __init__(self, mission):
        super().__init__()
        self.setWindowTitle('Mission Details')

        # Create labels to display mission details
        self.layout = QVBoxLayout()        
        self.label_name = QLabel(f'Name: {mission.name}')
        self.label_manufacturers = QLabel(f'Manufacturers: {self.get_separated_data(mission.manufacturers)}')
        self.label_payloads = QLabel(f'Payloads: {self.get_separated_data(mission.payloads)}')        
        self.label_wikipedia = QLabel(f'Wikipedia: <a href="{mission.wikipedia}" target="_blank">{mission.wikipedia}</a>')
        self.label_website = QLabel(f'Website: <a href="{mission.website}" target="_blank">{mission.website}</a>')
        self.label_twitter = QLabel(f'Twitter: <a href="{mission.twitter}" target="_blank">{mission.twitter}</a>')
        self.label_description = QLabel(f'Description: {mission.description}')

        # Make links clickeable
        self.habilitate_external_links()

        # Add a button to download missions's data in JSON
        self.download_button = QPushButton(f'Download {mission.name}\'s data')
        self.download_button.clicked.connect(lambda: self.download_json(mission))

        # Allow overflow with newlines
        self.label_description.setWordWrap(True)
        self.label_payloads.setWordWrap(True)

        # Add the labels to the layout
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.label_manufacturers)
        self.layout.addWidget(self.label_payloads)
        self.layout.addWidget(self.label_wikipedia)
        self.layout.addWidget(self.label_website)
        self.layout.addWidget(self.label_twitter)
        self.layout.addWidget(self.label_description)

        # Add the download button to the layout
        self.layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def get_separated_data(self, data):
        return ', '.join(data)

    def habilitate_external_links(self):
        self.label_wikipedia.setOpenExternalLinks(True)
        self.label_website.setOpenExternalLinks(True)
        self.label_twitter.setOpenExternalLinks(True)
    
    def download_json(self, mission):
        # Create a dictionary with mission data       
        mission_data = {
            'name': mission.name,
            'manufacturers': mission.manufacturers,
            'payloads': mission.payloads,
            'wikipedia': mission.wikipedia,
            'website': mission.website,
            'twitter': mission.twitter,
            'description': mission.description
        }
        # Convert the mission data to JSON format
        json_data = json.dumps(mission_data, indent=2)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, f'mission_{mission.name}_data.json')

        # Save the JSON data to a file
        with open(filename, "w") as json_file:
            json_file.write(json_data)

        # Show confirmation dialog with file path
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Download Completed")
        message_box.setText(f"JSON file has been downloaded to:\n{filename}")
        message_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    launchpad_window = MissionsListWindow()
    launchpad_window.show()
    sys.exit(app.exec())
