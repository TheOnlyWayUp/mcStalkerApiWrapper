from datetime import timedelta
from ratelimit import limits
import asyncio, aiohttp, logging

logging.basicConfig(
    filename="newfile.log", format="%(asctime)s %(message)s", filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.debug(
    "======================= MCStalker's API Wrapper has successfully begun to run ======================="
)


async def req(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


# @limits(calls=2, period=timedelta(seconds=1).total_seconds())
# async def get_foobar():
#     response = await req('https://httpbin.org/get')
#     response.raise_for_status()
#     return response.json()


class Converters:
    class _Server:
        ip = ""
        favicon = ""
        hostname = None
        players = []
        slots = {"online": None, "max": None}
        motd = ""
        added = ""
        lastPinged = ""
        vanilla = bool
        country = {
            "country": None,
            "location": None,
            "origin": None,
            "city": None,
            "postal": None,
            "region": None,
            "timezone": None,
        }

    class _Player:
        name = ""
        seenOn = {}  # Server object -> time


def returnServer(server: dict):
    _server = Converters._Server()
    _server.ip = server["ip"]
    _server.favicon = server["favicon"]
    _server.hostname = server["hostname"]
    _server.players = server["players"]
    _server.slots = server["slots"]
    _server.motd = server["motd"]
    _server.added = server["added"]
    _server.lastPinged = server["lastPinged"]
    _server.vanilla = server["vanilla"]
    _server.country = server["country"]
    return _server


class Errors:
    logger.debug("[CLIENT] [INFOR] The Error() class has been initialised.")

    class invalidAPI_Key(Exception):
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
    async def __init__(self, key):
        logger.debug("[CLIENT] [INFOR] The Server() class was initialised.")
        self.key = key
        r = await req(
            "backend.mcstalker.com/api/tokenCheck/", {"Authorization": self.key}
        )
        if not r["success"]:
            logger.critical("[SERVER] [ERROR] - API Key is incorrect.")
            raise Errors.invalidAPI_Key(
                f"Your API Key ({self.key}) was incorrect, please check if you have internet and are not being ratelimited. You can generate an API key at https://mcstalker.com/register."
            )

    @limits(calls=2, period=timedelta(seconds=1).total_seconds())
    async def returnServer(self, ip: str):
        response = await req(
            "backend.mcstalker.com/api/server/" + ip, {"Authorization": self.key}
        )
        response = await response.json()
        if response["success"]:
            logger.debug(f"[CLIENT] [INFOR] returnServer() was sucessful for {ip}.")
            return returnServer(response["data"])
        logger.error(
            f"[CLIENT] [ERROR] returnServer() has failed for {ip} - {response['message']}"
        )
        return Errors.requestError(response["message"])

    @limits(calls=2, period=timedelta(seconds=1).total_seconds())
    async def returnTopServers(self):
        response = await req(
            "backend.mcstalker.com/api/topServers/", {"Authorization": self.key}
        )
        response = await response.json()
        if response["success"]:
            logger.debug(f"[CLIENT] [INFOR] returnTopServers() was sucessful.")
            return [returnServer(server["data"]) for server in response["data"]]
        logger.error(
            f"[CLIENT] [ERROR] returnTopServers() has failed - {response['message']}"
        )
        return Errors.requestError(response["message"])


# x = {"ip": "ip here", "favicon": "favicon here", "hostname": "hostname here", "players": ["name", "name2"], "slots": {"online": "how many online", "max": "how many max"}, "motd": "motd here (clean)", "added": "when server was added, unix", "lastPinged": "when it was last pinged, unix", "vanilla": true, "country": {"country": "country here", "location": "location here", "origin": "origin here", "city": "city here", "postal": "postal here", "region": "region here", "timezone": "timezone here"}}
