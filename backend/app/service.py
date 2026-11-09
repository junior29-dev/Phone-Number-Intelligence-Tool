"""Core logic: pure functions, no web framework, easy to test."""
from functools import lru_cache

import httpx
import phonenumbers
from phonenumbers import PhoneNumberFormat as Fmt
from phonenumbers import PhoneNumberType as T
from phonenumbers import carrier, geocoder, timezone

from . import config

OPENCAGE_URL = "https://api.opencagedata.com/geocode/v1/json"

LINE_TYPES = {
    T.MOBILE: "Mobile", T.FIXED_LINE: "Fixed line", T.FIXED_LINE_OR_MOBILE: "Fixed line or mobile",
    T.TOLL_FREE: "Toll free", T.PREMIUM_RATE: "Premium rate", T.VOIP: "VoIP",
    T.PERSONAL_NUMBER: "Personal number", T.PAGER: "Pager", T.UAN: "Universal access",
    T.VOICEMAIL: "Voicemail", T.SHARED_COST: "Shared cost", T.UNKNOWN: "Unknown",
}


class InvalidNumber(ValueError):
    """Raised when the input cannot be parsed as a phone number."""


def parse(raw: str, region: str | None = None) -> phonenumbers.PhoneNumber:
    try:
        return phonenumbers.parse(raw, region)
    except phonenumbers.NumberParseException as exc:
        raise InvalidNumber(str(exc)) from exc


@lru_cache(maxsize=512)
def geocode(place: str) -> tuple[float, float] | None:
    """Look up coordinates with OpenCage. Cached, and returns None on any failure."""
    if not config.OPENCAGE_KEY or not place:
        return None
    try:
        resp = httpx.get(
            OPENCAGE_URL,
            params={"q": place, "key": config.OPENCAGE_KEY, "limit": 1, "no_annotations": 1},
            timeout=8,
        )
        resp.raise_for_status()
        results = resp.json()["results"]
    except (httpx.HTTPError, KeyError, ValueError):
        return None
    if not results:
        return None
    geo = results[0]["geometry"]
    return geo["lat"], geo["lng"]


def analyze(raw: str, region: str | None = None, with_map: bool = True) -> dict:
    num = parse(raw, region)
    location = geocoder.description_for_number(num, "en")
    country = geocoder.country_name_for_number(num, "en")
    place = f"{location}, {country}" if location and country and location != country else (location or country)
    coords = geocode(place) if with_map else None
    return {
        "input": raw,
        "possible": phonenumbers.is_possible_number(num),
        "valid": phonenumbers.is_valid_number(num),
        "formats": {
            "e164": phonenumbers.format_number(num, Fmt.E164),
            "international": phonenumbers.format_number(num, Fmt.INTERNATIONAL),
            "national": phonenumbers.format_number(num, Fmt.NATIONAL),
        },
        "country_code": num.country_code,
        "region": phonenumbers.region_code_for_number(num),
        "location": location or None,
        "country": country or None,
        "carrier": carrier.name_for_number(num, "en") or None,
        "line_type": LINE_TYPES.get(phonenumbers.number_type(num), "Unknown"),
        "timezones": list(timezone.time_zones_for_number(num)),
        "coordinates": {"lat": coords[0], "lng": coords[1]} if coords else None,
    }
