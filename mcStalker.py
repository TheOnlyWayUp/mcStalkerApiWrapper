from datetime import timedelta
from ratelimit import limits
import asyncio, aiohttp, logging, json

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

""" 
TO DO
- Add better ratelimiting
- Test logging
- Make qServer work with API Key

"""

try:
    log.debug(
        "======================= MCStalker's API Wrapper has successfully begun to run ======================="
    )
except:
    pass


def addLog(type="debug", content="None"):
    if type == "debug":
        log.debug(content)
    elif type == "info":
        log.info(content)
    elif type == "warning":
        log.warning(content)
    elif type == "error":
        log.error(content)
    elif type == "critical":
        log.critical(content)


async def req(url, headers, data=None, method="get"):
    async with aiohttp.ClientSession() as session:
        if method == "get":
            async with session.get(url, headers=headers, data=data) as response:
                return await response.json()
        elif method == "post":
            async with session.post(url, headers=headers, data=data) as response:
                return await response.json(content_type="text/html")


async def qServer(data):
    url = "https://backend.mcstalker.com/api/filterservers"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, headers={"content-type": "application/json"}, data=json.dumps(data)
        ) as resp:
            return await resp.json()

    #  async with aiohttp.ClientSession() as session:
    #          async with session.post(url, data=d2) as resp:
    #                  print(resp)


# @limits(calls=2, period=timedelta(seconds=1).total_seconds())
# async def get_foobar():
#     response = await req('https://httpbin.org/get')
#     response.raise_for_status()
#     return response.json()


class Converters:
    class _ipInfo:
        loc = None
        org = None
        city = None
        postal = None
        region = None
        country = None
        hostname = None
        timezone = None

    class _Server:
        """The _Server object, which is used to generate information about a server. Please read the docs for Server() instead."""

        ip = ""
        favicon = ""
        hostname = None
        players = []
        slots = {"online": None, "max": None}
        motd = ""
        added = ""
        lastPinged = ""
        vanilla = bool
        ipInfo = dict
        raw = ""

    class _Player:
        """The _Player object, which is used to generate information about a player. Please read the docs for Player() instead."""

        name = ""
        uuid = ""
        raw = ""


apiURL = "https://backend.mcstalker.com/api/"


def returnCleanServerDict(server: dict):
    print(server)
    _server = {
        "ip": server.get("ip"),
        "favicon": server.get("favicon"),
        "hostname": server.get("ipInfo").get("hostname"),
        "players": server.get("players"),
        "version": server.get("versionName"),
        "slots": {"online": server["online"], "max": server["max"]},
        "motd": server["motd"]
        if type(server["motd"]) is str
        else server["motd"]["text"]
        if server["motd"]["text"] != ""
        else server["motd"]["extra"],
        "authStatus": server.get("authStatus"),
        "alive": server.get("alive"),
        "vanilla": server.get("vanilla"),
        "addedAt": server.get("createdAt"),
        "lastPinged": server.get("updatedAt"),
        "ipInfo": server.get("ipInfo"),
    }
    # del _server['ipInfo']['hostname']
    return _server


def eKeyError(code):
    try:
        exec(code)
    except KeyError:
        pass


def returnIP_Info(ipInfo: dict):
    """Converts a dictionary to an IP_Info object.

    Args:
        ipInfo (dict): The dict containing IP information.

    Returns:
        Converters._ipInfo: The IP_Info object.
    """
    _ipInfo = Converters._ipInfo()
    _ipInfo.loc = ipInfo.get("loc")
    _ipInfo.org = ipInfo.get("org")
    _ipInfo.city = ipInfo.get("city")
    _ipInfo.postal = ipInfo.get("postal")
    _ipInfo.region = ipInfo.get("region")
    _ipInfo.country = ipInfo.get("country")
    _ipInfo.hostname = ipInfo.get("hostname")
    _ipInfo.timezone = ipInfo.get("timezone")
    return _ipInfo


