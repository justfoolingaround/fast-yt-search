import re

GOOGLE_PHOTOS_URL_RE = re.compile(r"^(?:(?:https?:)?//)(.+?\.ggpht\.com/.+?)=(.+)$")
YOUTUBE_THUMBNAIL_URL_RE = re.compile(
    r"^(?:(?:https?:)?//)(?:.+?\.ytimg|img\.youtube)\.com/v[i0-9]/(.+?)/.+?\.[^&?/]+$"
)


def get_text(
    component: dict, *, runs_joiner=", ", run_accessor=lambda run: run["text"]
):

    if "runs" in component:
        return runs_joiner.join(run_accessor(run) for run in component["runs"])

    if "simpleText" in component:
        return component["simpleText"]

    return None


def get_maxres_video_thumbnail(video_id: str):
    return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"


def bump_image(image, *, size=10000):

    google_photos_match = GOOGLE_PHOTOS_URL_RE.match(image)

    if google_photos_match:
        return f"https://{google_photos_match.group(1)}=s{size}"

    youtube_thumbnail_match = YOUTUBE_THUMBNAIL_URL_RE.match(image)

    if youtube_thumbnail_match:
        return get_maxres_video_thumbnail(youtube_thumbnail_match.group(1))

    return image
