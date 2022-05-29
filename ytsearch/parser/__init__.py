from .channel import from_channel_renderer
from .playlist import from_playlist_renderer
from .show import from_show_renderer
from .video import from_video_renderer


def iter_from_item_section_renderer(data: dict):

    for renderer_shelf in data["contents"]:

        if "videoRenderer" in renderer_shelf:
            yield {
                "type": "video",
                "content": from_video_renderer(renderer_shelf["videoRenderer"]),
            }
        else:
            if "channelRenderer" in renderer_shelf:
                yield {
                    "type": "channel",
                    "content": from_channel_renderer(renderer_shelf["channelRenderer"]),
                }
            else:
                if "playlistRenderer" in renderer_shelf:
                    yield {
                        "type": "playlist",
                        "content": from_playlist_renderer(
                            renderer_shelf["playlistRenderer"]
                        ),
                    }
                else:
                    if "showRenderer" in renderer_shelf:
                        yield {
                            "type": "show",
                            "content": from_show_renderer(
                                renderer_shelf["showRenderer"]
                            ),
                        }
