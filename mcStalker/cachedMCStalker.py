import asyncio, aiohttp, json
from cachetools import cached, TTLCache

class MCStalker:
    """The Parent Class, Do not import this."""

    def __init__(self, apiKey):
        self.key = apiKey

    class invalidApiKey(Exception):
        """The invalidApiKey error."""

        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Invalid API Key (Register at https://mcstalker.com/register)- {0} ".format(
                self.message
            )


class Stats(MCStalker):
    """The Stats class."""

    
    class _Stats:
        """The statistics of the API.
        updated: str = The last time the statistics were updated.
        players: int = The number of players currently in the database.
        servers: int = The number of servers currently in the database.
        raw: dict = The raw, cleaned data from the API.
        """

        updated: str = ""
        servers: int = None
        players: int = None
        raw: dict = None

    @staticmethod
    def returnCleanStatsDict(stats: dict):
        """Returns the statistics of the API.

        Args:
            stats (dict): The statistics of the API.

        Returns:
            dict: The statistics of the API.
        """
        _stats = {}
        _stats["lastUpdated"] = stats.get("updated")
        _stats["servers"] = stats.get("servers")
        _stats["players"] = stats.get("players")
        return _stats

    def returnStatsObject(self, statsDict: dict):
        """Returns the statistics of the API.

        Args:
            statsDict (dict): The statistics of the API.
        """
        stats = self._Stats()
        stats.updated = statsDict.get("lastUpdated")
        stats.servers = statsDict.get("servers")
        stats.players = statsDict.get("players")
        stats.raw = statsDict

    async def requestStats(self):
        """Requests the statistics of the API.

        Raises:
            MCStalker.invalidApiKey: If the API key is invalid.

        Returns:
            dict: The statistics of the API.
        """
        async with aiohttp.ClientSession() as session, session.get(
            "https://backend.mcstalker.com/api/stats",
            headers={"Authentication": f"Bearer {self.key}"},
        ) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status == 403:
                raise MCStalker.invalidApiKey(await resp.json()["message"])

    @cached(cache=TTLCache(maxsize=1024, ttl=300))
    async def returnStats(self):
        """Returns the statistics of the API.

        Returns:
            Stats._Stats: The statistics of the API.
        """
        return self.returnStatsObject(
            self.returnCleanStatsDict(await self.requestStats())
        )


def cachedHelp():
    """Returns the help message."""
    x = """
The MCStalker API Wrapper
---------------------------
Async-Friendly wrapper for the MCStalker API.

Endpoints currently supported - 
- /stats
- /searchusername
- /searchserver
- /filterservers

YOU NEED AN API KEY TO USE THIS WRAPPER.
You can register for a key at https://mcstalker.com/register

Imports - 
- from mcStalker.MCStalker import Player
- from mcStalker.MCStalker import Server
- from mcStalker.MCStalker import Stats

Usage -

    Stats -
        from mcStalker.MCStalker import Stats
        stats = Stats(apiKey)
        asyncio.run(stats.returnStats() -> Stats._Stats Object)

    Player -
        from mcStalker.MCStalker import Player
        player = Player(apiKey)
        asyncio.run(player.returnPlayer(username) -> Player._Player Object)

    Server - 
        from mcStalker.MCStalker import Server
        server = Server(apiKey)
        asyncio.run(server.returnServer(ip) -> Server._Server Object)
        asyncio.run(server.returnTopServers() -> [Server._Server Object, Server._Server Object, ...])

Created by TheOnlyWayUp#1231 - https://github.com/TheOnlyWayUp/
MCStalker created by SSouper - https://github.com/SSouper
    """
    print(x)


