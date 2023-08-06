from .base import *


class Population(OneMap):

    def __init__(self, om: OneMap = None):
        if om is None:
            super().__init__()
        else:
            self.logger = om.logger
            self.token = om.token
            self.authenticated = om.authenticated
            self.url = om.url
        self.data_to_endpoint = {
            "economic": "/getEconomicStatus",
            "education": "/getEducationAttending",
            "ethnicity": "/getEthnicGroup",
            "household_income_from_work": "/getHouseholdMonthlyIncomeWork",
            "household_size": "/getHouseholdSize",
            "household_structure": "/getHouseholdStructure",
            "income_from_work": "/getIncomeFromWork",
            "industry": '/getIndustry',
            "language_literacy": "/getLanguageLiterate",
            "marital": "/getMaritalStatus",
            "mode_transport_school": "/getModeOfTransportSchool",
            "mode_transport_work": '/getModeOfTransportWork',
            "occupation": "/getOccupation",
            "age": "/getPopulationAgeGroup",
            "religion": "/getReligion",
            "spoken_language": "/getSpokenAtHome",
            "tenancy": "/getTenancy",
            "dwelling_type_household": "/getTypeOfDwellingHousehold",
            "dwelling_type_population": "/getTypeOfDwellingPop"
        }
        self.data_query_by_gender = ["economic","ethnicity", "marital"]
        self.available_data_types = list(self.data_to_endpoint.keys())

    def get_population_data(self,
                            data_type: str,
                            year: int,
                            planning_area: str,
                            endpoint="/privateapi/popapi"):
        """
        Function to query population data from the OneMap API.
        :param data_type: what type of data to query - check self.available_data_types for list of supported types
        :param year: Specify which year to return the results for
        :param planning_area: Specify the planning area
        :param endpoint: Parameterized in case SLA changes OneMap API
        :return:
        """
        if data_type not in self.data_to_endpoint.keys():
            self.logger.error(f"Unsupported `data_type` provided: {data_type}")
            self.logger.info(f"Supported data types: {self.data_to_endpoint.keys()}")
            return {"error": f"Unsupported `data_type` provided: {data_type}"}

        self.check_auth_and_authenticate()

        response = requests.get(url=f"{self.url}{endpoint}{self.data_to_endpoint[data_type]}",
                                params={"token": self.token,
                                        "year": year,
                                        "planningArea": planning_area})
        self.logger.debug(response.url)
        response = self.parse_response(response)

        return response

    def get_population_by_gender(self,
                                 data_type: str,
                                 year: int,
                                 planning_area: str,
                                 gender: str = None,
                                 endpoint="/privateapi/popapi"):

        if data_type not in self.data_to_endpoint.keys():
            self.logger.error(f"Unsupported `data_type` provided: {data_type}")
            self.logger.info(f"Supported data types: {self.data_to_endpoint.keys()}")
            return {"error": f"Unsupported `data_type` provided: {data_type}"}

        self.check_auth_and_authenticate()

        response = requests.get(url=f"{self.url}{endpoint}{self.data_to_endpoint[data_type]}",
                                params={"token": self.token,
                                        "year": year,
                                        "planningArea": planning_area,
                                        "gender": gender})
        self.logger.debug(response.url)
        response = self.parse_response(response)

        return response
