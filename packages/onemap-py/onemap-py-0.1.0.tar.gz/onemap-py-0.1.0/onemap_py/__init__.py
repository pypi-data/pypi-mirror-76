from .base import OneMap
from .themes import Themes
from .planning_areas import PlanningAreas
from .population import Population
from .routing import Router


class Client(OneMap):
    def __init__(self, email = None, password = None, timeout = 10):
        super().__init__(email, password, timeout)
        self.Themes = Themes()
        self.PlanningAreas = PlanningAreas()
        self.Router = Router()
        self.Population = Population()

    def authenticate(self):
        self.check_auth_and_authenticate()
        for module in [self.Themes, self.PlanningAreas, self.Router, self.Population]:
            # Update authenticated status
            module.token = self.token
            module.authenticated = self.authenticated
