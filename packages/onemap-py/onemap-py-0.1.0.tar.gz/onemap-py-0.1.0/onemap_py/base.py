import logging
import json
import requests
import getpass
from typing import Tuple


class OneMap(object):
    def __init__(self, email = None, password = None, timeout = 10):
        self.logger = logging.getLogger(__name__)
        self.token = None
        self.authenticated = False
        self.url = "https://developers.onemap.sg"
        self.email = email
        self.password = password
        self.timeout = timeout

    @staticmethod
    def parse_response(response):
        if response.status_code == 200:
            response = json.loads(response.text)
        else:
            response = f"{response.status_code} - {response.text}"

        return response

    def _authenticate(self, email: str = None, password: str = None,
                     auth_endpoint: str = "/privateapi/auth/post/getToken"):
        if email is None:
            # Check if self.email is also None
            if self.email is None:
                email = input("Email: ")
            else:
                email = self.email
        if password is None:
            if self.password is None:
                password = getpass.getpass("Password: ")
            else:
                password = self.password

        response = requests.post(url=f"{self.url}{auth_endpoint}",
                                 json={"email": email,
                                       "password": password})
        err_msg = "Failed to authenticate, please check credentials"
        if response.status_code == 200:
            try:
                self.token = json.loads(response.text)['access_token']
                self.logger.info("Successful authentication")
                self.authenticated = True
            except KeyError:
                self.logger.exception(err_msg)
                raise ValueError(err_msg)

        else:
            self.logger.exception(err_msg)
            raise ValueError(err_msg)

    def search(self, search_val: str = None,
               return_geometry:str = "Y", get_address_details:str = "Y",
               page_num: int = 1,
               search_endpoint='/commonapi/search'):
        """

        :param search_val: string to search for
        :param return_geometry: Y/N whether to return the geometry of each result
        :param get_address_details: Y/N whether to return the address details of each result
        :param search_endpoint: endpoint to hit for searching (parameterized in case OneMap changes it)
        :return:
        """

        payload = {"searchVal": search_val,
                   "returnGeom": return_geometry,
                   "getAddrDetails": get_address_details,
                   "pageNum": page_num}

        response = requests.get(url=f"{self.url}{search_endpoint}",
                                params=payload,
                                timeout = self.timeout)

        self.logger.debug(f"Search URL: {response.url}")
        self.logger.debug(f"Search Value: {search_val}")

        response = self.parse_response(response)

        return response

    def check_auth_and_authenticate(self):
        if not self.authenticated:
            self.logger.warning("Proceeding to authenticate")
            self._authenticate()

    def convert_coordinates(self, source: str, target: str,
                            x: float = None, y: float = None,
                            lat: float = None, lng: float = None,
                            endpoint = "/commonapi/convert/"):
        """
        Method to convert between coordinate reference systems (CRS)
        :param source: Source CRS, one of "WGS84", "SVY21", "EPSG3857"
        :param target: Target CRS, one of "WGS84", "SVY21", "EPSG3857"
        :param x: X coordinate if source CRS is SVY21 or EPSG3857
        :param y: Y coordinate if source CRS is SVY21 or EPSG3857
        :param lat: Latitude for source CRS WGS84
        :param lng: Longitude for source CRS WGS84
        :param endpoint: Parameterized for easy maintenance if OneMap API changes
        :return: Dictionary containing either X, Y or latitude, longitude depending on source/target CRS
        """
        supported_crs = {
            "WGS84": "4326",
            "SVY21": "3414",
            "EPSG3857": "3857"
        }

        requires_xy = ["SVY21", "EPSG3857"]
        requires_latlng = ['WGS84']

        if source not in supported_crs.keys() or target not in supported_crs.keys():
            self.logger.error(f"Coordinate reference {source}->{target} not supported")
            self.logger.info(f"Supported CRS: {list(supported_crs.keys())}")
        payload = {}
        if source in requires_xy:
            # Check if X and Y are provided
            if x is None or y is None:
                raise ValueError(f"x and y must both be provided if source is one of {requires_xy}")
            payload = {"X": x,
                       "Y": y}
        if source in requires_latlng:
            if lat is None or lng is None:
                raise ValueError(f"lat and lng must both be provided if source is one of {requires_latlng}")
            payload = {'latitude': lat,
                       'longitude': lng}
        final_endpoint = f"{endpoint}/{supported_crs[source]}to{supported_crs[target]}"

        response = requests.get(url = f"{self.url}{final_endpoint}",
                                params = payload,
                                timeout = self.timeout)

        response = self.parse_response(response)

        return response

    def reverse_geocode(self, radius: int = 10, xy: Tuple[float, float] = None,
                        latlng: Tuple[float, float] = None,
                        address_type: str = "All",
                        other_features: str = "Y",
                        endpoint = '/privateapi/commonsvc/revgeocode'):
        """
        Method to call API to return buildings and roads within `radius` meters of provided coordinates
        A Maximum of 500m buffer/radius applies for buildings and 20m buffer/radius for roads.
        The system will return a maximum of 10 nearest buildings.

        :param radius: buffer radius (in metres) to search from the provided coordinates
        :param xy: (X, Y) coordinates in SVY21 CRS
        :param latlng: (lat, lng) coordinates in WGS84 CRS
        :param address_type: "All" or "HDB". Selection of All or HDB properties within the buffer/radius.
        :param other_features: "Y" or "N". Allow retrieval of information on reservoirs, playgrounds, jetties etc.
        :param endpoint: Parameterized for easy maintenance if API endpoint changes
        :return: Dictionary response from API
        """

        self.check_auth_and_authenticate()

        # Use latlng as default
        if latlng is not None:
            payload = {
                "token": self.token,
                "location":f"{latlng[0]},{latlng[1]}",
                "buffer": radius,
                "addressType": address_type,
                "otherFeatures": other_features
            }
        elif xy is not None:
            payload = {
                "token": self.token,
                "location": f"{xy[0]},{xy[1]}",
                "buffer": radius,
                "addressType": address_type,
                "otherFeatures": other_features
            }
            endpoint = f"{endpoint}xy"
        else:
            raise ValueError("You must provide one of `latlng` or `xy`")

        response = requests.get(url = f"{self.url}{endpoint}",
                                params = payload,
                                timeout = self.timeout)

        response = self.parse_response(response)

        return response
