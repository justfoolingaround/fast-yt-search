from dataclasses import dataclass

from .utils import bump_image, get_text


@dataclass
class Channel:
    id: str
    name: str
    video_count: str = None
    subscriber_count: str = None
    description: str = None
    badges: list = None
    thumbnail: str = None


def from_channel_renderer(data: dict):

    component = {
        "id": data["channelId"],
        "name": get_text(data["title"]),
    }

    if "videoCountText" in data:
        component["video_count"] = get_text(data["videoCountText"], runs_joiner=" ")

    if "subscriberCountText" in data:
        component["subscriber_count"] = get_text(data["subscriberCountText"])

    if "descriptionSnippet" in data:
        component["description"] = get_text(data["descriptionSnippet"])

    if "ownerBadges" in data:
        component["badges"] = [
            _["metadataBadgeRenderer"]["style"] for _ in data["ownerBadges"]
        ]

    thumbnails = [_["url"] for _ in data["thumbnail"]["thumbnails"]]

    if thumbnails:
        component.update(thumbnail=bump_image(thumbnails[0]))

    return Channel(**component)
