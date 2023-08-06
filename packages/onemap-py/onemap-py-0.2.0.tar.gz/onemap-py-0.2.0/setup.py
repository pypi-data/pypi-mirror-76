# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onemap_py']

package_data = \
{'': ['*']}

install_requires = \
['pypolyline>=0.2.4,<0.3.0']

setup_kwargs = {
    'name': 'onemap-py',
    'version': '0.2.0',
    'description': "Python wrapper for SLA's OneMap API",
    'long_description': 'Python Wrapper for SLA\'s OneMap API\n========================================\n\nIntroduction\n-------------\nThis package provides a simple way to query data using the OneMap API in Python.\n\nOneMap arranges its API endpoints by groups, and this package is organized to reflect that grouping.\n\nonemap-py allows you to make queries corresponding to the OneMap API, and returns the results to you in a standard\npython `dict`.\n\n## Sample Usage\n\n```python\nimport onemap_py\nx = onemap_py.Client("email@hostname.com", "password")\n\n# Search for an address\n# Note: For address search, no authentication required\ngh = x.search("GRAND HYATT")\ngh = gh[\'results\'][0] # Take the first result\n\n# For other queries, need to authenticate\nx.authenticate() # if email and password were None, interactive prompt\n\n# Get planning area for Grand Hyatt\nplanning_area = x.PlanningAreas.find_planning_area(gh[\'LATITUDE\'], gh[\'LONGITUDE\'])\nplanning_area = planning_area[\'pln_area_n\'] # Get the name\n\n# Get some population-related information for the planning area\navail_data = x.Population.available_data_types # find all available data types supported by the OneMap API\nx.Population.get_population_data("age", year = 2018, planning_area=planning_area)\n\n# Get route from Grand Hyatt to, say, Changi Airport Terminal 3\nx.Router.supported_route_types # [\'walk\', \'drive\', \'cycle\', \'pt\']\nchangi_airport = x.search("CHANGI AIRPORT TERMINAL 3")[\'results\'][0]\nx.Router.route_from_postal(gh[\'POSTAL\'], changi_airport[\'POSTAL\'], route_type=\'drive\')\n```\n\nDetails\n----------------\n> **Client**:\n>\n>   Main class that encapsulates all classes defined in other modules.\n        `Client` itself is a subclass of `OneMap`, but also has attributes `Router`, `PlanningAreas`, `Population`, and `Themes`.\n\n> **base.OneMap**\n> \n>    Provides basic functionality such as address search, coordinate conversion, and authentication.\n\n> **routing.Router**\n>\n>    Provides functionality to query routes between 2 points.\n>    Currently supports `(lat,lng)->(lat,lng)` or `postal->postal`\n\n> **planning_areas.PlanningAreas**\n>\n>   Provides functionality to retrieve planning areas, including geospatial boundaries.\n\n> **population.Population**\n>\n>    Handles all population-related queries, including education level, economic status, work income, marital status etc.\n>    Use `Population.available_data_types` to see available data types\n>   \n>    For a full list of data provided by OneMap, you can refer to their documentation.\n\n> **themes.Themes**\n>\n>    Thematic information from various agencies in Singapore.',
    'author': 'tauculator',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tauhlim/onemap-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
