# Fast YouTube Search

**Fast YouTube Search** consists of powerful and efficient functions to scrape out almost every search results from YouTube.

This project is intended to be made an extension for your projects (custom YouTube clients that doesn't track anything or Discord bots?).

### Core Features

- Asynchronous mode with `aiohttp` is supported for searching.
- Can use filtering from the YouTube search.
- Does not use `youtube-dl` or any heavy dependencies.
- Includes channel avatar, verification status and video features (Live, New, 4k, 360) in the results.
- Incredibly fast, light-weight and efficient.
- No API keys required.
- Region and/or video based autocomplete is included.
- Supports proxies, custom headers, cookies.

### Usage

```py

import requests

from yt_search import search

session = requests.Session()

for content in search(session, 'random video', filtering='4k'):
    print("'{video_title}' by {creator[name]}".format(**content))

```

For asynchronous usage, aiohttp is required.

```py

import asyncio
import aiohttp

from yt_search import async_search as search

async def async_main():
    session = aiohttp.ClientSession()

    async for content in search(session, 'random video', filtering='4k'):
        print("'{video_title}' by {creator[name]}".format(**content))

loop = asyncio.get_event_loop()
loop.run_until_complete(async_main())

```

### Data Structure

Here's a example of the structure of the dictionary returned by this program:

```py

{
    "video_id": "dQw4w9WgXcQ",
    "video_title": "Rick Astley - Never Gonna Give You Up (Video)",
    "video_thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
    "video_duration": "3:33",
    "mini_description": "Lyrics: Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry\u00a0...",
    "creator": {
        "name": "Official Rick Astley",
        "channel_url": "https://www.youtube.com/channel/UCuAXFkgsw1L7xaCfnd5JJOw",
        "avatar_url": "https://yt3.ggpht.com/ytc/AAUvwni36SveDisR-vOAmmklBfJxnnjuRG3ihzfrwEfORA=s88-c-k-c0x00ffffff-no-rj",
        "verified": True,
        "verified_artist": True
    },
    "features": [],
    "views": "94,87,24,080 views",
    "relative_upload_time": "11 years ago"
}

```

### Requirements

- Python 3.6 + 
- aiohttp (for using asynchronous search)