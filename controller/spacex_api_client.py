'''
Interaction with the SpaceX API to fetch data related to launch pads, capsules, cores, dragons, missions, etc.
'''
import requests

# Base URL for SpaceX API
base_url = "https://api.spacexdata.com"

# Dictionary of API endpoints
endpoints = {
    "capsules": "/capsules",
    "cores": "/cores",
    "dragons": "/dragons",
    "history": "/history",
    "company_info": "/info",
    "landpads": "/landpads",
    "launches": "/launches",
    "launchpads": "/launchpads",
    "missions": "/missions",
    "payloads": "/payloads",
    "rockets": "/rockets",
    "roadster": "/roadster",
    "ships": "/ships"
}

class SpaceXAPIClient:
    def __init__(self):
        self.base_url = base_url

    def make_request_from_all_endpoints(self, endpoint):
        url = f'{self.base_url}{endpoint}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to get data from {endpoint}. Response code: {response.status_code}')
            return [] # Return empty list on failure
        
    def make_api_request(self, endpoint_version, endpoint_name):
        url = f'{self.base_url}{endpoint_version}/{endpoint_name}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to get {endpoint_name} data. Response code: {response.status_code}')
            return []  # Return empty list on failure
        
    def get_launchpads(self):
        return self.make_api_request("/v4", "launchpads")

    def get_launches(self):
        return self.make_api_request("/v3", "launches")

    def get_missions(self):
        return self.make_api_request("/v3", "missions")

    def get_history(self):
        return self.make_api_request("/v3", "history")

    def get_dragons(self):
        return self.make_api_request("/v4", "dragons")

    def get_rockets(self):
        return self.make_api_request("/v4", "rockets")

if __name__ == '__main__':
    client = SpaceXAPIClient()
    # for endpoint, path in endpoints.items():
    #     data = client.make_request_from_all_endpoints(path)
    #     print(f'Datos de {endpoint}:')
    #     print(data)
    #     print()
    launchpads_data = client.get_missions()
    print("============================================================")
    print("=========================== Data ===========================")
    print("============================================================")
    print(launchpads_data)
    