from dataclasses import dataclass

from .channel import Channel
from .utils import get_text


@dataclass
class Show:
    id: str
    title: str
    channel: Channel = None
    thumbnail: str = None


def from_show_renderer(data: dict):

    component = {
        "title": get_text(data["title"]),
    }

    owner_runs = data.get("longBylineText", {}).get("runs", [])

    if owner_runs:
        channel = owner_runs[0]
        component["channel"] = Channel(
            channel["navigationEndpoint"]["browseEndpoint"]["browseId"],
            channel["text"],
        )

    if "naviagtionEndpoint" in data:
        component["id"] = data["navigationEndpoint"]["browseEndpoint"]["browseId"]

    thumbnails = (
        data.get("thumbnailRenderer", {})
        .get("showCustomThumbnailRenderer", {})
        .get("thumbnail", {})
        .get("thumbnails", [])
    )

    if thumbnails:
        highest_quality = thumbnails[-1]

        component.update(thumbnail=highest_quality["url"])

    return Show(**component)
