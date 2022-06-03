from .utils import bump_channel_thumbnail, get_text


def from_horizontalcard_renderer(data: dict):
    def genexp():
        for card in data["cards"]:

            renderer = card["searchRefinementCardRenderer"]

            component = {}

            thumbnails = [
                _["url"] for _ in renderer.get("thumbnail", {}).get("thumbnails", [])
            ]

            if thumbnails:
                selected = thumbnails[-1]

                if selected[-13:] == "mqdefault.jpg":
                    component.update(thumbnail=selected)
                else:
                    component.update(thumbnail=bump_channel_thumbnail(thumbnails[-1]))

            component.update(
                query=get_text(renderer["query"]),
            )

            yield component

    return list(genexp())
