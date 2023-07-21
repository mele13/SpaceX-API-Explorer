class Rocket:
    def __init__(
        self, height, diameter, mass_kg, fs_engines, fs_fuel_amount_tons, fs_burn_time_sec, fs_thrust_sea_level, fs_thrust_vaccuum, ss_engines, ss_fuel_amount_tons,
        ss_burn_time_sec, ss_thrust, ss_payloads, engines_type, engines_fuel_1, engines_fuel_2, landing_legs_number, landing_legs_material, payload_weights, images,
        name, type, active, stages, boosters, cost_per_launch, success_rate_pct, first_flight, country, company, wikipedia, description, engines_number
    ):
        self.height = height
        self.diameter = diameter
        self.mass_kg = mass_kg
        self.fs_engines = fs_engines
        self.fs_fuel_amount_tons = fs_fuel_amount_tons
        self.fs_burn_time_sec = fs_burn_time_sec
        self.fs_thrust_sea_level = fs_thrust_sea_level
        self.fs_thrust_vacuum = fs_thrust_vaccuum
        self.ss_engines = ss_engines
        self.ss_fuel_amount_tons = ss_fuel_amount_tons
        self.ss_burn_time_sec = ss_burn_time_sec
        self.ss_thrust = ss_thrust
        self.ss_payloads = ss_payloads
        self.engines_type = engines_type
        self.engines_number = engines_number
        self.engines_fuel_1 = engines_fuel_1
        self.engines_fuel_2 = engines_fuel_2
        self.landing_legs_number = landing_legs_number
        self.landing_legs_material = landing_legs_material
        self.payload_weights = payload_weights
        self.images = images
        self.name = name
        self.type = type
        self.active = active
        self.stages = stages
        self.boosters = boosters
        self.cost_per_launch = cost_per_launch
        self.success_rate_pct = success_rate_pct
        self.first_flight = first_flight
        self.country = country
        self.company = company
        self.wikipedia = wikipedia
        self.description = description
