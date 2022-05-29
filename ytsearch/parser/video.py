from .utils import get_maxres_video_thumbnail, get_text, bump_channel_thumbnail


def from_video_renderer(data: dict):

    component = {
        "id": data["videoId"],
        "thumbnail": get_maxres_video_thumbnail(data["videoId"]),
        "title": get_text(data["title"]),
        "views": get_text(data["viewCountText"], runs_joiner=" "),
    }

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

    channel_info_raw = data["ownerText"]["runs"]

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
        channel_info.update(thumbnail=bump_channel_thumbnail(thumbnails[0]))

    component.update(channel_info=channel_info)

    return component
