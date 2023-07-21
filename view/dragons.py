import requests
import json
import sys
import os

sys.path.append("controller")
sys.path.append("model")

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QApplication, QWidget, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from spacex_api_client import SpaceXAPIClient
from dragon import Dragon

downloads_path = "./resources/downloads/dragons/"

class DragonsListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dragon Details')

        self.spacex_api_client = SpaceXAPIClient()

        # Create a widget to display the list of dragons
        self.dragons_list_widget = QListWidget()

        # Initialize the details windows dictionary
        self.details_windows = {}

        # Load dragons information from api
        launches = self.load_dragons()

        # Add a button to download dragons data in JSON
        self.download_button = QPushButton("Download detailed data")
        self.download_button.clicked.connect(lambda: self.download_json(launches))

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.dragons_list_widget)
        main_layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Show information of the clicked launchpad
        self.dragons_list_widget.itemClicked.connect(self.show_dragons_details)
        
    def load_dragons(self):
        dragons = self.spacex_api_client.get_dragons()

        # Get dragons information from the obtained data
        for dragon_data in dragons:
            name = dragon_data['name']
            dragon = Dragon(
                name = name,
                type = dragon_data['type'],
                active = dragon_data['active'],                
                crew_capacity = dragon_data['crew_capacity'],
                orbit_duration_yr = dragon_data['orbit_duration_yr'],
                dry_mass_kg = dragon_data['dry_mass_kg'],
                heat_shield_material = dragon_data['heat_shield']['material'],
                heat_shield_dev = dragon_data['heat_shield']['dev_partner'],
                launch_payload_mass = dragon_data['launch_payload_mass']['kg'],
                return_payload_mass = dragon_data['return_payload_mass']['kg'],
                launch_payload_vol = dragon_data['launch_payload_vol']['cubic_meters'],
                return_payload_vol = dragon_data['return_payload_vol']['cubic_meters'],
                first_flight = dragon_data['first_flight'],
                thrusters = dragon_data['thrusters'],
                wikipedia = dragon_data['wikipedia'],
                description = dragon_data['description'],
                images = dragon_data['flickr_images'],
            )

            # Create a QListWidgetItem with dragon information
            item = QListWidgetItem(f'{name}')
            item.setData(Qt.ItemDataRole.UserRole, dragon)
            self.dragons_list_widget.addItem(item)
        
        return dragons

    def show_dragons_details(self, item):
        # Retrieve the dragon from the selected item
        dragon = item.data(Qt.ItemDataRole.UserRole)

        # Check if the details window already exists
        if dragon in self.details_windows:
            details_window = self.details_windows[dragon]
            details_window.show()
        else:
            # Create and show the DragonDetailsWindow with the dragon details
            details_window = DragonDetailsWindow(dragon)
            self.details_windows[dragon] = details_window
            details_window.show()

    def download_json(self, dragons):
        # Convert the dragon data to JSON format
        json_data = self.launch_to_json(dragons)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, 'dragons_detailed_data.json')

        # Save the JSON data to a file
        with open(filename, "w") as json_file:
            json_file.write(json_data)
        
        # Show confirmation dialog with file path
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Download Completed")
        message_box.setText(f"JSON file has been downloaded to:\n{filename}")
        message_box.exec()

    def launch_to_json(self, launches):
        # Convert the dictionary to JSON format
        json_data = json.dumps(launches, indent=2)

        return json_data


