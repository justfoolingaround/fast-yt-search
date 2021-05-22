"""
Perform a full search on YouTube with filters.

Only one filter at a time is supported because piling up filters requires some sort of algorithm.
"""

import json
import re

INITIAL_JSON_RE = re.compile(r"ytInitialData = ({.*});")
SEARCH_PAGE = "https://www.youtube.com/results"

FILTERS = {
    "last hour": "EgIIAQ",
    "today": "EgIIAg",
    "this week": "EgIIAw",
    "this month": "EgIIBA",
    "this year": "EgIIBQ",
    "<4": "EgIYAQ",
    "4-20": "EgIYAw",
    "20<": "EgIYAg",
    "live": "EgJAAQ",
    "4k": "EgJwAQ",
    "hd": "EgIgAQ",
    "subtitles": "EgIoAQ",
    "creative commons": "EgIwAQ",
    "360": "EgJ4AQ",
    "vr180": "EgPQAQE",
    "3d": "EgI4AQ",
    "hdr": "EgPIAQE",
    "location": "EgO4AQE",
    "purchased": "EgJIAQ",
    "relevance": "CAA",
    "upload date": "CAI",
    "view count": "CAM",
    "rating": "CAE"
}

def json_parse_search(html_content: str):
    """
    Extract the JSON content that YouTube initializes in a search results page.
    """
    return json.loads(INITIAL_JSON_RE.search(html_content).group(1))

def is_empty(content):
    return content == {'video_id': '', 'video_title': '', 'video_thumbnail': 'https://i.ytimg.com/vi//maxresdefault.jpg', 'video_duration': '', 'mini_description': '', 'creator': {'name': '', 'channel_url': 'https://www.youtube.com/channel/', 'avatar_url': 'https://www.youtube.com/404', 'verified': False, 'verified_artist': False}, 'features': [], 'views': '', 'relative_upload_time': ''}

def dict_conversion(content: dict):
    return {
        'video_id': content.get('videoId', ''),
        'video_title': ''.join(c.get('text', {}) for c in content.get('title', {}).get('runs', [])),
        'video_thumbnail': "https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(content.get('videoId', '')),
        'video_duration': content.get('lengthText', {}).get('simpleText', ''),
        'mini_description': ''.join(c.get('text', {}) for c in content.get('detailedMetadataSnippets', [{}])[0].get('snippetText', {}).get('runs', [])),
        'creator': {
            'name': ''.join(c.get('text', {}) for c in content.get('ownerText', {}).get('runs', [])),
            'channel_url': "https://www.youtube.com/channel/" + (content.get('ownerText', {}).get('runs') or [{}])[0].get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId', ''),
            'avatar_url': content.get('channelThumbnailSupportedRenderers', {}).get('channelThumbnailWithLinkRenderer', {}).get('thumbnail', {}).get('thumbnails', [{}])[0].get('url', 'https://www.youtube.com/404'),
            'verified': any(d.get('metadataBadgeRenderer', {}).get('style', '').startswith('BADGE_STYLE_TYPE_VERIFIED') for d in content.get('ownerBadges', [])),
            'verified_artist': any(d.get('metadataBadgeRenderer', {}).get('style', '') == 'BADGE_STYLE_TYPE_VERIFIED_ARTIST' for d in content.get('ownerBadges', []))
        },
        'features': [c.get('metadataBadgeRenderer', {}).get('label', '').lower() for c in content.get('badges', [])],
        'views': content.get('viewCountText', {}).get('simpleText', '') or 'live',
        'relative_upload_time': content.get('publishedTimeText', {}).get('simpleText', '') or 'live',
    }
    
def search(session, query, filtering=None, **session_kwargs):
    
    params = {
        'search_query': query,
        'region': 'en',
    }
    
    if filtering and (filtering.lower() in FILTERS):
        params.update({'sp': filtering})
        
    with session.get(SEARCH_PAGE, params=params, **session_kwargs) as youtube_results:
        for content in json_parse_search(youtube_results.text).get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [{}])[0].get('itemSectionRenderer', {}).get('contents', []):
            if not is_empty(content):
                yield dict_conversion(content.get('videoRenderer', {}))
                
async def async_search(session, query, filtering=None, other_params={}, **session_kwargs):
    
    params = {
        'search_query': query,
        'region': 'en',
    }
    
    if filtering and (filtering.lower() in FILTERS):
        params.update({'sp': filtering})
        
    async with session.get(SEARCH_PAGE, params=params | other_params, **session_kwargs) as youtube_results:
        for content in json_parse_search(await youtube_results.text()).get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [{}])[0].get('itemSectionRenderer', {}).get('contents', []):
            if not is_empty(content):
                yield dict_conversion(content.get('videoRenderer', {}))