class Player(MCStalker):
    class _Player:
        """The _Player object, which is used to generate information about a player. Please read the docs for Player() instead."""

        name = ""
        uuid = ""
        addedAt = ""
        lastSeen = ""
        servers = []
        raw = ""

    class playerNotFound(Exception):
        """The requestError error."""

        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Player was not found - {0} ".format(self.message)

    async def requestPlayer(self, url):
        """Requests a player.

        Args:
            url ([str]): The url of the player.

        Returns:
            dict: The player information.
        """
        async with aiohttp.ClientSession() as session, session.get(
            url, headers={"Authorization": f"Bearer {self.key}"}
        ) as resp:
            return await resp.json(), resp.status

    def returnPlayerObject(self, player: dict):
        """Returns a player object.

        Args:
            player (dict): The dict containing player information.

        Returns:
            Player._Player: The player object.
        """
        _player = self._Player()
        _player.name = player["name"]
        _player.uuid = player["uuid"]
        _player.addedAt = player["addedAt"]
        _player.lastSeen = player["lastSeen"]
        _player.raw = player
        return _player

    def returnCleanPlayerDict(self, player: dict):
        """Returns a cleaned player dict.

        Args:
            player (dict): The dict containing player information.

        Returns:
            dict: The cleaned player dict.
        """
        _player = {
            "name": player.get("username"),
            "uuid": player.get("uuid"),
            "addedAt": player.get("createdAt"),
            "lastSeen": player.get("updatedAt"),
            "servers": player.get("servers"),
        }
        return _player

    @cached(cache=TTLCache(maxsize=1024, ttl=300))
    async def returnPlayer(self, username):
        """Returns a player object.

        Args:
            username (str): The username of the player.

        Raises:
            self.invalidApiKey: If the API key is invalid.
            self.playerNotFound: If the player was not found.

        Returns:
            Player._Player: The player object.
        """
        player = await self.requestPlayer(
            "https://backend.mcstalker.com/api/searchusername/" + username
        )
        status = player[1]
        player = player[0]
        if status == 200:
            player = self.returnCleanPlayerDict(player)
            obj = self.returnPlayerObject(player)
            return obj
        if status == 403:
            raise self.invalidApiKey(player["error"])
        raise self.playerNotFound(player["error"])