class DragonDetailsWindow(QMainWindow):
    def __init__(self, dragon):
        super().__init__()
        self.setWindowTitle('Dragon Details')

        # Create labels to display dragon details
        self.label_name = QLabel(f'Name: {dragon.name}')
        self.label_type = QLabel(f'Type: {dragon.type}')
        self.label_active = QLabel(f'Active: {dragon.active}')
        self.label_crew_capacity = QLabel(f'Crew Capacity: {dragon.crew_capacity}')
        self.label_orbit_duration = QLabel(f'Orbit Duration (years): {dragon.orbit_duration_yr}')
        self.label_dry_mass_kg = QLabel(f'Dry Mass (kg): {dragon.dry_mass_kg}')
        self.label_heat_shield_material = QLabel(f'Heat Shield Material: {dragon.heat_shield_material}')
        self.label_heat_shield_dev = QLabel(f'Heat Shield Developer: {dragon.heat_shield_dev}')
        self.label_launch_payload_mass = QLabel(f'Launch Payload Mass (kg): {dragon.launch_payload_mass}')
        self.label_return_payload_mass = QLabel(f'Return Payload Mass (kg): {dragon.return_payload_mass}')
        self.label_launch_payload_vol = QLabel(f'Launch Payload Volume (cubic meters): {dragon.launch_payload_vol}')
        self.label_return_payload_vol = QLabel(f'Return Payload Volume (cubic meters): {dragon.return_payload_vol}')
        self.label_first_flight = QLabel(f'First Flight: {dragon.first_flight}')
        self.label_thrusters = QLabel(f'Thrusters:')
        self.label_wikipedia = QLabel(f'Wikipedia: <a href="{dragon.wikipedia}" target="_blank">{dragon.wikipedia}</a>')
        self.label_description = QLabel(f'Description: {dragon.description}')

        # Create a QHBoxLayout to hold the image labels
        self.image_layout = QHBoxLayout()

        # Check if there are images to display
        if not dragon.images:
            # No images available, display the "No image available" text
            no_image_label = QLabel("No image(s) available")
            self.image_layout.addWidget(no_image_label)
        else:
            # Get images from dragon images URLs
            for image_url in dragon.images:
                image = self.get_image_from_url(image_url)
                if image:
                    # Create a QLabel for each image and add it to the image layout
                    image_label = QLabel()
                    image_label.setPixmap(image.scaledToWidth(200))
                    self.image_layout.addWidget(image_label)

        # Make links clickeable
        self.habilitate_external_links()

        # Add a button to download dragon's data in JSON
        self.download_button = QPushButton(f'Download {dragon.name}\'s data')
        self.download_button.clicked.connect(lambda: self.download_json(dragon))

        # Allow overflow with newlines
        self.label_description.setWordWrap(True)
        
        # Get thrusters from dragon data
        thrusters = dragon.thrusters

        # Add the labels to the layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.label_type)
        self.layout.addWidget(self.label_active)
        self.layout.addWidget(self.label_crew_capacity)
        self.layout.addWidget(self.label_orbit_duration)
        self.layout.addWidget(self.label_dry_mass_kg)
        self.layout.addWidget(self.label_heat_shield_material)
        self.layout.addWidget(self.label_heat_shield_dev)
        self.layout.addWidget(self.label_launch_payload_mass)
        self.layout.addWidget(self.label_return_payload_mass)
        self.layout.addWidget(self.label_launch_payload_vol)
        self.layout.addWidget(self.label_return_payload_vol)
        self.layout.addWidget(self.label_first_flight)
        self.layout.addWidget(self.label_thrusters)

        # Check if there are thrusters to display
        if thrusters:
            # Iterate over the thrusters list and create labels for each thruster
            for idx, thruster in enumerate(thrusters):
                thruster_label = QLabel(f"\tThruster {idx + 1} -> Type: {thruster['type']}; Fuel 1: {thruster['fuel_1']}, Fuel 2: {thruster['fuel_2']}, Isp: {thruster['isp']}, Thrust: {thruster['thrust']['kN']} kN, {thruster['thrust']['lbf']} lbf")

                # Add the thruster labels to the layout
                self.layout.addWidget(thruster_label)
        else:
            # No thrusters available, display a label indicating that there are no thrusters
            no_thrusters_label = QLabel("No thrusters available")
            self.layout.addWidget(no_thrusters_label)

        self.layout.addWidget(self.label_wikipedia)
        self.layout.addLayout(self.image_layout) # Add the labels to the QVBoxLayout
        self.layout.addWidget(self.label_description)

        # Add the download button to the layout
        self.layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # # Show the window maximized
        # self.showMaximized()

    def get_separated_data(self, data):
        return ', '.join(data)

    def habilitate_external_links(self):
        self.label_wikipedia.setOpenExternalLinks(True)
    
    def get_image_from_url(self, image_url):
        # Download the image from the URL using requests
        response = requests.get(image_url)
        if response.status_code == 200:
            # Convert the image data to a QPixmap
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            return pixmap
            
        return None
    
    def download_json(self, dragon):
        # Create a dictionary with dragon data       
        dragon_data = {
            'heat_shield_material': dragon.heat_shield_material,
            'heat_shield_dev': dragon.heat_shield_dev,
            'launch_payload_mass': dragon.launch_payload_mass,
            'return_payload_mass': dragon.return_payload_mass,
            'launch_payload_vol': dragon.launch_payload_vol,
            'return_payload_vol': dragon.return_payload_vol,
            'first_flight': dragon.first_flight,
            'name': dragon.name,
            'type': dragon.type,
            'active': dragon.active,
            'crew_capacity': dragon.crew_capacity,
            'orbit_duration_yr': dragon.orbit_duration_yr,
            'dry_mass_kg': dragon.dry_mass_kg,
            'thrusters': dragon.thrusters,
            'wikipedia': dragon.wikipedia,
            'description': dragon.description,
            'images': dragon.images,
        }
        # Convert the dragon data to JSON format
        json_data = json.dumps(dragon_data, indent=2)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, f'dragon_{dragon.name}_data.json')

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
    launchpad_window = DragonsListWindow()
    launchpad_window.show()
    sys.exit(app.exec())
