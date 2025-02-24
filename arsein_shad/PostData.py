import asyncio
import base64
import io
import sys
from base64 import b64decode
from json import JSONDecodeError, dumps, loads
from random import choice, choices, randint

import aiohttp
import httpx

from .Clien import clien
from .Device import DeviceTelephone
from .Encoder import encoderjson
from .Error import AuthError, ErrorPrivatyKey, ErrorServer
from .ErrorShad import ErrorShad
from .GetDataMethod import GetDataMethod
from .GtM import defaultapi


async def http(
    plat: str = None,
    js: dict = None,
    OrginalAuth: str = None,
    auth: str = None,
    key: str = None,
    api_version: str = "6",
):
    enc, Enc = encoderjson(auth, key), encoderjson(OrginalAuth, key)
    Retry = httpx.AsyncHTTPTransport(retries=1)
    if plat == "web":
        async with httpx.AsyncClient(transport=Retry, http2=True, timeout=20) as client:
            servers = GetDataMethod(target=defaultapi, args=()).show()
            response = await client.post(
                servers,
                data=dumps(
                    {
                        "api_version": (
                            api_version if api_version != "6" else api_version
                        ),
                        "auth": OrginalAuth,
                        "data_enc": enc.encrypt(dumps(js)),
                        "sign": enc.makeSignFromData(enc.encrypt(dumps(js))),
                    }
                ),
                headers={
                    "Referer": "https://web.shad.ir/",
                    "Content-Type": "application/json; charset=utf-8",
                },
            )
            return response.text

    elif plat == "android":
        async with httpx.AsyncClient(transport=Retry, http2=True, timeout=20) as client:
            servers = GetDataMethod(target=defaultapi, args=()).show()
            response = await client.post(
                servers,
                data=dumps(
                    {
                        "api_version": (
                            api_version if api_version != "6" else api_version
                        ),
                        "auth": auth,
                        "data_enc": Enc.encrypt(dumps(js)),
                        "sign": enc.makeSignFromData(Enc.encrypt(dumps(js))),
                    }
                ),
            )
            return response.text


async def httpfiles(serversfile: str, dade, head: dict):
    Retry = httpx.AsyncHTTPTransport(retries=5)
    async with httpx.AsyncClient(transport=Retry, http2=True, timeout=20) as client:
        response = await client.post(serversfile, data=dade, headers=head)
        return response.text


async def httplogin(auths: str, js: dict):
    Retry = httpx.AsyncHTTPTransport(retries=5)
    servers = defaultapi()
    async with httpx.AsyncClient(transport=Retry, http2=True, timeout=20) as client:
        enc = encoderjson(auth=auths)
        response = await client.post(
            servers,
            data=dumps(
                {
                    "api_version": "6",
                    "tmp_session": auths,
                    "data_enc": enc.encrypt(dumps(js)),
                }
            ),
        )
        return response.text


async def download(
    auth: str, dc_id: str, fileID: str, size: str, accessHashRec: str, chunk_size=131072
):
    header: dict = {
        "auth": auth,
        "file-id": str(fileID),
        "start-index": "0",
        "last-index": str(size),
        "access-hash-rec": accessHashRec,
        "Content-Type": "text/plain",
    }
    serverDownload: str = f"https://shst{dc_id}.iranlms.ir/GetFile.ashx"
    done = False
    stream = io.BytesIO()

    Retry = httpx.AsyncHTTPTransport(retries=5)
    async with httpx.AsyncClient(transport=Retry, http2=True, timeout=20) as client:
        while not done:
            try:
                if int(size) <= chunk_size:
                    response = await client.get(url=serverDownload, headers=header)
                    stream.write(response.content)
                    done = True
                else:
                    if 0 <= chunk_size:
                        response = await client.get(url=serverDownload, headers=header)
                        stream.write(response.content)
                        done = True
                    else:
                        for i in range(0, int(size), chunk_size):
                            (
                                header["start-index"],
                                header["last-index"],
                            ) = str(i), (
                                str(i + chunk_size)
                                if i + chunk_size <= int(size)
                                else str(size)
                            )
                        response = await client.get(url=serverDownload, headers=header)
                        stream.write(response.content)
                        done = True
            except Exception as error:
                print(error)
                continue
    if stream.tell() > 0:
        stream.seek(0)
        return [stream.getvalue(), done]


class method_Shad:
    def __init__(
        self,
        plat: str = None,
        OrginalAuth: str = None,
        auth: str = None,
        keyAccount: str = None,
    ):
        self.Plat = plat
        self.Auth = auth
        self.OrginalAuth = OrginalAuth
        self.keyAccount = keyAccount
        if not keyAccount == None:
            self.enc = (
                encoderjson(self.Auth, self.keyAccount)
                if plat == "web"
                else encoderjson(self.OrginalAuth, self.keyAccount)
            )

    def methodsShad(
        self,
        types: str = None,
        methode: str = None,
        indata: dict = None,
        wn: dict = None,
        downloads: list = None,
        server: str = None,
        podata: bin = None,
        header: dict = None,
    ):
        self.Type: str = types
        self.inData: dict = {"method": methode, "input": indata, "client": wn}
        self.download: list = downloads
        self.serverfile: str = str(server)
        self.datafile: bin = podata
        self.headerfile: dict = header

        while 1:
            try:
                for senddata in range(1):
                    if self.Type == "json":
                        sendJS: dict = loads(
                            self.enc.decrypt(
                                loads(
                                    asyncio.run(
                                        http(
                                            plat=self.Plat,
                                            js=self.inData,
                                            OrginalAuth=self.OrginalAuth,
                                            auth=self.Auth,
                                            key=self.keyAccount,
                                        )
                                    )
                                ).get("data_enc")
                            )
                        )
                        if sendJS.get("status") != "OK":
                            stat = ErrorShad(sendJS).Error
                            if stat == "re":
                                return ErrorShad(sendJS).state
                            elif stat == "ra":
                                ErrorShad(sendJS)
                        else:
                            return sendJS

                    elif self.Type == "file":
                        sendFILE = asyncio.run(
                            httpfiles(
                                serversfile=self.serverfile,
                                dade=self.datafile,
                                head=self.headerfile,
                            )
                        )
                        return sendFILE

                    elif self.Type == "login":
                        authrnd = encoderjson.changeAuthType(
                            "".join(choices("abcdefghijklmnopqrstuvwxyz", k=32))
                        )
                        self.enc = encoderjson(auth=authrnd)
                        sendLOGIN: dict = loads(
                            self.enc.decrypt(
                                loads(
                                    asyncio.run(
                                        httplogin(auths=authrnd, js=self.inData)
                                    )
                                ).get("data_enc")
                            )
                        )
                        if sendLOGIN.get("status") != "OK":
                            stat = ErrorShad(sendLOGIN).Error
                            if stat == "re":
                                return ErrorShad(sendLOGIN).state
                            elif stat == "ra":
                                ErrorShad(sendLOGIN)
                        else:
                            return sendLOGIN

                    elif self.Type == "download":
                        sendDOWNLOAD = asyncio.run(
                            download(
                                auth=self.download[0],
                                dc_id=self.download[1],
                                fileID=self.download[2],
                                size=self.download[3],
                                accessHashRec=self.download[4],
                            )
                        )

                        return sendDOWNLOAD
            except JSONDecodeError:
                continue
            except httpx.ConnectError or httpx.HTTPError:
                continue
            except httpx.TimeoutException:
                continue
