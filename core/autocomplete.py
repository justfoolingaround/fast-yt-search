"""
YouTube search's autocomplete.
"""

import re

SUGGEST_QUERIES = "https://suggestqueries-clients6.youtube.com/complete/search"
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

AUTOCOMPLETE_PARSER = re.compile(r'\["([^"]+)"')

def autocomplete(session, incomplete_query, *,
        client_name='youtube', home_language='en', global_language='en', video_id=None):
    """
    YouTube's autocomplete; the content will vary from language to language and can be adjusted to a specific video using that video's id.
    """
    query = {
        'q': incomplete_query,
        'hl': home_language,
        'gl': global_language,
        'client': client_name,
        'callback': 'h',
    }
    
    if video_id:
        query.update({'video_id': video_id})
        
    return AUTOCOMPLETE_PARSER.findall(session.get(SUGGEST_QUERIES, params=query, headers=HEADERS).text)[1:]