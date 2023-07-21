import folium
import requests
import json
import sys
import os

sys.path.append("controller")
sys.path.append("model")

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QApplication, QWidget, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from spacex_api_client import SpaceXAPIClient
from launchpad import LaunchPad

downloads_path = "./resources/downloads/launchpads/"

class LaunchPadListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Launch Pad Details')

        self.spacex_api_client = SpaceXAPIClient()

        # Create a widget to display the list of launchpads
        self.launchpad_list_widget = QListWidget()

        # Initialize the details windows dictionary
        self.details_windows = {}

        # Load launchpads information from api
        launchpads = self.load_launchpads()

        # Add a button to download launchpads data in JSON
        self.download_button = QPushButton("Download detailed data")
        self.download_button.clicked.connect(lambda: self.download_json(launchpads))

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.launchpad_list_widget)
        main_layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Show information of the clicked launchpad
        self.launchpad_list_widget.itemClicked.connect(self.show_launchpad_details)
        
    def load_launchpads(self):
        launchpads = self.spacex_api_client.get_launchpads()

        # Get launchpad information from the obtained data
        for launchpad_data in launchpads:
            name = launchpad_data['name']
            full_name = launchpad_data['full_name']
            launchpad = LaunchPad(
                name = name,
                full_name = full_name,
                locality = launchpad_data['locality'],
                region = launchpad_data['region'],
                latitude = launchpad_data['latitude'],
                longitude = launchpad_data['longitude'],
                status = launchpad_data['status'],
                details = launchpad_data['details'],
                images = launchpad_data['images']
            )

            # Create a QListWidgetItem with launchpad information
            item = QListWidgetItem(f'{name}')
            item.setData(Qt.ItemDataRole.UserRole, launchpad)
            self.launchpad_list_widget.addItem(item)

        return launchpads

    def show_launchpad_details(self, item):
        # Retrieve the launchpad from the selected item
        launchpad = item.data(Qt.ItemDataRole.UserRole)

        # Check if the details window already exists
        if launchpad in self.details_windows:
            details_window = self.details_windows[launchpad]
            details_window.show()
        else:
            # Create and show the LaunchPadDetailsWindow with the launchpad details
            details_window = LaunchPadDetailsWindow(launchpad)
            self.details_windows[launchpad] = details_window
            details_window.show()

    def download_json(self, launchpads):
        # Convert the launchpad data to JSON format
        json_data = self.launchpad_to_json(launchpads)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, 'launchpad_detailed_data.json')

        # Save the JSON data to a file
        with open(filename, "w") as json_file:
            json_file.write(json_data)
        
        # Show confirmation dialog with file path
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Download Completed")
        message_box.setText(f"JSON file has been downloaded to:\n{filename}")
        message_box.exec()

    def launchpad_to_json(self, launchpads):
        # Convert the dictionary to JSON format
        json_data = json.dumps(launchpads, indent=2)

        return json_data


class LaunchPadDetailsWindow(QMainWindow):
    def __init__(self, launchpad):
        super().__init__()
        self.setWindowTitle('Launch Pad Details')

        # Create labels to display launchpad details
        self.layout = QVBoxLayout()
        self.label_images = QLabel()
        self.label_name = QLabel(f'Name: {launchpad.full_name}')
        self.label_locality = QLabel(f'Locality: {launchpad.locality}')
        self.label_region = QLabel(f'Region: {launchpad.region}')
        self.label_latitude = QLabel(f'Latitude: {launchpad.latitude}')
        self.label_longitude = QLabel(f'Longitude: {launchpad.longitude}')
        self.label_status = QLabel(f'Status: {launchpad.status}')
        self.label_details = QLabel(f'Details: {launchpad.details}')

        # Add a button to download launchpad's data in JSON
        self.download_button = QPushButton(f'Download {launchpad.name}\'s data')
        self.download_button.clicked.connect(lambda: self.download_json(launchpad))

        # Allow overflow with newlines
        self.label_details.setWordWrap(True)

        # Get image from launchpad images
        image = self.get_image_from_url(launchpad.images)
        
        if image:
            # Scale the image to fit the label and display it
            self.label_images.setPixmap(image.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.label_images.setText("Image not available")

        # Create a QLabel to hold the map as an image
        self.label_map = QLabel()
        self.label_map.setMinimumHeight(400)

        # Generate the map and display it as an image
        map_image = self.generate_map_image(launchpad.latitude, launchpad.longitude)
        self.label_map.setPixmap(map_image)

        # Add the labels to the layout
        self.layout.addWidget(self.label_images)
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.label_locality)
        self.layout.addWidget(self.label_region)
        self.layout.addWidget(self.label_latitude)
        self.layout.addWidget(self.label_longitude)
        self.layout.addWidget(self.label_status)
        self.layout.addWidget(self.label_details)
        self.layout.addWidget(self.label_map)

        # Add the download button to the layout
        self.layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Show the window maximized
        self.showMaximized()

    def generate_map_image(self, latitude, longitude):
        # Create a folium map centered at the specified latitude and longitude
        map_center = [latitude, longitude]
        map_osm = folium.Map(location=map_center, zoom_start=15, tiles='OpenStreetMap')

        # Get the map as a PNG image
        map_png = map_osm._to_png()

        # Create a QPixmap from the image
        map_image = QPixmap()
        map_image.loadFromData(map_png)

        return map_image
    
    def get_image_from_url(self, images_dict):
        if 'large' in images_dict:
            # Get the list of image URLs associated with the 'large' key
            image_list = images_dict['large']

            if image_list:
                image_url = image_list[0] # Get first image URL

                # Download the image from the URL using requests
                response = requests.get(image_url)
                if response.status_code == 200:
                    # Convert the image data to a QPixmap
                    image_data = response.content
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)

                    return pixmap
            
        return None
    
    def download_json(self, launchpad):
        # Create a dictionary with launchpad data
        launchpad_data = {
            'name': launchpad.name,
            'full_name': launchpad.full_name,
            'locality': launchpad.locality,
            'region': launchpad.region,
            'latitude': launchpad.latitude,
            'longitude': launchpad.longitude,
            'status': launchpad.status,
            'details': launchpad.details,
            'images': launchpad.images
        }
        # Convert the launchpad data to JSON format
        json_data = json.dumps(launchpad_data, indent=2)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, f'launchpad_{launchpad.name}_data.json')

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
    launchpad_window = LaunchPadListWindow()
    launchpad_window.show()
    sys.exit(app.exec())
