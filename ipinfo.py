# !/usr/bin/env python3
from typing import Union

import requests

from main import is_ip


class IPInfo:
    def __init__(self,
                 ip="?",
                 city="?",
                 country_code="?",
                 as_number="?",
                 company="?"):
        self.city = city
        self.country_code = country_code
        self.as_number = as_number
        self.company = company
        self.ip = ip

    @staticmethod
    def from_ip_info_answer(ip_info_answer: dict):
        city = ip_info_answer["city"]
        country_code = ip_info_answer["country"]
        if "org" in ip_info_answer and ip_info_answer["org"]:
            as_number, company = \
                ip_info_answer["org"].split(' ', maxsplit=1)
        else:
            as_number = company = "unknown"
        ip = ip_info_answer["ip"]
        return IPInfo(ip, city, country_code, as_number, company)

    @staticmethod
    def from_ip(ip: str):
        return IPInfo.from_ip_info_answer(get_info(ip))


def get_info(host: str) -> Union[dict, type(None)]:
    if not is_ip(host):
        return None
    response = requests.get('http://ipinfo.io/' + host + '/json')
    response.raise_for_status()
    return response.json()
