class Dragon:
    def __init__(
        self, name, active, crew_capacity, orbit_duration_yr, dry_mass_kg, first_flight, heat_shield_material, heat_shield_dev, launch_payload_mass,
        return_payload_mass, launch_payload_vol, return_payload_vol, wikipedia, description, images, type, thrusters
    ):
        self.heat_shield_material = heat_shield_material
        self.heat_shield_dev = heat_shield_dev
        self.launch_payload_mass = launch_payload_mass
        self.return_payload_mass = return_payload_mass
        self.launch_payload_vol = launch_payload_vol
        self.return_payload_vol = return_payload_vol
        self.first_flight = first_flight
        self.name = name
        self.type = type
        self.active = active
        self.crew_capacity = crew_capacity
        self.orbit_duration_yr = orbit_duration_yr
        self.dry_mass_kg = dry_mass_kg
        self.thrusters = thrusters
        self.wikipedia = wikipedia
        self.description = description
        self.images = images
