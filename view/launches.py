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
from launch import Launch

downloads_path = "./resources/downloads/launches/"

class LaunchesListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Launches Details')

        self.spacex_api_client = SpaceXAPIClient()

        # Create a widget to display the list of launchpads
        self.launchpad_list_widget = QListWidget()

        # Initialize the details windows dictionary
        self.details_windows = {}

        # Load launchpads information from api
        launches = self.load_launches()

        # Add a button to download launchpads data in JSON
        self.download_button = QPushButton("Download detailed data")
        self.download_button.clicked.connect(lambda: self.download_json(launches))

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.launchpad_list_widget)
        main_layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Show information of the clicked launchpad
        self.launchpad_list_widget.itemClicked.connect(self.show_launches_details)
        
    def load_launches(self):
        launches = self.spacex_api_client.get_launches()

        # Get launches information from the obtained data
        for launches_data in launches:

            mission_name = launches_data['mission_name']
            flight_number = launches_data['flight_number']

            if 'rocket' in launches_data and launches_data['rocket'] is not None and 'fairings' in launches_data['rocket'] and launches_data['rocket']['fairings'] is not None and 'recovery_attempt' in launches_data['rocket']['fairings']:
                recovery_attempt = launches_data['rocket']['fairings']['recovery_attempt']
            else:
                recovery_attempt = "No data available for recovery attempts"

            if 'rocket' in launches_data and launches_data['rocket'] is not None and 'fairings' in launches_data['rocket'] and launches_data['rocket']['fairings'] is not None and 'recovered' in launches_data['rocket']['fairings']:
                recovered = launches_data['rocket']['fairings']['recovered']
            else:
                recovered = "No data available"

            launch = Launch(
                flight_number = launches_data['flight_number'],
                mission_name = launches_data['mission_name'],
                launch_year = launches_data['launch_year'],
                launch_date = launches_data['launch_date_utc'],
                rocket_name = launches_data['rocket']['rocket_name'],
                rocket_type = launches_data['rocket']['rocket_type'],
                land_success = launches_data['rocket']['first_stage']['cores'][0]['land_success'],
                landing_intent = launches_data['rocket']['first_stage']['cores'][0]['landing_intent'],
                landing_type = launches_data['rocket']['first_stage']['cores'][0]['landing_type'],
                landing_vehicle = launches_data['rocket']['first_stage']['cores'][0]['landing_vehicle'],
                customers = launches_data['rocket']['second_stage']['payloads'][0]['customers'],
                nationality = launches_data['rocket']['second_stage']['payloads'][0]['nationality'],
                manufacturer = launches_data['rocket']['second_stage']['payloads'][0]['manufacturer'],
                payload_type = launches_data['rocket']['second_stage']['payloads'][0]['payload_type'],
                payload_kg = launches_data['rocket']['second_stage']['payloads'][0]['payload_mass_kg'],
                orbit = launches_data['rocket']['second_stage']['payloads'][0]['orbit'],
                orbit_reference_sys = launches_data['rocket']['second_stage']['payloads'][0]['orbit_params']['reference_system'],
                orbit_regime = launches_data['rocket']['second_stage']['payloads'][0]['orbit_params']['regime'],
                recovery_attempt = recovery_attempt,
                recovered = recovered,
                ships = launches_data['ships'],
                flight_club = launches_data['telemetry']['flight_club'],
                launch_site_name = launches_data['launch_site']['site_name'],
                launch_site_full_name = launches_data['launch_site']['site_name_long'],
                launch_success = launches_data['launch_success'],
                mission_patch = launches_data['links']['mission_patch'],
                reddit_campaign = launches_data['links']['reddit_campaign'],
                article_link = launches_data['links']['article_link'],
                wikipedia = launches_data['links']['wikipedia'],
                video_link = launches_data['links']['video_link'],
                images = launches_data['links']['flickr_images'],
                details = launches_data['details'],
            )

            # Create a QListWidgetItem with launch information
            item = QListWidgetItem(f'{flight_number} - {mission_name}')
            item.setData(Qt.ItemDataRole.UserRole, launch)
            self.launchpad_list_widget.addItem(item)
        
        return launches

    def show_launches_details(self, item):
        # Retrieve the launch from the selected item
        launch = item.data(Qt.ItemDataRole.UserRole)

        # Check if the details window already exists
        if launch in self.details_windows:
            details_window = self.details_windows[launch]
            details_window.show()
        else:
            # Create and show the LaunchDetailsWindow with the launch details
            details_window = LaunchDetailsWindow(launch)
            self.details_windows[launch] = details_window
            details_window.show()

    def download_json(self, launches):
        # Convert the launch data to JSON format
        json_data = self.launch_to_json(launches)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, 'launches_detailed_data.json')

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


