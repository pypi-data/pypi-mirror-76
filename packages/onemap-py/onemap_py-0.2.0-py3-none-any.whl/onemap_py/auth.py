import requests
import json
import logging


def authenticate(email: str = None, password: str = None, keep_token=True,
                 auth_url: str = "https://developers.onemap.sg/privateapi/auth/post/getToken",
                 logger: logging.Logger = None):

    if email is None or password is None:
        if logger is not None:
            logger.exception("Please provide both email and password")
        else:
            raise ValueError("Please provide both email and password")

    response = requests.post(url=auth_url,
                             json={"email": email,
                                   "password": password})

    if response.status_code == 200 and keep_token:
        # Store response text in local json
        json.dump(obj=json.loads(response.text),
                  fp=open("token.json", "w"))

    return response
