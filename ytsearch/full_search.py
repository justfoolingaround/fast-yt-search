from . import filters
from .constants import PUBLIC_YOUTUBE_API_KEY, YOUTUBE_SEARCH_API, YOUTUBE_SEARCH_URL
from .parser import iter_from_item_section_renderer


def sanitise_api_response(data: dict):

    if "contents" in data:
        medias = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"]
    else:
        medias = data["onResponseReceivedCommands"][0]["appendContinuationItemsAction"][
            "continuationItems"
        ]

    if len(medias) > 1:
        item_selection_renderer, continuation_tracker = medias
    else:
        item_selection_renderer, continuation_tracker = medias[0], None

    return (
        int(data["estimatedResults"]),
        item_selection_renderer["itemSectionRenderer"],
        continuation_tracker["continuationItemRenderer"]["continuationEndpoint"][
            "continuationCommand"
        ]["token"]
        if continuation_tracker is not None
        else None,
    )


youtube_client_version = "2.20200304.02.01"
youtube_client_name = "1"

context = {
    "hl": "en",
    "client": {
        "clientName": youtube_client_name,
        "clientVersion": youtube_client_version,
    },
}


def search(
    session,
    query,
    *,
    sort_by=filters.SortBy.RELEVANCE,
    features=(),
    duration=None,
    content_type=None,
    upload_time=None,
    autocorrect=False,
    keep_searching=False,
    custom_api_context=context,
):

    filter_key = filters.get_filter_key(
        sort_by=sort_by,
        features=features,
        duration=duration,
        content_type=content_type,
        upload_time=upload_time,
        autocorrect=autocorrect,
    )

    params = {
        "hl": "en",
        "search_query": query,
        "pbj": "1",
    }

    if filter_key:
        params["sp"] = filter_key

    youtube_response = session.get(
        YOUTUBE_SEARCH_URL,
        params=params,
        headers={
            "x-youtube-client-name": youtube_client_name,
            "x-youtube-client-version": youtube_client_version,
        },
    ).json()[1]["response"]
    (
        estimated_results,
        item_selection_renderer,
        continuation_token,
    ) = sanitise_api_response(youtube_response)

    for component in iter_from_item_section_renderer(item_selection_renderer):
        yield estimated_results, component

    if not keep_searching:
        return

    component = {}

    while component is not None and continuation_token is not None:

        component = None

        response = session.post(
            YOUTUBE_SEARCH_API,
            params={
                "key": PUBLIC_YOUTUBE_API_KEY,
            },
            json={"context": custom_api_context, "continuation": continuation_token},
        ).json()

        (
            estimated_results,
            item_selection_renderer,
            continuation_token,
        ) = sanitise_api_response(response)

        for component in iter_from_item_section_renderer(item_selection_renderer):
            yield estimated_results, component
