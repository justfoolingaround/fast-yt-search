from .utils import get_text


def from_show_renderer(data: dict):

    component = {
        "title": get_text(data["title"]),
    }

    owner_runs = data.get("longBylineText", {}).get("runs", [])

    if owner_runs:
        channel = owner_runs[0]
        channel_component = {
            "id": channel["navigationEndpoint"]["browseEndpoint"]["browseId"],
            "name": channel["text"],
        }
        component["channel"] = channel_component

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

    return component
