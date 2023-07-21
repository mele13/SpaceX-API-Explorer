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
from event import Event

downloads_path = "./resources/downloads/history/"

class HistoryListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('History Details')

        self.spacex_api_client = SpaceXAPIClient()

        # Create a widget to display the list of events
        self.history_list_widget = QListWidget()

        # Initialize the details windows dictionary
        self.details_windows = {}

        # Load history information from api
        history = self.load_history()

        # Add a button to download history data in JSON
        self.download_button = QPushButton("Download detailed data")
        self.download_button.clicked.connect(lambda: self.download_json(history))

        # Create a layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.history_list_widget)
        main_layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Show information of the clicked launchpad
        self.history_list_widget.itemClicked.connect(self.show_event_details)
        
    def load_history(self):
        history = self.spacex_api_client.get_history()

        # Get event information from the obtained data
        for event_data in history:
            title = event_data['title']
            event = Event(
                id = event_data['id'],
                title = title,
                event_date = event_data['event_date_utc'],
                flight_number = event_data['flight_number'],
                wikipedia = event_data['links']['wikipedia'],
                article = event_data['links']['article'],
                reddit = event_data['links']['reddit'],
                details = event_data['details'],
            )

            # Create a QListWidgetItem with event information
            item = QListWidgetItem(f'{title}')
            item.setData(Qt.ItemDataRole.UserRole, event)
            self.history_list_widget.addItem(item)

        return history

    def show_event_details(self, item):
        # Retrieve the event from the selected item
        event = item.data(Qt.ItemDataRole.UserRole)

        # Check if the details window already exists
        if event in self.details_windows:
            details_window = self.details_windows[event]
            details_window.show()
        else:
            # Create and show the EventDetailsWindow with the event details
            details_window = EventDetailsWindow(event)
            self.details_windows[event] = details_window
            details_window.show()

    def download_json(self, history):
        # Convert the event data to JSON format
        json_data = self.history_to_json(history)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, 'history_detailed_data.json')

        # Save the JSON data to a file
        with open(filename, "w") as json_file:
            json_file.write(json_data)
        
        # Show confirmation dialog with file path
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Download Completed")
        message_box.setText(f"JSON file has been downloaded to:\n{filename}")
        message_box.exec()

    def history_to_json(self, history):
        # Convert the dictionary to JSON format
        json_data = json.dumps(history, indent=2)

        return json_data


class EventDetailsWindow(QMainWindow):
    def __init__(self, event):
        super().__init__()
        self.setWindowTitle('Event Details')

        # Create labels to display event details
        self.layout = QVBoxLayout()
        self.label_title = QLabel(f'Event title: {event.title}')
        self.label_date = QLabel(f'Date: {event.event_date}')
        self.label_flight_number = QLabel(f'Flight number: {event.flight_number}')
        self.label_wikipedia = QLabel(f'Wikipedia: <a href="{event.wikipedia}" target="_blank">{event.wikipedia}</a>')
        self.label_article = QLabel(f'Article: <a href="{event.article}" target="_blank">{event.article}</a>')
        self.label_reddit = QLabel(f'Reddit: <a href="{event.reddit}" target="_blank">{event.reddit}</a>')
        self.label_details = QLabel(f'Details: {event.details}')

        # Add a button to download launchpad's data in JSON
        self.download_button = QPushButton(f'Download {event.title}\'s data')
        self.download_button.clicked.connect(lambda: self.download_json(event))

        # Allow overflow with newlines
        self.label_details.setWordWrap(True)

        # Add the labels to the layout
        self.layout.addWidget(self.label_title)
        self.layout.addWidget(self.label_date)
        self.layout.addWidget(self.label_flight_number)
        self.layout.addWidget(self.label_wikipedia)
        self.layout.addWidget(self.label_article)
        self.layout.addWidget(self.label_reddit)
        self.layout.addWidget(self.label_details)

        # Add the download button to the layout
        self.layout.addWidget(self.download_button)

        # Create a central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
    
    def download_json(self, event):
        # Create a dictionary with launchpad data
        event_data = {
            'id': event.id,
            'title': event.title,
            'event_date': event.event_date,
            'flight_number': event.flight_number,
            'wikipedia': event.wikipedia,
            'article': event.article,
            'reddit': event.reddit,
            'details': event.details,
        }

        # Convert the event data to JSON format
        json_data = json.dumps(event_data, indent=2)

        # Concatenate downloads_path with the filename
        filename = os.path.join(downloads_path, f'launchpad_{event.title}_data.json')

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
    launchpad_window = HistoryListWindow()
    launchpad_window.show()
    sys.exit(app.exec())
