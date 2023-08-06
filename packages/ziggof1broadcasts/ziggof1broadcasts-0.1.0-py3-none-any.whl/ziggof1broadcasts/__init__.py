"""Fetch latest Ziggo F1 broadcasts."""
import datetime
import json

from aiohttp import ClientSession, ClientResponseError

class ZiggoF1Broadcasts:
    """Class for holding Ziggo F1 broadcasts details."""

    NAME = "Ziggo F1 broadcasts"
    URL = "https://web-api-pepper.horizon.tv/oesp/v2/NL/nld/web/listings?byStartTime=##Time##~&byEndTime=##Time##~&byLocationId=24443942973&byStationId=675503655063&sort=startTime"


async def get_ziggo_f1_broadcasts(session: ClientSession, *, source=ZiggoF1Broadcasts, startTime=datetime.date.today()):
    """Fetch Ziggo F1 broadcasts."""

    # Replace the placeholders in the URL with the starttime
    convertedURL = source.URL.replace("##Time##", startTime.strftime('%Y-%m-%dT%H:%M:%SZ'))

    # Gather the data from the Horizon API
    resp = await session.get(convertedURL)
    data = await resp.json(content_type='application/json')

    # Only gather the Formule 1 GP broadcasts - skip the condensed broadcasts
    output_dict = [
        x for x in data['listings']
        if "Formule 1 GP" in x['program']['title']
        and "(samenvatting)" not in x['program']['title']
    ]

    return output_dict
