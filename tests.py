#NEEDS PIP INSTALL CPRINT TO WORK

import MCStalker, asyncio
from cprint import *

allGood = 0


def testApiKeys():
    """Test if the API is working correctly.
    """
    global allGood
    cprint("------------ CURRENTLY TESTING BAD API KEYS ------------\n")
    stats = MCStalker.Stats("balls")
    server = MCStalker.Server("balls")
    player = MCStalker.Player("balls")

    asyncio.run(stats.returnStats())
    cprint.ok("STATS CHECK SUCCESSFUL (1/4)")
    allGood += 1

    try:
        asyncio.run(server.returnServer("46.228.199.189"))
    except MCStalker.MCStalker.invalidApiKey:
        allGood += 1
        cprint.ok("SERVER CHECK SUCCESSFUL (2/4)")

    try:
        asyncio.run(server.returnTopServers())
    except MCStalker.MCStalker.invalidApiKey:
        allGood += 1
        cprint.ok("TOP SERVERS CHECK SUCCESSFUL (3/4)")

    try:
        asyncio.run(player.returnPlayer("TheOnlyWayUp"))
    except MCStalker.MCStalker.invalidApiKey:
        allGood += 1
        cprint.ok("PLAYER CHECK SUCCESSFUL (4/4)")

    cprint("\n------------ FINISHED TESTING BAD API KEYS ------------")


def testSearches():
    """Test if the API is working correctly.
    """
    global allGood
    cprint("\n\n------------ CURRENTLY TESTING SEARCHES ------------\n")
    key = input("Enter your API Key: ")

    stats = MCStalker.Stats(key)
    server = MCStalker.Server(key)
    player = MCStalker.Player(key)

    try:
        asyncio.run(stats.returnStats())
        allGood += 1
        cprint.ok("STATS CHECK SUCCESSFUL (1/4)")
    except Exception as e:
        raise e

    try:
        asyncio.run(server.returnServer("46.228.199.189"))
        allGood += 1
        cprint.ok("SERVER CHECK SUCCESSFUL (2/4)")
    except Exception as e:
        raise e

    try:
        asyncio.run(server.returnTopServers())
        allGood += 1
        cprint.ok("TOP SERVERS CHECK SUCCESSFUL (3/4)")
    except Exception as e:
        raise e

    try:
        asyncio.run(player.returnPlayer("TheOnlyWayUp"))
        allGood += 1
        cprint.ok("PLAYER CHECK SUCCESSFUL (4/4)")
    except Exception as e:
        raise e

    cprint("\n------------ FINISHED TESTING SEARCHES ----------------")


testApiKeys()
cprint.warn("\n\nSleeping 5 seconds to prevent cloudflare from kicking my ass.\n")
asyncio.run(asyncio.sleep(5))
testSearches()

if allGood == 8:
    cprint.info("Everything is working correctly.")
else:
    cprint.fatal("Not all endpoints are working correctly.", interrupt=False)