"""Fetch latest Ziggo outages and announcements."""
from aiohttp import ClientSession, ClientResponseError
from dataclasses import dataclass
import logging


@dataclass
class ZiggoOutages:
    """Class for holding Ziggo outages & announcements."""

    URL = "https://restapi.ziggo.nl/1.0/incidents/"
    NAME = "Ziggo outages & announcements"

async def get_ziggo_status(postalcode, housenumber, session: ClientSession, *, source=ZiggoOutages):
    """Fetch Ziggo outages & announcements."""
    URL = source.URL + postalcode + "/" + housenumber

    resp = await session.get(URL)
    data = await resp.json(content_type=None)

    if data["callback"]["error"]:
        # Error could occur with wrong house number or postal code
        raise ClientResponseError(
            resp.request_info,
            resp.history,
            status="An error occurred",
            message=data["callback"]['error_message'],
            headers=resp.headers
        )

    if not data["announcements"] and not data["outages"]:
        return "No announcements or outages known"

    elif data["outages"]:
        return data["outages"]

    elif data["announcements"]:
        return data["announcements"]