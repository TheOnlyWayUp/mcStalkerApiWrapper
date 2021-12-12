The MCStalker API Wrapper
---------------------------
Async-Friendly wrapper for the MCStalker API.

**Check out the [Wiki](https://github.com/TheOnlyWayUp/mcStalkerApiWrapper/wiki) for examples and more information!**

Discord - https://discord.gg/bQhzbg27cm

MCStalker - [https://mcstalker.com](https://mcstalker.com/ref/mcstalkerispog)

Pypi - https://pypi.org/project/mcStalker

Created by TheOnlyWayUp#1231

----------


Endpoints currently supported - 
- /stats
- /searchusername
- /searchserver
- /filterservers

YOU NEED AN API KEY TO USE THIS WRAPPER.

You can get a key at https://mcstalker.com/register

Imports - 
- from mcStalker import Player(apiKey)
- from mcStalker import Server(apiKey)
- from mcStalker import Stats(apiKey)

Usage -

Stats -
  ```python
      from mcStalker import Stats
      stats = Stats(apiKey)
      asyncio.run(stats.returnStats() -> Stats._Stats Object)
  ```

Player -
  ```python
      from mcStalker import Player
      player = Player(apiKey)
      asyncio.run(player.returnPlayer(username) -> Player._Player Object)
  ```
  
Server - 
  ```python
      from mcStalker import Server
      server = Server(apiKey)
      asyncio.run(server.returnServer(ip) -> Server._Server Object)
      asyncio.run(server.returnTopServers() -> [Server._Server Object, Server._Server Object, ...])
  ```
  
Created by TheOnlyWayUp#1231 - https://github.com/TheOnlyWayUp/

MCStalker created by SSouper - https://github.com/SSouper
