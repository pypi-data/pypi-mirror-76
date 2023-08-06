from .base import *
from pypolyline.util import decode_polyline


class Router(OneMap):
    def __init__(self, email =None, password = None, timeout = 30):
        super().__init__(email, password, timeout)
        self.supported_route_types = ['walk', 'drive', 'cycle', 'pt']
        self.supported_pt_modes = ['TRANSIT', 'BUS', 'RAIL']

    def route(self, start_point: Tuple[float, float], end_point: Tuple[float, float], route_type: str,
              date: str = None, time: str = None,
              mode: str = None, max_walk_distance: int = None, num_itineraries: int = None,
              endpoint = "/privateapi/routingsvc/route"):
        """

        :param start_point: (lat,lng)
        :param end_point: (lat, lng)
        :param route_type: One of self.supported_route_types

        Only use these if route_type == 'pt'
        :param date: "YYYY-mm-dd"
        :param time: "HH:MM:SS"
        :param mode: One of self.supported_pt_modes
        :param max_walk_distance: (Optional) Max distance (in meters) of walking
        :param num_itineraries: (Optional) 1 - 3, limits the number of results returned

        :return: dictionary of API response
        """
        if route_type not in self.supported_route_types:
            raise ValueError(f"Route type `{route_type}` not supported\n Supported: {self.supported_route_types}")

        self.check_auth_and_authenticate()

        payload = {"token": self.token,
                   "start": f"{start_point[0]},{start_point[1]}",
                   "end": f"{end_point[0]},{end_point[1]}",
                   "routeType": route_type
                   }

        if route_type == 'pt':
            if any([i is None for i in [date, time, mode]]):
                raise ValueError("You must provide `date`, `time`, and `mode` if `route_type` is `pt`")
            payload['date'] = date
            payload['time'] = time
            payload['mode'] = mode

            if max_walk_distance is not None:
                payload['maxWalkDistance'] = max_walk_distance
            if num_itineraries is not None:
                payload['numItineraries'] = num_itineraries

        response = requests.get(url = f"{self.url}{endpoint}",
                                params = payload,
                                timeout = self.timeout)
        print(response.url)

        return self.parse_response(response)

    @staticmethod
    def decode_route_geometry(polyline):
        # Convenience wrapper for decoding route geometry
        return decode_polyline(polyline.encode("utf-8"), 5)

    def route_from_postal(self, start_postal: str, end_postal: str, route_type: str,
              date: str = None, time: str = None,
              mode: str = None, max_walk_distance: int = None, num_itineraries: int = None):
        self.check_auth_and_authenticate()

        if len(start_postal) + len(end_postal) != 12:
            raise ValueError("Please provide valid postal codes, which contain 6 digits each")

        try:
            start_point = (self.search(start_postal)['results'][0]['LATITUDE'],
                           self.search(start_postal)['results'][0]['LONGITUDE'])
        except IndexError:  # out of bounds means empty results list returned
            raise ValueError(f"Please check your starting postal code, {start_postal} did not return any results")

        try:
            end_point = (self.search(end_postal)['results'][0]['LATITUDE'],
                         self.search(start_postal)['results'][0]['LONGITUDE'])
        except IndexError:
            raise ValueError(f"Please check your destination postal code, {end_postal} did not return any results")

        return self.route(start_point, end_point, route_type, date, time, mode,
                          max_walk_distance, num_itineraries)
