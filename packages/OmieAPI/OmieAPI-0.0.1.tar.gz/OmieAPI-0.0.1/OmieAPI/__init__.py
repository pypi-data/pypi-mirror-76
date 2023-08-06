import json

import requests


class ApiOmie:
    def __init__(self, app_key, app_secret):
        self.APP_KEY = app_key
        self.APP_SECRET = app_secret

    def request(self, url, call, params=None):
        if params is None:
            params = {}
        data = {
            'app_key': self.APP_KEY,
            'app_secret': self.APP_SECRET,
            'call': call,
            'param': [params]
        }

        header = {
            'Content-type': "application/json"
        }

        r = requests.post(
            url=url,
            data=json.dumps(data),
            headers=header
        )

        return r

    def calc_retencao(self, j: json):
        total = 0
        if "retem_ir" in j:
            if j["retem_ir"] == "S":
                total += j["valor_ir"]
        if "retem_cofins" in j:
            if j["retem_cofins"] == "S":
                total += j["valor_cofins"]
        if "retem_inss" in j:
            if j["retem_inss"] == "S":
                total += j["valor_inss"]
        if "retem_csll" in j:
            if j["retem_csll"] == "S":
                total += j["valor_csll"]
        if "retem_iss" in j:
            if j["retem_iss"] == "S":
                total += j["valor_iss"]
        if "retem_pis" in j:
            if j["retem_pis"] == "S":
                total += j["valor_pis"]
        return total
