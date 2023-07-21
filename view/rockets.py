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
from rocket import Rocket

downloads_path = "./resources/downloads/rockets/"

class RocketsListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Rockets Details')

        self.spacex_api_client = SpaceXAPIClient()

        # Create a widget to display the list of rocket
        self.rockets_list_widget = QListWidget()

        # Initialize the details windows dictionary
        self.details_windows = {}

        # Load rockets information from api
        rockets = self.load_rockets()

        # Add a button to download rockets data in JSON
        self.download_button = QPushButton("Download detailed data")
        self.download_button.clicked.connect(lambda: self.download_json(rockets))

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.rockets_list_widget)
        main_layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Show information of the clicked rocket
        self.rockets_list_widget.itemClicked.connect(self.show_rockets_details)
        
    def load_rockets(self):
        rockets = self.spacex_api_client.get_rockets()

        # Get rockets information from the obtained data
        for rockets_data in rockets:
            name = rockets_data['name']
            rocket = Rocket(
                height = rockets_data['height']['meters'],
                diameter = rockets_data['diameter']['meters'],
                mass_kg = rockets_data['mass']['kg'],
                fs_engines = rockets_data['first_stage']['engines'],
                fs_fuel_amount_tons = rockets_data['first_stage']['fuel_amount_tons'],
                fs_burn_time_sec = rockets_data['first_stage']['burn_time_sec'],
                fs_thrust_sea_level = rockets_data['first_stage']['thrust_sea_level']['kN'],
                fs_thrust_vaccuum = rockets_data['first_stage']['thrust_vacuum']['kN'],
                ss_engines = rockets_data['second_stage']['engines'],
                ss_fuel_amount_tons = rockets_data['second_stage']['fuel_amount_tons'],
                ss_burn_time_sec = rockets_data['second_stage']['burn_time_sec'],
                ss_thrust = rockets_data['second_stage']['thrust']['kN'],
                ss_payloads = rockets_data['second_stage']['payloads']['option_1'],
                engines_number = rockets_data['engines']['number'],
                engines_type = rockets_data['engines']['type'],
                engines_fuel_1 = rockets_data['engines']['propellant_1'],
                engines_fuel_2 = rockets_data['engines']['propellant_2'],
                landing_legs_number = rockets_data['landing_legs']['number'],
                landing_legs_material = rockets_data['landing_legs']['material'],
                payload_weights = rockets_data['payload_weights'],
                images = rockets_data['flickr_images'],
                name = name,
                type = rockets_data['type'],
                active = rockets_data['active'],
                stages = rockets_data['stages'],
                boosters = rockets_data['boosters'],
                cost_per_launch = rockets_data['cost_per_launch'],
                success_rate_pct = rockets_data['success_rate_pct'],
                first_flight = rockets_data['first_flight'],
                country = rockets_data['country'],
                company = rockets_data['company'],
                wikipedia = rockets_data['wikipedia'],
                description = rockets_data['description']
            )

            # Create a QListWidgetItem with rocket information
            item = QListWidgetItem(f'{name}')
            item.setData(Qt.ItemDataRole.UserRole, rocket)
            self.rockets_list_widget.addItem(item)
        
        return rockets

    def show_rockets_details(self, item):
        # Retrieve the rocket from the selected item
        rocket = item.data(Qt.ItemDataRole.UserRole)

        # Check if the details window already exists
        if rocket in self.details_windows:
            details_window = self.details_windows[rocket]
            details_window.show()
        else:
            # Create and show the rocketDetailsWindow with the rocket details
            details_window = RocketDetailsWindow(rocket)
            self.details_windows[rocket] = details_window
            details_window.show()

    def download_json(self, rockets):
        # Convert the rocket data to JSON format
        json_data = self.rocket_to_json(rockets)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, 'rockets_detailed_data.json')

        # Save the JSON data to a file
        with open(filename, "w") as json_file:
            json_file.write(json_data)
        
        # Show confirmation dialog with file path
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Download Completed")
        message_box.setText(f"JSON file has been downloaded to:\n{filename}")
        message_box.exec()

    def rocket_to_json(self, rockets):
        # Convert the dictionary to JSON format
        json_data = json.dumps(rockets, indent=2)

        return json_data


