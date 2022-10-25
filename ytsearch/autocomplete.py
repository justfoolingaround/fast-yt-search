import json

SUGGEST_QUERIES_ENDPOINT = "https://suggestqueries-clients6.youtube.com/complete/search"


def autocomplete(
    session,
    incomplete_query,
    *,
    client_name="youtube",
    home_language="en",
    video_id=None
):
    query = {
        "q": incomplete_query,
        "hl": home_language,
        "client": client_name,
        "callback": ".",
    }

    if video_id:
        query.update({"video_id": video_id})

    for __ in json.loads(
        session.get(SUGGEST_QUERIES_ENDPOINT, params=query).text[7:-1]
    )[1:-1]:
        for result, _, _ in __:
            yield result
