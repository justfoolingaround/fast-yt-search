from .utils import get_maxres_video_thumbnail, get_text, bump_channel_thumbnail


def from_playlist_renderer(data: dict):

    component = {
        "id": data["playlistId"],
        "title": get_text(data["title"]),
    }

    if "videoCountText" in data:
        component["video_count"] = get_text(data["videoCountText"], runs_joiner=" ")

    if "publishedTimeText" in data:
        component["relative_upload_time"] = get_text(data["publishedTimeText"])

    owner_runs = data.get("longBylineText", {}).get("runs", [])

    if owner_runs:
        channel = owner_runs[0]
        channel_component = {
            "id": channel["navigationEndpoint"]["browseEndpoint"]["browseId"],
            "name": channel["text"],
        }
        component["channel"] = channel_component

    def genexp():
        for video in data.get("videos"):
            video_component = video["childVideoRenderer"]

            internal_component = {
                "title": get_text(video_component["title"]),
                "id": video_component["videoId"],
                "thumbnail": get_maxres_video_thumbnail(video_component["videoId"]),
            }

            is_live = not ("lengthText" in video_component)
            internal_component.update(is_live=is_live)

            if not is_live:
                internal_component["duration"] = get_text(video_component["lengthText"])

            yield internal_component

    component["videos"] = list(genexp())

    return component