class Server(MCStalker):
    """The Server class, which is used to generate information about a server."""

    class _ipInfo:
        """The _ipInfo object, which is used to generate information about an IP."""

        loc = None
        org = None
        city = None
        postal = None
        region = None
        country = None
        hostname = None
        timezone = None

    class _Server:
        """The Server Object.
        ip: str = The IP address of the server.
        hostname: str = The hostname of the server.
        favicon: base64 string = The favicon of the server.
        players: list[MCStalker.Player()] = A list of players on the server.
        slots: dict{'online':None, 'max':None} = Player slots of the server.
        motd: str = The MOTD of the server.
        added: Unix timestamp = The time the server was added to the database.
        lastPinged: Unix timestamp = The time the server was last updated.
        vanilla: bool = Whether the server is vanilla or not.
        ipInfo: MCStalker._ipInfo = The IP information of the server.
        version: str = The human friendly version of the server.
        raw: dict = The raw Cleaned JSON response from the server.
        """

        ip = ""
        favicon = ""
        hostname = None
        players = []
        slots = {"online": None, "max": None}
        motd = ""
        added = "Unix Timestamp"
        lastPinged = "Unix Timestamp"
        vanilla = bool
        ipInfo: dict = None
        version: str = None
        raw = ""

    class serverNotFound(Exception):
        """The requestError error."""

        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Server was not found - {0} ".format(self.message)

    def returnCleanMotd(self, motd) -> str:
        """DONT USE, ALTERNATIVE USED IN CODE!!!
        Returns a cleaned MOTD.

        Args:
            motd (any): The MOTD to clean.

        Returns:
            str: The cleaned MOTD.
        """
        if type(motd) is list:
            return "".join([letter["text"] for letter in motd])
        if type(motd) is str:
            return motd
        if type(motd) is dict:
            try:
                return motd["text"]
            except KeyError:
                return self.returnCleanMotd(motd["extra"])
        return None

    def returnCleanServerDict(self, server: dict) -> dict:
        """Returns a clean dict with only the things we need in all the correct places.

        Args:
            server (dict): The dict to clean.

        Returns:
            dict: The cleaned dict.
        """
        _server = {
            "ip": server.get("ip"),
            "favicon": server.get("favicon"),
            "hostname": server.get("ipInfo").get("hostname"),
            "players": server.get("players"),
            "version": server.get("versionName"),
            "slots": {"online": server.get("online"), "max": server.get("max")},
            "motd": server.get("searchMotd"),
            "authStatus": server.get("authStatus"),
            "alive": server.get("alive"),
            "vanilla": server.get("vanilla"),
            "addedAt": server.get("createdAt"),
            "lastPinged": server.get("updatedAt"),
            "ipInfo": server.get("ipInfo"),
        }
        return _server

    def returnServerObject(self, server: dict) -> _Server:
        """Converts a dictionary to a Server object.

        Args:
            server (dict): The dict containing server information.

        Returns:
            Converters._Server: The server object.
        """
        _server = self._Server()
        _server.ip = server.get("ip")
        _server.favicon = server.get("favicon")
        _server.hostname = server.get("hostname")
        _server.slots = server.get("slots")
        try:
            playerClass = Player(self.key)
            _server.players = [
                playerClass.returnPlayerObject(
                    playerClass.returnCleanPlayerDict(player)
                )
                for player in server["players"]
            ]
        except TypeError:
            _server.players = []

        _server.motd = server.get("motd")
        _server.added = server.get("addedAt")
        _server.version = server.get("version")
        _server.lastPinged = server.get("lastPinged")
        _server.vanilla = server.get("vanilla")
        _server.ipInfo = self.returnIpObject(server["ipInfo"])
        _server.raw = server
        return _server

    def returnIpObject(self, ipInfo: dict) -> _ipInfo:
        """Converts a dictionary to an IP_Info object.

        Args:
            ipInfo (dict): The dict containing IP information.

        Returns:
            Converters._ipInfo: The IP_Info object.
        """
        _ipInfo = self._ipInfo()
        _ipInfo.loc = ipInfo.get("loc")
        _ipInfo.org = ipInfo.get("org")
        _ipInfo.city = ipInfo.get("city")
        _ipInfo.postal = ipInfo.get("postal")
        _ipInfo.region = ipInfo.get("region")
        _ipInfo.country = ipInfo.get("country")
        _ipInfo.hostname = ipInfo.get("hostname")
        _ipInfo.timezone = ipInfo.get("timezone")
        return _ipInfo

    async def requestServer(self, url: str):
        """Requests a server from the API.

        Args:
            url (str): The URL to request.

        Returns:
            dict: The JSON response.
        """
        async with aiohttp.ClientSession() as session, session.get(
            url, headers={"Authorization": f"Bearer {self.key}"}
        ) as response:
            return await response.json(), response.status

    async def requestTopServers(self, data: dict) -> dict:
        """Requests a list of servers from the API.

        Args:
            data (dict): The data to send.

        Returns:
            dict: The JSON response.
        """
        url = "https://backend.mcstalker.com/api/filterservers"
        async with aiohttp.ClientSession() as session, session.post(
            url,
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {self.key}",
            },
            data=json.dumps(data),
        ) as resp:
            return await resp.json(content_type="application/json"), resp.status

    @cached(cache=TTLCache(maxsize=1024, ttl=300))
    async def returnServer(self, ip: str) -> _Server:
        """Returns a Server object.

        Args:
            ip (str): The IP address of the server.

        Returns:
            Converters._Server: The server object.
        """
        response = await self.requestServer(
            f"https://backend.mcstalker.com/api/searchserver/{ip}"
        )
        # response = await response.json()
        status = response[1]
        response = response[0]
        if status == 200:
            server = self.returnServerObject(self.returnCleanServerDict(response))
            return server
        if status == 403:
            raise self.invalidApiKey(response.get("error"))
        raise self.serverNotFound(response.get("error"))

    @cached(cache=TTLCache(maxsize=1024, ttl=300))
    async def returnTopServers(
        self,
        version: int = 756,
        sort: str = "updated",
        ascending: bool = False,
        peopleOnline: bool = True,
        country: str = "all",
        vanilla: bool = False,
        motd: str = "",
        page: int = 1,
    ) -> list:
        """Returns the top servers as per the parameters defined. You can run the function without passing any, it'll return servers as per the recommended options.
        Version: 1.17.1
        Sort: Most recently added.
        Ascending: False
        People Online: True
        Country: All
        Vanilla: False
        Motd: ""
        Page: 1

        Args:
            version (int - Protocol Number, optional): The version a server needs to have to be returned. Defaults to 756 (1.17.1).
            sort (str - "updated/new/empty/top", optional): What kind of servers to find. Defaults to "updated".
            ascending (bool, optional): Whether the results should be in ascending or descending order. Defaults to False.
            peopleOnline (bool, optional): If people have to be online on the server for it to be returned. Defaults to True.
            country (str, optional): The country a server must be located in. Defaults to 'all'.
            vanilla (bool, optional): Whether the server must be vanilla to be returned. Defaults to False.
            motd (str, optional): The MOTD a server must have to be returned. Defaults to "".
            page (int, optional): The page number. Defaults to 1.

        Returns:
            list: A list of Server Objects.
        """
        options = {
            "sortMode": sort,
            "ascdesc": "DESC" if not ascending else "ASC",
            "version": version,
            "country": country,
            "mustHavePeople": peopleOnline,
            "vanillaOnly": vanilla,
            "searchText": motd,
            "page": page,
        }

        # response = await req(
        #     f"{apiURL}filterservers", {"Authorization": self.key, "content-type":"application/json"}, options, "post"
        # )
        response = await self.requestTopServers(options)
        status = response[1]
        response = dict(response[0])
        if status == 200:
            return [
                self.returnServerObject(self.returnCleanServerDict(server))
                for server in response["result"]
            ]
        if status == 403:
            raise self.invalidApiKey(response["error"])
        raise self.serverNotFound(response["error"])