class RocketDetailsWindow(QMainWindow):
    def __init__(self, rocket):
        super().__init__()
        self.setWindowTitle('Rocket Details')

        # Create labels to display rocket details
        self.layout = QVBoxLayout()
        self.label_height = QLabel(f'Height: {rocket.height}')
        self.label_diameter = QLabel(f'Diameter: {rocket.diameter}')
        self.label_mass_kg = QLabel(f'Mass (kg): {rocket.mass_kg}')
        self.label_fs_engines = QLabel(f'First Stage Engines: {rocket.fs_engines}')
        self.label_fs_fuel_amount_tons = QLabel(f'First Stage Fuel Amount (tons): {rocket.fs_fuel_amount_tons}')
        self.label_fs_burn_time_sec = QLabel(f'First Stage Burn Time (sec): {rocket.fs_burn_time_sec}')
        self.label_fs_thrust_sea_level = QLabel(f'First Stage Thrust Sea Level: {rocket.fs_thrust_sea_level}')
        self.label_fs_thrust_vacuum = QLabel(f'First Stage Thrust Vacuum: {rocket.fs_thrust_vacuum}')
        self.label_ss_engines = QLabel(f'Second Stage Engines: {rocket.ss_engines}')
        self.label_ss_fuel_amount_tons = QLabel(f'Second Stage Fuel Amount (tons): {rocket.ss_fuel_amount_tons}')
        self.label_ss_burn_time_sec = QLabel(f'Second Stage Burn Time (sec): {rocket.ss_burn_time_sec}')
        self.label_ss_thrust = QLabel(f'Second Stage Thrust: {rocket.ss_thrust}')
        self.label_ss_payloads = QLabel(f'Second Stage Payloads: {rocket.ss_payloads}')
        self.label_engines_type = QLabel(f'Engines Type: {rocket.engines_type}')
        self.label_engines_number = QLabel(f'Engines Number: {rocket.engines_number}')
        self.label_engines_fuel_1 = QLabel(f'Engines Fuel 1: {rocket.engines_fuel_1}')
        self.label_engines_fuel_2 = QLabel(f'Engines Fuel 2: {rocket.engines_fuel_2}')
        self.label_landing_legs_number = QLabel(f'Landing Legs Number: {rocket.landing_legs_number}')
        self.label_landing_legs_material = QLabel(f'Landing Legs Material: {rocket.landing_legs_material}')
        self.label_payload_weights = QLabel(f'Payload Weights: {rocket.payload_weights}')
        self.label_name = QLabel(f'Names: {rocket.name}')
        self.label_type = QLabel(f'Type: {rocket.type}')
        self.label_active = QLabel(f'Active: {rocket.active}')
        self.label_stages = QLabel(f'Stages: {rocket.stages}')
        self.label_boosters = QLabel(f'Boosters: {rocket.boosters}')
        self.label_cost_per_launch = QLabel(f'Cost Per Launch: {rocket.cost_per_launch}')
        self.label_success_rate_pct = QLabel(f'Success Rate (%): {rocket.success_rate_pct}')
        self.label_first_flight = QLabel(f'First Flight: {rocket.first_flight}')
        self.label_country = QLabel(f'Country: {rocket.country}')
        self.label_company = QLabel(f'Company: {rocket.company}')
        self.label_wikipedia = QLabel(f'Wikipedia: <a href="{rocket.wikipedia}" target="_blank">{rocket.wikipedia}</a>')
        self.label_images = QLabel(f'Image gallery:')
        self.label_description = QLabel(f'Description: {rocket.description}')

        # Create a QHBoxLayout to hold the image labels
        self.image_layout = QHBoxLayout()

        # Check if there are images to display
        if not rocket.images:
            # No images available, display the "No image available" text
            no_image_label = QLabel("No image(s) available")
            self.image_layout.addWidget(no_image_label)
        else:
            # Get images from rocket images URLs
            for image_url in rocket.images:
                image = self.get_image_from_url(image_url)
                if image:
                    # Create a QLabel for each image and add it to the image layout
                    image_label = QLabel()
                    image_label.setPixmap(image.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                    self.image_layout.addWidget(image_label)

        # Make links clickeable
        self.habilitate_external_links()

        # Add a button to download rocket's data in JSON
        self.download_button = QPushButton(f'Download {rocket.name}\'s data')
        self.download_button.clicked.connect(lambda: self.download_json(rocket))

        # Allow overflow with newlines
        self.label_description.setWordWrap(True)

        # Add the labels to the layout
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.label_type)
        self.layout.addWidget(self.label_active)
        self.layout.addWidget(self.label_stages)
        self.layout.addWidget(self.label_boosters)
        self.layout.addWidget(self.label_cost_per_launch)
        self.layout.addWidget(self.label_success_rate_pct)
        self.layout.addWidget(self.label_first_flight)
        self.layout.addWidget(self.label_country)
        self.layout.addWidget(self.label_company)
        self.layout.addWidget(self.label_height)
        self.layout.addWidget(self.label_diameter)
        self.layout.addWidget(self.label_mass_kg)
        self.layout.addWidget(self.label_fs_engines)
        self.layout.addWidget(self.label_fs_fuel_amount_tons)
        self.layout.addWidget(self.label_fs_burn_time_sec)
        self.layout.addWidget(self.label_fs_thrust_sea_level)
        self.layout.addWidget(self.label_fs_thrust_vacuum)
        self.layout.addWidget(self.label_ss_engines)
        self.layout.addWidget(self.label_ss_fuel_amount_tons)
        self.layout.addWidget(self.label_ss_burn_time_sec)
        self.layout.addWidget(self.label_ss_thrust)
        self.layout.addWidget(self.label_ss_payloads)
        self.layout.addWidget(self.label_engines_type)
        self.layout.addWidget(self.label_engines_number)
        self.layout.addWidget(self.label_engines_fuel_1)
        self.layout.addWidget(self.label_engines_fuel_2)
        self.layout.addWidget(self.label_landing_legs_number)
        self.layout.addWidget(self.label_landing_legs_material)
        self.layout.addWidget(self.label_payload_weights)
        self.layout.addWidget(self.label_wikipedia)
        self.layout.addLayout(self.image_layout) # Add the labels to the QVBoxLayout
        self.layout.addWidget(self.label_description)

        # Add the download button to the layout
        self.layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Show the window maximized
        self.showMaximized()

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
    
    def download_json(self, rocket):
        # Create a dictionary with rocket data       
        rocket_data = {
            'height': rocket.height,
            'diameter': rocket.diameter,
            'mass_kg': rocket.mass_kg,
            'fs_engines': rocket.fs_engines,
            'fs_fuel_amount_tons': rocket.fs_fuel_amount_tons,
            'fs_burn_time_sec': rocket.fs_burn_time_sec,
            'fs_thrust_sea_level': rocket.fs_thrust_sea_level,
            'fs_thrust_vaccuum': rocket.fs_thrust_vacuum,
            'ss_engines': rocket.ss_engines,
            'ss_fuel_amount_tons': rocket.ss_fuel_amount_tons,
            'ss_burn_time_sec': rocket.ss_burn_time_sec,
            'ss_thrust': rocket.ss_thrust,
            'ss_payloads': rocket.ss_payloads,
            'engines_type': rocket.engines_type,
            'engines_number': rocket.engines_number,
            'engines_fuel_1': rocket.engines_fuel_1,
            'engines_fuel_2': rocket.engines_fuel_2,
            'landing_legs_number': rocket.landing_legs_number,
            'landing_legs_material': rocket.landing_legs_material,
            'payload_weights': rocket.payload_weights,
            'images': rocket.images,
            'name': rocket.name,
            'type': rocket.type,
            'active': rocket.active,
            'stages': rocket.stages,
            'boosters': rocket.boosters,
            'cost_per_launch': rocket.cost_per_launch,
            'success_rate_pct': rocket.success_rate_pct,
            'first_flight': rocket.first_flight,
            'country': rocket.country,
            'company': rocket.company,
            'wikipedia': rocket.wikipedia,
            'description': rocket.description
        }
        # Convert the rocket data to JSON format
        json_data = json.dumps(rocket_data, indent=2)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, f'rocket_{rocket.name}_data.json')

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
    rocket_window = RocketsListWindow()
    rocket_window.show()
    sys.exit(app.exec())
