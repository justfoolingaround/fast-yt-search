<p align="center"><img src="https://capsule-render.vercel.app/api?type=soft&fontColor=d60a79&text=fast-youtube-search&height=150&fontSize=60&desc=The most powerful and fastest YouTube searching Python library.&descAlignY=75&descAlign=60&color=00000000&animation=twinkling"></p>

## Overview

- [Installation](#installation)
    1. [PIP Installation](#pip-installation)
    2. [Source Code Download](#source-code-download)
- [Usage](#usage)
- [Core Features](#core-features)
- [Functioning](#functioning)

## Installation

This project can be installed on to your device via different mechanisms, these mechanisms are listed below in the order of ease.

<ol>

<li id="pip-installation"> PIP Installs Packages <strong>aka</strong> PIP Installation 

    $ pip install git+https://www.github.com/justfoolingaround/fast-youtube-search
</li>
<li id="source-code-download"> Source Code Download

    $ git clone https://www.github.com/justfoolingaround/fast-youtube-search

Given that you have [`git`](https://git-scm.com/) installed, you can clone the repository from GitHub. If you do not have or want to deal with installation of [`git`](https://git-scm.com/), you can simply download the repository using [this link.](https://github.com/justfoolingaround/fast-youtube-search/archive/refs/heads/master.zip)

After the repository is downloaded and placed in an appropriate directory, you can use [`setup.py`](./setup.py) to proceed with the installation.

    $ pip install .
</li>
</ol>
This command is to be executed from the directory where the repository is located.

**Additional information:** You **must** have Python installed **and** in PATH to use this project properly. Your Python executable may be `py` **or** `python` **or** `python3`. **Only Python 3.6 and higher versions are supported by the project.**

## Usage

```py
import httpx # requests is also supported, httpx is better.

import ytsearch

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

# We're going to be using a PC user-agent to get full functionality.

client = httpx.Client(headers=headers)

for estimated_results, component in ytsearch.search(client, "Rick Astley - Never Gonna Give You Up"):
    print(component)

# This is going to get the first page, now for the fully filtered **all** results.

for estimated_results, component in ytsearch.search(client, "Rick Astley - Never Gonna Give You Up", content_type=ytsearch.filters.ContentType.VIDEO, keep_searching=True):
    print(component)
```

## Core Features

- Devastatingly powerful, can search **any** YouTube content limitlessly and effortlessly.
- Supports search filters, and you can pile them up.
- Easy API reference, just import n' use.
- **No external dependency required for installation.** Session clients of libraries similar to `python-requests` or `httpx` will work.
- User controlled API client context and user-agent.
- Gives you whatever you see based on your settings.
    - For PC user agents, it will give you those moving thumbnails, namely `rich thumbnails`.
- High efficiency code.
- Supports autocomplete, with the option to set with a video context.
- Gives the highest possible images for thumbnails and channel profile images.

## Functioning

This project functions similarly to your YouTube client, you give it a query, it'll run a search. If you scroll down, it'll give you the illusion of infinite scroll. 

Except, this project is faster. It doesn't load anything other than what is required.