def returnServer(server: dict):
    """Converts a dictionary to a Server object.

    Args:
        server (dict): The dict containing server information.

    Returns:
        Converters._Server: The server object.
    """
    server = returnCleanServerDict(server)
    _server = Converters._Server()
    _server.ip = server.get("ip")
    _server.favicon = server.get("favicon")
    _server.hostname = server.get("hostname")
    try:
        _server.players = [returnPlayer(player) for player in server["players"]]
    except TypeError:
        _server.players = []
    _server.slots = server.get("slots")
    _server.motd = server.get("motd")
    _server.added = server.get("addedAt")
    _server.lastPinged = server.get("lastPinged")
    _server.vanilla = server.get("vanilla")
    _server.ipInfo = returnIP_Info(server["ipInfo"])
    _server.raw = server
    return _server

    # _server.favicon = server["favicon"]
    # _server.hostname = server["hostname"]
    # _server.players = [returnPlayer(player) for player in server["players"]]
    # _server.slots = server["slots"]
    # _server.motd = server["motd"]
    # _server.added = server["addedAt"]
    # _server.lastPinged = server["lastPinged"]
    # _server.vanilla = server["vanilla"]
    # _server.ipInfo = returnIP_Info(server["ipInfo"])
    # _server.raw = server
    # return _server


def returnPlayer(player: dict):
    _player = Converters._Player()
    _player.name = player["username"]
    _player.uuid = player["uuid"]
    _player.raw = player
    return _player


class Errors:
    class invalidApiKey(Exception):
        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Invalid API Key - {0} ".format(self.message)

    class requestError(Exception):
        def __init__(self, *args):
            self.message = args[0]

        def __str__(self):
            return "Error sending the request - {0} ".format(self.message)


Errors = Errors()


class Server:
    def __init__(self, key):
        """Initialising the Server() class.

        Args:
            key (str): The API key to use.
        """
        asyncio.run(self.init(key))

    async def init(self, key):
        """This is not for users to use. It is for the API wrapper. Ignore and move on."""
        self.key = key
        # r = await req(f"{apiURL}tokenCheck", {"Authorization": self.key})
        # if not r["success"]:
        #     addLog(type="critical", content="[SERVER] [ERROR] - API Key is incorrect.")
        #     raise Errors.invalidAPI_Key(
        #         f"Your API Key ({self.key}) was incorrect, please check if you have internet and are not being ratelimited. You can generate an API key at https://mcstalker.com/register."
        #     )

    @limits(calls=2, period=timedelta(seconds=1).total_seconds())
    async def returnServer(self, ip: str):
        """Returns a Server object.

        Args:
            ip (str): The IP address of the server.

        Returns:
            Converters._Server: The server object.
        """
        response = await req(f"{apiURL}searchserver/{ip}", {"Authorization": self.key})
        # response = await response.json()
        if "error" not in response:
            return returnServer(response)
        addLog(
            "error",
            f"[CLIENT] [ERROR] returnServer() has failed for {ip} - {response['error']}",
        )
        return Errors.requestError(response["error"])

    @limits(calls=2, period=timedelta(seconds=1).total_seconds())
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
    ):
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
        response = dict(await qServer(options))
        if "error" not in response.keys():
            return [returnServer(server) for server in response["result"]]
        addLog(
            "error",
            f"[CLIENT] [ERROR] returnTopServers() has failed - {response['error']}",
        )
        return Errors.requestError(response["error"])


# x = {"ip": "ip here", "favicon": "favicon here", "hostname": "hostname here", "players": ["name", "name2"], "slots": {"online": "how many online", "max": "how many max"}, "motd": "motd here (clean)", "added": "when server was added, unix", "lastPinged": "when it was last pinged, unix", "vanilla": true, "country": {"country": "country here", "location": "location here", "origin": "origin here", "city": "city here", "postal": "postal here", "region": "region here", "timezone": "timezone here"}}