class LaunchDetailsWindow(QMainWindow):
    def __init__(self, launch):
        super().__init__()
        self.setWindowTitle('Launch Details')

        # Create labels to display launch details
        self.layout = QVBoxLayout()
        self.label_mission_patch = QLabel()
        self.label_flight_number = QLabel(f'Flight Number: {launch.flight_number}')
        self.label_mission_name = QLabel(f'Mission Name: {launch.mission_name}')
        self.label_launch_site_name = QLabel(f'Launch Site Name: {launch.launch_site_name}')
        self.label_launch_site_full_name = QLabel(f'Launch Site Full Name: {launch.launch_site_full_name}')
        self.label_launch_success = QLabel(f'Launch Success: {launch.launch_success}')
        self.label_launch_year = QLabel(f'Launch Year: {launch.launch_year}')
        self.label_launch_date = QLabel(f'Launch Date: {launch.launch_date}')
        self.label_rocket_name = QLabel(f'Rocket Name: {launch.rocket_name}')
        self.label_rocket_type = QLabel(f'Rocket Type: {launch.rocket_type}')
        self.label_landing_intent = QLabel(f'Landing Intent: {launch.landing_intent}')
        self.label_land_success = QLabel(f'Land Success: {launch.land_success}')
        self.label_landing_type = QLabel(f'Landing Type: {launch.landing_type}')
        self.label_landing_vehicle = QLabel(f'Landing Vehicle: {launch.landing_vehicle}')
        self.label_customers = QLabel(f'Customers: {self.get_separated_data(launch.customers)}')
        self.label_nationality = QLabel(f'Nationality: {launch.nationality}')
        self.label_manufacturer = QLabel(f'Manufacturer: {launch.manufacturer}')
        self.label_payload_type = QLabel(f'Payload Type: {launch.payload_type}')
        self.label_payload_kg = QLabel(f'Payload Mass (kg): {launch.payload_kg}')
        self.label_orbit = QLabel(f'Orbit: {launch.orbit}')
        self.label_orbit_reference_sys = QLabel(f'Orbit Reference System: {launch.orbit_reference_sys}')
        self.label_orbit_regime = QLabel(f'Orbit Regime: {launch.orbit_regime}')
        self.label_recovery_attempt = QLabel(f'Recovery Attempt: {launch.recovery_attempt}')
        self.label_recovered = QLabel(f'Recovered: {launch.recovered}')
        self.label_ships = QLabel(f'Ships: {self.get_separated_data(launch.ships)}')
        self.label_flight_club = QLabel(f'Flight Club: <a href="{launch.flight_club}" target="_blank">{launch.flight_club}</a>')
        self.label_reddit_campaign = QLabel(f'Reddit Campaign: <a href="{launch.reddit_campaign}" target="_blank">{launch.reddit_campaign}</a>')
        self.label_article_link = QLabel(f'Article Link: <a href="{launch.article_link}" target="_blank">{launch.article_link}</a>')
        self.label_wikipedia = QLabel(f'Wikipedia: <a href="{launch.wikipedia}" target="_blank">{launch.wikipedia}</a>')
        self.label_video_link = QLabel(f'Video Link: <a href="{launch.video_link}" target="_blank">{launch.video_link}</a>')
        self.label_images = QLabel(f'Image gallery:')
        self.label_details = QLabel(f'Details: {launch.details}')

        # Create a QHBoxLayout to hold the image labels
        self.image_layout = QHBoxLayout()

        # Check if there are images to display
        if not launch.images:
            # No images available, display the "No image available" text
            no_image_label = QLabel("No image(s) available")
            self.image_layout.addWidget(no_image_label)
        else:
            # Get images from launch images URLs
            for image_url in launch.images:
                image = self.get_image_from_url(image_url)
                if image:
                    # Create a QLabel for each image and add it to the image layout
                    image_label = QLabel()
                    image_label.setPixmap(image.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                    self.image_layout.addWidget(image_label)

        # Make links clickeable
        self.habilitate_external_links()

        # Add a button to download launchpad's data in JSON
        self.download_button = QPushButton(f'Download {launch.flight_number} - {launch.mission_name}\'s data')
        self.download_button.clicked.connect(lambda: self.download_json(launch))

        # Allow overflow with newlines
        self.label_details.setWordWrap(True)

        # Get image from launch mission patch
        image = self.get_image_from_url(launch.mission_patch)        
        if image:
            # Scale the image to fit the label and display it
            self.label_mission_patch.setPixmap(image.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.label_mission_patch.setText("Image not available")

        # Add the labels to the layout
        self.layout.addWidget(self.label_mission_patch)
        self.layout.addWidget(self.label_flight_number)
        self.layout.addWidget(self.label_mission_name)
        self.layout.addWidget(self.label_launch_site_name)
        self.layout.addWidget(self.label_launch_site_full_name)
        self.layout.addWidget(self.label_launch_success)
        self.layout.addWidget(self.label_launch_year)
        self.layout.addWidget(self.label_launch_date)
        self.layout.addWidget(self.label_rocket_name)
        self.layout.addWidget(self.label_rocket_type)
        self.layout.addWidget(self.label_landing_intent)
        self.layout.addWidget(self.label_land_success)
        self.layout.addWidget(self.label_landing_type)
        self.layout.addWidget(self.label_landing_vehicle)
        self.layout.addWidget(self.label_customers)
        self.layout.addWidget(self.label_nationality)
        self.layout.addWidget(self.label_manufacturer)
        self.layout.addWidget(self.label_payload_type)
        self.layout.addWidget(self.label_payload_kg)
        self.layout.addWidget(self.label_orbit)
        self.layout.addWidget(self.label_orbit_reference_sys)
        self.layout.addWidget(self.label_orbit_regime)
        self.layout.addWidget(self.label_recovery_attempt)
        self.layout.addWidget(self.label_recovered)
        self.layout.addWidget(self.label_ships)
        self.layout.addWidget(self.label_flight_club)
        self.layout.addWidget(self.label_reddit_campaign)
        self.layout.addWidget(self.label_article_link)
        self.layout.addWidget(self.label_wikipedia)
        self.layout.addWidget(self.label_video_link)
        self.layout.addWidget(self.label_images)        
        self.layout.addLayout(self.image_layout) # Add the labels to the QVBoxLayout
        self.layout.addWidget(self.label_details)

        # Add the download button to the layout
        self.layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Show the window maximized
        self.showMaximized()

    def get_separated_data(self, data):
        return ', '.join(data)

    def habilitate_external_links(self):
        self.label_flight_club.setOpenExternalLinks(True)
        self.label_reddit_campaign.setOpenExternalLinks(True)
        self.label_article_link.setOpenExternalLinks(True)
        self.label_wikipedia.setOpenExternalLinks(True)
        self.label_video_link.setOpenExternalLinks(True)
    
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
    
    def download_json(self, launch):
        # Create a dictionary with launch data       
        launch_data = {
            'flight_number': launch.flight_number,
            'mission_name': launch.mission_name,
            'launch_year': launch.launch_year,
            'launch_date': launch.launch_date,
            'rocket_name': launch.rocket_name,
            'rocket_type': launch.rocket_type,
            'land_success': launch.land_success,
            'landing_intent': launch.landing_intent,
            'landing_type': launch.landing_type,
            'landing_vehicle': launch.landing_vehicle,
            'customers': launch.customers,
            'nationality': launch.nationality,
            'manufacturer': launch.manufacturer,
            'payload_type': launch.payload_type,
            'payload_kg': launch.payload_kg,
            'orbit': launch.orbit,
            'orbit_reference_sys': launch.orbit_reference_sys,
            'orbit_regime': launch.orbit_regime,
            'recovery_attempt': launch.recovery_attempt,
            'recovered': launch.recovered,
            'ships': launch.ships,
            'flight_club': launch.flight_club,
            'launch_site_name': launch.launch_site_name,
            'launch_site_full_name': launch.launch_site_full_name,
            'launch_success': launch.launch_success,
            'mission_patch': launch.mission_patch,
            'reddit_campaign': launch.reddit_campaign,
            'article_link': launch.article_link,
            'wikipedia': launch.wikipedia,
            'video_link': launch.video_link,
            'images': launch.images,
            'details': launch.details
        }
        # Convert the launch data to JSON format
        json_data = json.dumps(launch_data, indent=2)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, f'launchpad_{launch.flight_number}_{launch.mission_name}_data.json')

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
    launchpad_window = LaunchesListWindow()
    launchpad_window.show()
    sys.exit(app.exec())
