from .base import *


class PlanningAreas(OneMap):
    def __init__(self, om: OneMap = None):
        super().__init__()
        if om is not None:
            self.logger = om.logger
            self.token = om.token
            self.authenticated = om.authenticated
            self.url = om.url

    def get_all_planning_areas(self, year: int = 2014, names_only: bool = False,
                          endpoint = "/privateapi/popapi/getAllPlanningarea"):
        """

        :param year: Year to retrieve the data for (1998, 2008, 2014)
        :param names_only: Whether to return planning area names only, or whole polygons
        :param endpoint: Parameterized in case SLA updates the OneMap API
        :return: Dictionary converted from the response JSON
        """
        if names_only:
            endpoint = "/privateapi/popapi/getPlanningareaNames"

        self.check_auth_and_authenticate()

        response = requests.get(url=f"{self.url}{endpoint}",
                                params={"token": self.token, "year": year},
                                timeout=self.timeout)

        response = self.parse_response(response)

        return response

    def find_planning_area(self, lat: float, lng: float, year: int = 2014,
                          endpoint = "/privateapi/popapi/getPlanningarea"):

        self.check_auth_and_authenticate()

        response = requests.get(url=f"{self.url}{endpoint}",
                                params={"token": self.token,
                                        "lat": lat,
                                        "lng": lng,
                                        "year": year},
                                timeout=self.timeout)
        self.logger.debug(response.url)

        response = self.parse_response(response)

        return response