class Launch:
    def __init__(
        self, flight_number, mission_name, launch_year, launch_date, rocket_name, rocket_type, land_success, landing_intent, landing_type, landing_vehicle,
        customers, nationality, manufacturer, payload_type, payload_kg, orbit, orbit_reference_sys, orbit_regime, recovery_attempt, recovered, ships, flight_club,
        launch_site_name, launch_site_full_name, launch_success, mission_patch, reddit_campaign, article_link, wikipedia, video_link, images, details
    ):
        self.flight_number = flight_number
        self.mission_name = mission_name
        self.launch_year = launch_year
        self.launch_date = launch_date
        self.rocket_name = rocket_name
        self.rocket_type = rocket_type
        self.land_success = land_success
        self.landing_intent = landing_intent
        self.landing_type = landing_type
        self.landing_vehicle = landing_vehicle
        self.customers = customers
        self.nationality = nationality
        self.manufacturer = manufacturer
        self.payload_type = payload_type
        self.payload_kg = payload_kg
        self.orbit = orbit
        self.orbit_reference_sys = orbit_reference_sys
        self.orbit_regime = orbit_regime
        self.recovery_attempt = recovery_attempt
        self.recovered = recovered
        self.ships = ships
        self.flight_club = flight_club
        self.launch_site_name = launch_site_name
        self.launch_site_full_name = launch_site_full_name
        self.launch_success = launch_success
        self.mission_patch = mission_patch
        self.reddit_campaign = reddit_campaign
        self.article_link = article_link
        self.wikipedia = wikipedia
        self.video_link = video_link
        self.images = images
        self.details = details
