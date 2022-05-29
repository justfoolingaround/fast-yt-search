def get_text(
    component: dict, *, runs_joiner=", ", run_accessor=lambda run: run["text"]
):

    if "runs" in component:
        return runs_joiner.join(run_accessor(run) for run in component["runs"])

    if "simpleText" in component:
        return component["simpleText"]

    return None


def bump_channel_thumbnail(thumbnail: str, *, size=10000):
    prefix, _ = thumbnail.rsplit("=")
    return f"{prefix}=s{size}"


def get_maxres_video_thumbnail(video_id):
    return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
