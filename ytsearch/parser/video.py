from dataclasses import dataclass

from .channel import Channel
from .utils import bump_image, get_maxres_video_thumbnail, get_text


@dataclass
class Video:
    id: str
    title: str
    thumbnail: str
    channel: Channel = None

    views: str = None
    duration: str = None
    is_live: bool = False
    short_description: str = None
    rich_thumbnail: list = None
    badges: list = None
    relative_upload_time: str = None


def from_video_renderer(data: dict):

    component = {
        "id": data["videoId"],
        "thumbnail": get_maxres_video_thumbnail(data["videoId"]),
        "title": get_text(data["title"]),
    }

    if "viewCountText" in data:
        component["views"] = get_text(data["viewCountText"], runs_joiner=" ")

    if "richThumbnail" in data:
        component["rich_thumbnail"] = [
            _["url"]
            for _ in data["richThumbnail"]["movingThumbnailRenderer"][
                "movingThumbnailDetails"
            ]["thumbnails"]
        ]

    if "badges" in data:
        component["badges"] = [
            _["metadataBadgeRenderer"]["style"] for _ in data["badges"]
        ]

    if "publishedTimeText" in data:
        component["relative_upload_time"] = get_text(data["publishedTimeText"])

    if "detailedMetadataSnippets" in data:
        component["short_description"] = "\n".join(
            get_text(_["snippetText"]) for _ in data["detailedMetadataSnippets"]
        )

    is_live = not ("lengthText" in data)
    component.update(is_live=is_live)

    if not is_live:
        component["duration"] = get_text(data["lengthText"])

    if "ownerText" in data:
        channel_info_raw = data["ownerText"]

        channel_info = {
            "id": get_text(
                channel_info_raw,
                run_accessor=lambda run: run["navigationEndpoint"]["browseEndpoint"][
                    "browseId"
                ],
            ),
            "name": get_text(channel_info_raw, run_accessor=lambda run: run["text"]),
        }

        if "ownerBadges" in data:
            channel_info["badges"] = [
                _["metadataBadgeRenderer"]["style"] for _ in data["ownerBadges"]
            ]

        thumbnails = [
            _["url"]
            for _ in data["channelThumbnailSupportedRenderers"][
                "channelThumbnailWithLinkRenderer"
            ]["thumbnail"]["thumbnails"]
        ]

        if thumbnails:
            channel_info.update(thumbnail=bump_image(thumbnails[0]))

        component.update(channel=Channel(**channel_info))

    return Video(**component)
