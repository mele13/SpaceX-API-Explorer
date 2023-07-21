class Event:
    def __init__(self, id, title, event_date, flight_number, details, reddit, article, wikipedia):
        self.id = id
        self.title = title
        self.event_date = event_date
        self.flight_number = flight_number
        self.wikipedia = wikipedia
        self.article = article
        self.reddit = reddit
        self.details = details