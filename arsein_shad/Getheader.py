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
            async with aiohttp.ClientSession() as session:
                return await self._uploadFile_async(file, session)

        return asyncio.run(_run_sync_wrapper())
        

    async def _upload_part_async(
        self, session, url, part_number, total_parts, file_id, base_header, file_path, offset, chunk_size
    ):
        
        with open(file_path, "rb") as f:
            f.seek(offset)
            chunk_data = f.read(chunk_size)
        
        if not chunk_data:
            return {"error": "No data read for chunk"}

        part_header = base_header.copy()
        part_header["part-number"] = str(part_number)
        part_header["total-part"] = str(total_parts)
        part_header["chunk-size"] = str(len(chunk_data))

        while True:
            try:
                async with session.post(url, data=chunk_data, headers=part_header) as response:
                    response.raise_for_status()
                    
                    response_text = await response.text()
                    json_data = loads(response_text)
                    
                    self.update_progress(file_id, offset + len(chunk_data), os.path.getsize(file_path), total_parts)
                    
                    return json_data.get("data", {})
            except Exception as e:
                await asyncio.sleep(1) 


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
            
            req = self.requestSendFile(file)["data"]
            
            file_id = req["id"]
            access_hash_send = req["access_hash_send"]
            url = req["upload_url"]
            
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

            
            tasks = []
            for i in range(total_parts):
                offset = i * chunk_size
                current_chunk_size = min(chunk_size, file_size - offset)
                
                tasks.append(
                    self._upload_part_async(
                        session, url, i + 1, total_parts, file_id, base_header, file, offset, current_chunk_size
                    )
                )

            
            results = await asyncio.gather(*tasks)

            
            last_part_data = results[-1]
            access_hash_rec = last_part_data.get("access_hash_rec")
            
            if not access_hash_rec:
                raise Exception("Final Access Hash not received or upload failed.")
            
            
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
