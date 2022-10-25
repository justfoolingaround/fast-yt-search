from . import filters
from .constants import PUBLIC_YOUTUBE_API_KEY, YOUTUBE_SEARCH_API, YOUTUBE_SEARCH_URL
from .parser import iter_from_item_section_renderer


def fetch_data(data: dict, *, initial=False):

    if initial:
        medias = (
            data.get("contents", {})
            .get("twoColumnSearchResultsRenderer", {})
            .get("primaryContents", {})
            .get("sectionListRenderer", {})
            .get("contents", [])
        )
    else:
        medias = (
            data.get("onResponseReceivedCommands", [{}])[0]
            .get("appendContinuationItemsAction", {})
            .get("continuationItems", [])
        )

    if len(medias) > 1:
        item_selection_renderer, continuation_tracker = medias
    else:
        item_selection_renderer, continuation_tracker = medias[0], {}

    estimated_results = int(data["estimatedResults"])
    items = item_selection_renderer.get("itemSectionRenderer", [])
    continuation_token = (
        continuation_tracker.get("continuationItemRenderer", {})
        .get("continuationEndpoint", {})
        .get("continuationCommand", {})
        .get("token", None)
    )
    return estimated_results, items, continuation_token


youtube_client_version = "2.20221021.00.00"
youtube_client_name = "1"


def youtube_pbj_request(
    session,
    *args,
    params={},
    headers={},
    youtube_client_version=youtube_client_version,
    youtube_client_name=youtube_client_name,
    **kwargs,
):

    params.update({"pbj": "1"})
    headers.update(
        {
            "x-youtube-client-name": youtube_client_name,
            "x-youtube-client-version": youtube_client_version,
        }
    )

    return session.get(
        *args,
        params=params,
        headers=headers,
        **kwargs,
    )


def search(
    session,
    query: str,
    *,
    sort_by: "filters.SortBy | None" = filters.SortBy.RELEVANCE,
    features: "tuple[filters.Feature]" = (),
    duration: "filters.Duration" = None,
    content_type: "filters.ContentType" = None,
    upload_time: "filters.UploadTime" = None,
    autocorrect: bool = False,
    keep_searching: bool = False,
    youtube_client_version=youtube_client_version,
    youtube_client_name=youtube_client_name,
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
    }

    if filter_key:
        params["sp"] = filter_key

    youtube_response = youtube_pbj_request(
        session,
        YOUTUBE_SEARCH_URL,
        params=params,
        youtube_client_name=youtube_client_name,
        youtube_client_version=youtube_client_version,
    )

    _, returned_data = youtube_response.json()

    (
        estimated_results,
        item_selection_renderer,
        continuation_token,
    ) = fetch_data(returned_data["response"], initial=True)

    for component in iter_from_item_section_renderer(item_selection_renderer):
        yield component | {"estimated_results": estimated_results}

    if not keep_searching:
        return

    component = {}

    context = {
        "hl": "en",
        "client": {
            "clientName": youtube_client_name,
            "clientVersion": youtube_client_version,
        },
    }

    while component is not None and continuation_token is not None:

        component = None

        response = session.post(
            YOUTUBE_SEARCH_API,
            params={
                "key": PUBLIC_YOUTUBE_API_KEY,
            },
            json={"context": context, "continuation": continuation_token},
        ).json()

        (
            estimated_results,
            item_selection_renderer,
            continuation_token,
        ) = fetch_data(response)

        for component in iter_from_item_section_renderer(item_selection_renderer):
            yield estimated_results | {"estimated_results": estimated_results}
