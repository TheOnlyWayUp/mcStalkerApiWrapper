from setuptools import setup, find_packages


LONGDESCRIPTION = """
The MCStalker API Wrapper
---------------------------
Async-Friendly wrapper for the MCStalker API.

[![N|Solid](https://mcstalker.com/favicon-32x32.png)](https://mcstalker.com/ref/mcstalkerispog)

Endpoints currently supported - 
- /stats
- /searchusername
- /searchserver
- /filterservers

YOU NEED AN API KEY TO USE THIS WRAPPER.

You can get a key at https://mcstalker.com/register

Imports - 
- Non Cached
```python
  from mcStalker.mcStalker import Player
  from mcStalker.mcStalker import Server
  from mcStalker.mcStalker import Stats
```

- Cached
```python
  from mcStalker.cachedMCStalker import Player
  from mcStalker.cachedMCStalker import Server
  from mcStalker.cachedMCStalker import Stats
```

Usage -

Stats -
```python
    from mcStalker.mcStalker import Stats #Not cached
    from mcStalker.cachedMCStalker import Stats #Cached
    stats = Stats(apiKey)
    asyncio.run(stats.returnStats() -> Stats._Stats Object)
```

Player -
```python
    from mcStalker.mcStalker import Player #Not cached
    from mcStalker.cachedMCStalker import Player #Cached
    player = Player(apiKey)
    asyncio.run(player.returnPlayer(username) -> Player._Player Object)
```
  
Server - 
```python
    from mcStalker.mcStalker import Server #Not cached
    from mcStalker.cachedMCStalker import Server #Cached
    server = Server(apiKey)
    asyncio.run(server.returnServer(ip) -> Server._Server Object)
    asyncio.run(server.returnTopServers() -> [Server._Server Object, Server._Server Object, ...])
```
  
Created by TheOnlyWayUp#1231 - https://github.com/TheOnlyWayUp/

MCStalker created by SSouper - https://github.com/SSouper
"""

VERSION = "0.0.6"
DESCRIPTION = "mcStalker is an Asynchronous API Wrapper for the MCStalker (https://mcstalker.com) API. It uses modern Pythonic structures to efficiently request information. It features optional caching, is modular, and is easy to integrate."

# Setting up
setup(
    name="mcStalker",
    version=VERSION,
    author="TheOnlyWayUp",
    author_email="thedarkdraconian@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONGDESCRIPTION,
    packages=find_packages(),
    install_requires=["asyncio", "aiohttp"],
    keywords=[
        "async",
        "aiohttp",
        "better_than_sync",
        "mcstalker",
        "minecraft",
        "server_scanning",
        "api_wrapper",
        "minecraft_server",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
