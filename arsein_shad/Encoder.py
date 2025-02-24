import base64
import io
import json
import random
import re
import secrets
import string
from base64 import b64decode
from json import JSONDecoder, loads

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad, unpad
from PIL import Image

from .Error import AuthError


class encoderjson:
    def __init__(self, auth: str, private_key: str = None):
        self.auth = auth
        self.key = bytearray(self.createSecretPassphrase(auth), "UTF-8")
        self.iv = bytearray.fromhex("0" * 32)
        if private_key:
            self.keypair = RSA.import_key(private_key.encode("utf-8"))

    def changeAuthType(auth_dec):
        n = ""
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = lowercase.upper()
        digits = "0123456789"
        for s in auth_dec:
            if s in lowercase:
                n += chr(((32 - (ord(s) - 97)) % 26) + 97)
            elif s in uppercase:
                n += chr(((29 - (ord(s) - 65)) % 26) + 65)
            elif s in digits:
                n += chr(((13 - (ord(s) - 48)) % 10) + 48)
            else:
                n += s
        return n

    def decodeAuthType(auth_enc):
        n = ""
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = lowercase.upper()
        digits = "0123456789"
        for s in auth_enc:
            if s in lowercase:
                n += chr(((32 - (ord(s) - 97)) % 26) + 97)
            elif s in uppercase:
                n += chr(((29 - (ord(s) - 65)) % 26) + 65)
            elif s in digits:
                n += chr(((13 - (ord(s) - 48)) % 10) + 48)
            else:
                n += s
        return n

    def createSecretPassphrase(self, e):
        t, i = e[0:8], e[8:16]
        n = e[16:24] + t + e[24:32] + i

        for s in range(len(n)):
            e = n[s]
            if e >= "0" and e <= "9":
                t = chr(((ord(e) - ord("0") + 5) % 10) + ord("0"))
                n = n[:s] + t + n[s + 1 :]
            else:
                t = chr(((ord(e) - ord("a") + 9) % 26) + ord("a"))
                n = n[:s] + t + n[s + 1 :]
        return n

    def encrypt(self, text):
        try:
            encode_data = base64.b64encode(
                AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(
                    pad(text.encode("UTF-8"), AES.block_size)
                )
            ).decode("UTF-8")
            return encode_data
        except:
            raise

    def decrypt(self, text):
        try:
            decode_data = unpad(
                AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(
                    base64.urlsafe_b64decode(text.encode("UTF-8"))
                ),
                AES.block_size,
            ).decode("UTF-8")
            return decode_data
        except ValueError:
            raise AuthError(
                "Check your auth This auth is not the key to decrypt and encrypt data"
            )

    def makeSignFromData(self, data_enc: str):
        sha_data = SHA256.new(data_enc.encode("utf-8"))
        signature = pkcs1_15.new(self.keypair).sign(sha_data)
        return base64.b64encode(signature).decode("utf-8")

    def decryptRsaOaep(private: str, data_enc: str):
        keyPair = RSA.import_key(private.encode("utf-8"))
        return (
            PKCS1_OAEP.new(keyPair).decrypt(base64.b64decode(data_enc)).decode("utf-8")
        )

    def encryptRsaOaep(private: str, data_enc: str):
        keyPair = RSA.import_key(private.encode("utf-8"))
        return (
            PKCS1_OAEP.new(keyPair).encrypt(base64.b64encode(data_enc)).decode("utf-8")
        )

    def rsaKeyGenerate():
        keyPair = RSA.generate(1024)
        public = encoderjson.changeAuthType(
            base64.b64encode(keyPair.publickey().export_key()).decode("utf-8")
        )
        private = keyPair.export_key().decode("utf-8")
        return [public, private]


def getThumbInline(image_bytes: bytes):
    im = Image.open(io.BytesIO(image_bytes))
    width, height = im.size
    if height > width:
        new_height = 40
        new_width = round(new_height * width / height)
    else:
        new_width = 40
        new_height = round(new_width * height / width)
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
    changed_image = io.BytesIO()
    im.save(changed_image, format="PNG")
    changed_image = changed_image.getvalue()
    return base64.b64encode(changed_image)
