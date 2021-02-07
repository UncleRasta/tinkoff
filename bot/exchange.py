from openapi_client import openapi
import os

class Tinkoff:
    def __init__(self, access_token: str = None):
        self._access_token = access_token if access_token else os.environ["TINK_TOKEN"]
        self._client = openapi.api_client(self._access_token)

    def get_portfolio(self):
        try:
            pf = self._client.portfolio.portfolio_get()
            name = pf.payload.positions[0].name
            price = pf.payload.positions[0].average_position_price
            income = pf.payload.positions[0].expected_yield
            return name, price, income
        except Exception as err:
            return err
    