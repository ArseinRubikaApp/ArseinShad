import aiohttp
import asyncio
import requests, httpx
import os
import base64

from .Encoder import encoderjson
from .PostData import method_Shad
from .GetDataMethod import GetDataMethod
from .Clien import clien
from json import loads
from pathlib import Path
from base64 import b64decode


class Upload:
    def __init__(self, plat: str, OrginalAuth: str, Sh_account: str, keyAccount: str):
        self.Auth = OrginalAuth
        self.Sh_account = Sh_account
        self.enc = (
            encoderjson(self.Sh_account, keyAccount)
            if plat == "web"
            else encoderjson(self.Auth, keyAccount)
        )
        self.methodUpload = method_Shad(
            plat=plat,
            OrginalAuth=self.Auth,
            auth=self.Sh_account,
            keyAccount=keyAccount,
        )
        self.cli = clien(plat).platform
        self.Platform = plat

    def HeaderSendData(self, auth, chunksize, fileid, accesshashsend):
        return {
            "access-hash-send": accesshashsend,
            "auth": self.Sh_account if self.Platform == "web" else self.Auth,
            "file-id": str(fileid),
            "chunk-size": str(len(chunksize)),
        }

    def requestSendFile(self, addressfile):
        return GetDataMethod(
            target=self.methodUpload.methodsShad,
            args=(
                "json",
                "requestSendFile",
                {
                    "file_name": os.path.basename(addressfile),
                    "size": os.path.getsize(addressfile),
                    "mime": os.path.splitext(addressfile)[1].strip("."),
                },
                self.cli,
            ),
        ).show()

    def geSizeFile(self, k=None, databyt=None):
        meghdaruploud = str(round(k / 1024) / 1000)
        meghdarfile = str(round(len(databyt) / 1024) / 1000)
        if len(meghdaruploud) < 4:
            megh = f"{meghdaruploud} KB"
        elif len(meghdaruploud) < 7:
            megh = f"{meghdaruploud} MB"
        elif len(meghdaruploud) < 10:
            megh = f"{meghdaruploud} GB"
        elif len(meghdarfile) < 4:
            megh1 = f"{meghdarfile} KB"
        elif len(meghdarfile) < 7:
            megh1 = f"{meghdarfile} MB"
        elif len(meghdarfile) < 10:
            megh1 = f"{meghdarfile} GB"
        print(f"{megh} / {megh1}")

    def uploadFile(self, file: str):
        try:
            req = self.requestSendFile(file)["data"]
            databyt: bin = open(file, "rb").read()
            ids = req["id"]
            dc_id = req["dc_id"]
            access_hash_send = req["access_hash_send"]
            url = req["upload_url"]
            header = self.HeaderSendData(self.Auth, databyt, ids, access_hash_send)
            if len(databyt) <= 131072:
                header["part-number"], header["total-part"] = "1", "1"
                while True:
                    try:
                        j = self.methodUpload.methodsShad(
                            types="file", server=url, podata=databyt, header=header
                        )
                        j = loads(j)["data"]["access_hash_rec"]
                        break
                    except:
                        continue
                return [req, j]
            else:
                t = len(databyt) // 131072 + 1
                for i in range(1, t + 1):
                    if i != t:
                        k = (i - 1) * 131072
                        (
                            header["chunk-size"],
                            header["part-number"],
                            header["total-part"],
                        ) = ("131072", str(i), str(t))
                        while True:
                            try:
                                j = self.methodUpload.methodsShad(
                                    types="file",
                                    server=url,
                                    podata=databyt[k : k + 131072],
                                    header=header,
                                )
                                j = loads(j)["data"]
                                break
                            except:
                                continue
                    else:
                        k = (i - 1) * 131072
                        (
                            header["chunk-size"],
                            header["part-number"],
                            header["total-part"],
                        ) = (str(len(databyt[k:])), str(i), str(t))
                        while True:
                            try:
                                p = self.methodUpload.methodsShad(
                                    types="file",
                                    server=url,
                                    podata=databyt[k:],
                                    header=header,
                                )
                                p = loads(p)["data"]["access_hash_rec"]
                                break
                            except:
                                continue
                return [req, p]
        except Exception as err:
            print("methodUpload: ", err)
