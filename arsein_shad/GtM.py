import asyncio

import httpx
import nest_asyncio

from .Error import ErrorServer
from .GetDataMethod import GetDataMethod

list_servers, reoeatchoice_server, repeat = [], 0, 0

nest_asyncio.apply()


def Server_Shad():
    while 1:
        try:
            for server_rubika in range(1):

                async def GETservers(server):
                    Retry = httpx.AsyncHTTPTransport(retries=5)
                    async with httpx.AsyncClient(
                        transport=Retry, http2=True, timeout=1.0
                    ) as client:
                        response = await client.get(url=server)
                        return response.json()

                for added in range(1):
                    servers = (
                        asyncio.run(GETservers("https://shgetdcmess.iranlms.ir/"))
                        .get("data")
                        .get("API")
                        .values()
                    )
                    list_servers.extend(servers)
                    list_servers.pop(1)
            break
        except httpx.ConnectError:
            raise ErrorServer("Please check your is not internet")
        except:
            continue


def defaultapi():
    global list_servers, reoeatchoice_server, repeat
    while 1:
        try:
            for tekrar in range(1):
                if len(list_servers) == 0:
                    reoeatchoice_server = 0
                    req = GetDataMethod(target=Server_Shad, args=()).show()
                    if req:
                        continue
                elif len(list_servers) == 138:
                    if reoeatchoice_server < 138:
                        reoeatchoice_server += 1
                        repeat = reoeatchoice_server - 1
                        return list_servers[repeat]
                    elif reoeatchoice_server == 138:
                        list_servers, reoeatchoice_server, repeat = [], 0, 0
                        continue
        except:
            continue
