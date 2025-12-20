import os
import math
import asyncio
import aiohttp
import requests, httpx
import base64
from base64 import b64decode
from pathlib import Path
from json import loads

from .Encoder import encoderjson
from .PostData import method_Shad
from .GetDataMethod import GetDataMethod
from .Clien import clien


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
        self.progressFiles = {}
        self.uploadQueue = type('UploadQueue', (object,), {'next': lambda self, msg: None})()

    def HeaderSendData(self, auth, chunksize_len, fileid, accesshashsend):
        return {
            "access-hash-send": accesshashsend,
            "auth": self.Sh_account if self.Platform == "web" else self.Auth,
            "file-id": str(fileid),
            "chunk-size": str(chunksize_len),
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

    def geSizeFile(self, k=None, databyt_len=None):
        pass

    def uploadFile(self, file: str):
        async def _run_sync_wrapper():
            timeout = aiohttp.ClientTimeout(total=300, connect=20, sock_read=60, sock_connect=20)
            connector = aiohttp.TCPConnector(force_close=True, limit=10)
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                return await self._uploadFile_async(file, session)
        return asyncio.run(_run_sync_wrapper())

    async def _safe_parse_response(self, response: aiohttp.ClientResponse):
        try:
            return await response.json(content_type=None)
        except Exception:
            try:
                text = await response.text()
                return loads(text) if text else {}
            except Exception:
                return {}

    async def _upload_part_async(
        self, session, url, part_number, total_parts, file_id, base_header, file_path, offset, chunk_size
    ):
        with open(file_path, "rb") as f:
            f.seek(offset)
            chunk_data = f.read(chunk_size)

        if not chunk_data:
            return {}

        part_header = base_header.copy()
        part_header["part-number"] = str(part_number)
        part_header["total-part"] = str(total_parts)
        part_header["chunk-size"] = str(len(chunk_data))

        upload_result = None
        for attempt in range(3):
            try:
                async with session.post(url, data=chunk_data, headers=part_header) as response:
                    response.raise_for_status()
                    upload_result = await self._safe_parse_response(response)
                    break
            except Exception:
                await asyncio.sleep(1 * (2 ** attempt))

        if upload_result is None:
            upload_result = {}

        total_size = os.path.getsize(file_path)
        uploaded_size = min(offset + len(chunk_data), total_size)
        self.update_progress(file_id, uploaded_size, total_size, total_parts)

        data = upload_result.get("data") or {}
        if "access_hash_rec" in upload_result and "access_hash_rec" not in data:
            data["access_hash_rec"] = upload_result["access_hash_rec"]

        data["_status"] = upload_result.get("status")
        data["_status_det"] = upload_result.get("status_det")
        return data

    def update_progress(self, file_id, uploaded_size, total_size, total_parts):
        percent = min(100, math.floor(uploaded_size * 100 / (total_size or 1)))
        self.progressFiles[file_id] = {'percent': percent}
        self.uploadQueue.next({
            'file_id': file_id,
            'uploaded_size': uploaded_size,
            'percent': percent,
            'total_size': total_size
        })

    async def _uploadFile_async(self, file: str, session: aiohttp.ClientSession):
        file_id = None
        try:
            req_all = self.requestSendFile(file)
            req = (req_all.get("data") or req_all) or {}

            file_id = req.get("id")
            access_hash_send = req.get("access_hash_send")
            url = req.get("upload_url")

            if not file_id or not access_hash_send or not url:
                raise Exception(f"Init failed: {req_all}")

            file_size = os.path.getsize(file)
            chunk_size = 131072
            total_parts = math.ceil(file_size / chunk_size)

            base_header = self.HeaderSendData(self.Auth, 0, file_id, access_hash_send)

            self.uploadQueue.next({
                'file_id': file_id,
                'uploaded_size': 0,
                'percent': 0,
                'total_size': file_size
            })

            access_hash_rec = None
            reinit_attempts = 0

            i = 0
            while i < total_parts:
                offset = i * chunk_size
                current_chunk_size = min(chunk_size, file_size - offset)

                part_data = await self._upload_part_async(
                    session, url, i + 1, total_parts, file_id, base_header, file, offset, current_chunk_size
                )

                status = part_data.get("_status")
                status_det = part_data.get("_status_det")

                if status == "ERROR_TRY_AGAIN" and reinit_attempts < 3:
                    req_all = self.requestSendFile(file)
                    req = (req_all.get("data") or req_all) or {}
                    file_id = req.get("id")
                    access_hash_send = req.get("access_hash_send")
                    url = req.get("upload_url")
                    base_header = self.HeaderSendData(self.Auth, 0, file_id, access_hash_send)
                    access_hash_rec = None
                    reinit_attempts += 1
                    i = 0
                    continue

                if not access_hash_rec and "access_hash_rec" in part_data:
                    access_hash_rec = part_data["access_hash_rec"]

                i += 1

            if not access_hash_rec:
                access_hash_rec = ""

            if file_id in self.progressFiles:
                del self.progressFiles[file_id]

            self.uploadQueue.next({
                'file_id': file_id,
                'percent': 100,
                'is_done': True,
            })

            return [req, access_hash_rec]

        except Exception as err:
            if file_id and file_id in self.progressFiles:
                del self.progressFiles[file_id]
            raise err
