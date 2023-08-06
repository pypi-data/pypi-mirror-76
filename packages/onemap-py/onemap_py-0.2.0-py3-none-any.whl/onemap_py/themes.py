from .base import *


class Themes(OneMap):
    def __init__(self):
        super().__init__()

    def get_theme_info(self, theme_name: str,
                       endpoint: str = "/privateapi/themesvc/getThemeInfo"):
        self.check_auth_and_authenticate()

        response = requests.get(url=f"{self.url}{endpoint}",
                                params={"token": self.token, "queryName": theme_name})

        response = self.parse_response(response)

        return response

    def get_all_themes_info(self, more_info = "Y", theme_endpoint: str = "/privateapi/themesvc/getAllThemesInfo"):

        self.check_auth_and_authenticate()

        response = requests.get(url=f"{self.url}{theme_endpoint}",
                                params={"token": self.token, "moreInfo": more_info})

        response = self.parse_response(response)

        return response

    def retrieve_theme(self, theme: str, bbox: Tuple[Tuple[float, float], Tuple[float, float]] = None,
                       endpoint="/privateapi/themesvc/retrieveTheme"):
        """
        Return all instances of a given theme (e.g. kindergartens) within the bounding box provided
        by `bbox` parameter.
        :param theme: One of the acceptable `QueryName`s as returned from get_themes()
        :param bbox: (Optional) Bounding box vertices ((lat,lng), (lat,lng)) to filter results
        :param endpoint: Parameterized in case endpoint changes
        :return: Dictionary form of json response from API
        """
        self.check_auth_and_authenticate()
        payload = {"token": self.token,
                   "queryName": theme
                   }
        if bbox is not None:
            payload['extents'] = "{:.5f},{:.5f},{:.5f},{:.5f}".format(bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])

        response = requests.get(url=f"{self.url}{endpoint}",
                                params=payload,
                                timeout=self.timeout)

        response = self.parse_response(response)

        try:
            out = response['SrchResults'] # Just return results
            return out[0], out[1:] # first one is metadata, 2nd one is results
        except KeyError:
            return response

    def get_list_of_available_themes(self):
        themes = self.get_all_themes_info()
        themes = themes['Theme_Names']

        queries = [i['QUERYNAME'] for i in themes]

        return queries
