from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum

if TYPE_CHECKING:
    from typing import List, Dict, Optional
    from bs4.element import Tag


@dataclass
class Symptoms:
    """
    Declaration of symptoms to be submitted together with DailyDeclaration. If you init this class without any parameters, all symptoms will be marked False.
    """

    fever: bool = False
    dry_cough: bool = False
    shortness_of_breath: bool = False
    sore_throat: bool = False
    runny_nose: bool = False

    def to_form_data(self, inputs: List[Tag]) -> Dict[str, Optional[str]]:
        """
        Given a list of input related html tags (<input>, <option> etc), produce a subset of formdata to be posted to the server.
        :param inputs: List of input related html tags found on the page. This is required to produce the correct key values for the formdata (by looking at the `name` attribute)
        :return: formdata to be posted
        """
        html_input_names = {
            "fever": "Fever",
            "dry_cough": "DryCough",
            "shortness_of_breath": "Shortnessofbreath",
            "sore_throat": "SoreThroat",
            "runny_nose": "RunnyNose",
        }

        form_data = dict()

        for namedtuple_attr, html_sub_name in html_input_names.items():
            html_name = next(
                iter([i.get("name") for i in inputs if html_sub_name in i.get("name")])
            )
            if getattr(self, namedtuple_attr):
                form_data[html_name] = "on"
            else:
                form_data[html_name] = None

        return form_data


@dataclass
class DailyDeclaration:
    """
    Daily declaration. If you init this class without any parameters, all options will be marked False (i.e. you are well).

    Attributes:
        visited_other_countries (bool): If the user has visited any other countries in the past 14 days. Setting this is false but passing a non-empty list to `visited_countries` results in undefined behaviour.
        countries_visited (List[str]): list of country names visited in the past 14 days. Passing non-standard country names results in undefined behaviour.
        received_SHN (bool): If the user has received a Quarantine or Isolation Order or Stay-Home Notice in the past 14 days
        contact_SHN (bool): If the user has come into contact with someone who is a confirmed case for COVID-19 or has been placed on Quarantine or Isolation Order or served Stay-Home Notice
        received_MC (bool): If the user has been issued a medical certificate for respiratory symptoms and the validity date of the MC has not yet expired
        symptoms (Symptoms): List of symptoms this user is experiencing.
    """

    visited_other_countries: bool = False
    countries_visited: List[str] = field(default_factory=list)
    received_SHN: bool = False
    contact_SHN: bool = False
    received_MC: bool = False
    symptoms: Symptoms = field(default_factory=Symptoms)

    def to_form_data(self, inputs: List[Tag]) -> Dict[str, str]:
        """
        Given a list of input related html tags (<input>, <option> etc), produce a subset of formdata to be posted to the server.
        :param inputs: List of input related html tags found on the page. This is required to produce the correct key values for the formdata (by looking at the `name` attribute)
        :return: formdata to be posted
        """
        html_input_names = {
            "visited_other_countries": "OtherCountryVisited",
            "received_SHN": "Notice",
            "contact_SHN": "Contact",
            "received_MC": "MC",
        }

        html_input_values = {
            "OtherCountryVisited": ("rbVisitOtherCountryNo", "rbVisitOtherCountryYes"),
            "Notice": ("rbNoticeNo", "rbNoticeYes"),
            "Contact": ("rbContactNo", "rbContactYes"),
            "MC": ("rbMCNo", "rbMCYes"),
        }

        form_data = dict()

        for namedtuple_attr, html_sub_name in html_input_names.items():
            html_name = next(
                iter([i.get("name") for i in inputs if html_sub_name in i.get("name")])
            )
            if getattr(self, namedtuple_attr):
                form_data[html_name] = html_input_values[html_sub_name][1]
            else:
                form_data[html_name] = html_input_values[html_sub_name][0]

        # add countries visited
        if len(self.countries_visited) > 0:
            html_sub_name = "Countries"
            html_name = next(
                iter([i.get("name") for i in inputs if html_sub_name in i.get("name")])
            )
            form_data[html_name] = ", ".join(self.countries_visited)

        # add symptoms
        form_data = {**form_data, **self.symptoms.to_form_data(inputs)}

        return form_data


class TemperatureReading(Enum):
    OK = "Less than or equal to 37.6°C"
    HIGH_TEMP_BUT_OK = "More than or equal to 37.7°C but I am feeling well"
    HIGH_TEMP_NOT_OK = "More than or equal to 37.7°C and I am not feeling well"


class User:
    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        custom_headers = {
            "Host": "tts.sutd.edu.sg",
            "Origin": "https://tts.sutd.edu.sg",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        self.headers = {**Headers(headers=False).generate(), **custom_headers}
        self.session = None

    def login(self) -> User:
        # get login
        self.session = requests.Session()

        r = self.session.get("https://tts.sutd.edu.sg", headers=self.headers)
        soup = BeautifulSoup(r.text, "html.parser")

        def get_value(i):
            if "Login" in i.get("name"):
                return self.__username
            elif "Password" in i.get("name"):
                return self.__password
            else:
                return i.get("value")

        form_data = {i.get("name"): get_value(i) for i in soup.find_all("input")}

        url_to_post = "https://tts.sutd.edu.sg" + soup.form.get("action").lstrip(".")

        r = self.session.post(url_to_post, data=form_data)

        assert "tt_home_user" in r.url

        return self

    def take_temperature(self, temperature: TemperatureReading) -> User:
        r = self.session.get(
            "https://tts.sutd.edu.sg/tt_temperature_taking_user.aspx",
            headers=self.headers,
        )

        assert "tt_temperature_taking_user" in r.url

        soup = BeautifulSoup(r.text, "html.parser")

        def get_value(i):
            if "Temperature" in i.get("name"):
                return temperature.value
            else:
                return i.get("value") or ""

        form_data = {
            i.get("name"): get_value(i) for i in soup.select("input, select, textarea")
        }

        url_to_post = "https://tts.sutd.edu.sg" + soup.form.get("action").lstrip(".")

        custom_headers = {
            "Referer": "https://tts.sutd.edu.sg/tt_temperature_taking_user.aspx"
        }

        r = self.session.post(
            url_to_post, data=form_data, headers={**self.headers, **custom_headers}
        )

        return self

    def do_daily_declaration(self, declaration: DailyDeclaration) -> User:
        r = self.session.get(
            "https://tts.sutd.edu.sg/tt_daily_dec_user.aspx", headers=self.headers
        )

        assert "tt_daily_dec_user" in r.url

        soup = BeautifulSoup(r.text, "html.parser")

        inputs = soup.find_all("input")

        custom_headers = {"Referer": "https://tts.sutd.edu.sg/tt_daily_dec_user.aspx"}

        initial_form_data = {i.get("name"): i.get("value") for i in inputs}

        url_to_post = "https://tts.sutd.edu.sg" + soup.form.get("action").lstrip(".")

        form_data = {**initial_form_data, **declaration.to_form_data(inputs)}

        filtered_form_data = {k: v for (k, v) in form_data.items() if v is not None}

        r = self.session.post(
            url_to_post,
            data=filtered_form_data,
            headers={**self.headers, **custom_headers},
        )

        return self
