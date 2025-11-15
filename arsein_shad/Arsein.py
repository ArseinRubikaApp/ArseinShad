import asyncio
import base64
import datetime
import io
import os
from base64 import b64decode
from json import dump, loads
from random import choice, randint
from re import findall

import aiohttp
import httpx
import mutagen
import tinytag
from mutagen.mp3 import MP3
from PIL import Image
from tinytag import TinyTag

from .Clien import clien
from .Copyright import copyright
from .Device import DeviceTelephone
from .Encoder import encoderjson, getThumbInline
from .Error import AuthError, ErrorMethod, ErrorPrivatyKey, TypeMethodError
from .GetDataMethod import GetDataMethod
from .Getheader import Upload
from .PostData import method_Shad
from .TypeText import TypeText, deleteRSAset, makeJsonResend


class Messenger:
    def __init__(self, Sh_account: str, keyAccount: str, TypePlat=None):
        keyAccount, Sh_account = deleteRSAset(keyAccount), "".join(
            findall(r"\w{32}", Sh_account)
        )
        self.keyUser, status_platform = keyAccount, ""

        # check Auth Account
        if Sh_account.__len__() != 32:
            raise AuthError("The Auth entered is incorrect")

        # check PrivatyKey Account
        if self.keyUser[:3] == "eyJ" or str(TypePlat) in ("web"):
            status_platform = "web"
            self.cli = clien("web").platform
            self.keyUser = (
                loads(b64decode(self.keyUser).decode("utf-8"))["d"]
                if self.keyUser[:3] == "eyJ"
                else f"-----BEGIN RSA PRIVATE KEY-----\n{self.keyUser}\n-----END RSA PRIVATE KEY-----"
            )

        elif self.keyUser[:3] == "MII" or str(TypePlat) in ("android"):
            status_platform = "android"
            self.cli = clien("android").platform
            self.keyUser = f"-----BEGIN RSA PRIVATE KEY-----\n{self.keyUser}\n-----END RSA PRIVATE KEY-----"
        elif not "android" or "web" in status_platform:
            raise ErrorPrivatyKey("Your account private key is incorrect")

        # get Data
        self.CopyRight = copyright.CopyRight
        self.Auth = encoderjson.changeAuthType(Sh_account)
        self.OrginalAuth = Sh_account
        self.TypePlatform = status_platform
        self.methods = method_Shad(
            plat=status_platform,
            OrginalAuth=Sh_account,
            auth=self.Auth,
            keyAccount=self.keyUser,
        )
        self.Upload = Upload(status_platform, self.OrginalAuth, self.Auth, self.keyUser)

    def __repr__(self):
        return f"Auth your Account: {self.Auth} and PrivateKey: {self.keyUser.replace('-----BEGIN RSA PRIVATE KEY-----','').replace('-----END RSA PRIVATE KEY-----','')[:50]} ...."

    @property
    def thumb_inline(self):
        return "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD/2wBDAQMDAwQDBAgEBAgQCwkLEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBD/wAARCAAoACgDASIAAhEBAxEB/8QAGwAAAgMAAwAAAAAAAAAAAAAAAAYFBwgDBAn/xAAwEAACAQIGAQMCAwkAAAAAAAABAgMEEQAFBhIhMUEHE3EUIlFhkQgVFiMyM0Jigf/EABkBAAMBAQEAAAAAAAAAAAAAAAMEBgUHAv/EACgRAAEDBAECBQUAAAAAAAAAAAECAwQABREhMRITBhQiQVFhcYHR4f/aAAwDAQACEQMRAD8AwbTZfWVtTAqQ+/UysIY5IjuknZjZVN+x46ueicSNVpSfL82lyiqoHpamnmaGancfzIZASpRierHi3jDDlGXVMczstVHKJEMW6MhlZQw7BF+bcLx+PfBe8n0IlfmzQmmnhBb74pUZXQ+Q265/Un/mOwRbUme2XFjOd5P7rmEq9mMvpBqo0yB1QqYTu2t45HBHzjqzZHtJkWIC4II8gkfrjZlN6SJNlsJFHAWipmpw306glWJJJNuWuT9x56wg6m9GK/J44s6r9OZt+6JX9v6iKmdEkJuAqSFdhNx1zexx7assNPo9/b70NV8kq9SuKy1U5a0IcbCQwt0eOcGH6v0e8NTJT1jLTzBtghljbeWvb+m3jyfGDGNKsyQ6QAK1o92y2CVU4adpkqpqeigp6yovKiq6Q+y+7cPF/uubfHHk41v6XZBoLMKHW2Z6vqa6rziXN6GnoKmtljkzP25A5dgjSBGJcRh5LttUkg3xh7LtTVEdSk1PGI3G11kV2uF/xC36HfycXB6e+r2b5RUy7MxZTUywyzlrMXeJt8bXPN1bkfnilYQ4/C7KF4OsEa0CDz9QPzUrIR5eX3lpyMHIO+RjjjVeiesH9LtNZZJU6Y0jpfMDDKYAgryysnQIjV7k7gwLmwAseb4rH9oXVGmMs0FDkeTakptv8SU5TL8srWkjSlSkR5AkPuOoVagtY+XuRioq71f1HLQzU/1btup5nlU2O6Ocgy3/ACcgE/GKY1x6qZxnMS0NZmkslPFUvVogbhJnsHkH+x2rc/kMKQPDrjDrbz689Jzsk5+Of5zRZd6TLbWyyjHUMaAGPnjdLnqbmVLX6uzWqpq7MJIWqOUkAp5VIFjzawta1rDxcYMJeo85q2naumLVX1ckh92oJcSk9sSSCzG/XBvyfABgVzda8waPAjL7Aqu6HOmiXaztZQdv3Ec/OJKj1C8NikpBwYMT0Oe+GE4NVcuGyp45FT7a0rhFvNfNveIKT7h66t8cY4J9XUs+VvTVFKDVtMrLWGVrpEAQU9vprmx3Hni3nBgw09eJYWE9WsChN2qKnYTS9V1T1E7KjRyOwvGZD/cXwF/E98ceR3xgwYMLoSZJK1k5zTwbQhICUiv/2Q=="

    # MentionText Mono Bold Italic Strike Underline Spoiler hyperlink
    def sendMessage(
        self, guid, text, Type=None, link=None, Guid_mention=None, message_id=None
    ):
        if Type != None:
            if Type == "MentionText":
                if Guid_mention != None:
                    return GetDataMethod(
                        target=self.methods.methodsShad,
                        args=(
                            "json",
                            "sendMessage",
                            {
                                "object_guid": guid,
                                "rnd": f"{randint(100000,999999)}",
                                "text": text,
                                "metadata": {
                                    "meta_data_parts": TypeText(
                                        "MentionText", text, guid=Guid_mention
                                    )
                                },
                                "reply_to_message_id": message_id,
                            },
                            self.cli,
                        ),
                    ).show()

            elif Type != "MentionText" and Type != "hyperlink":
                return GetDataMethod(
                    target=self.methods.methodsShad,
                    args=(
                        "json",
                        "sendMessage",
                        {
                            "object_guid": guid,
                            "rnd": f"{randint(100000,999999)}",
                            "text": text,
                            "metadata": {"meta_data_parts": TypeText(Type, text=text)},
                            "reply_to_message_id": message_id,
                        },
                        self.cli,
                    ),
                ).show()

            elif Type == "hyperlink":
                return GetDataMethod(
                    target=self.methods.methodsShad,
                    args=(
                        "json",
                        "sendMessage",
                        {
                            "object_guid": guid,
                            "rnd": f"{randint(100000,999999)}",
                            "text": text,
                            "metadata": {
                                "meta_data_parts": TypeText(Type, text=text, link=link)
                            },
                            "reply_to_message_id": message_id,
                        },
                        self.cli,
                    ),
                ).show()

        elif Type == None:
            return GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "sendMessage",
                    {
                        "object_guid": guid,
                        "rnd": f"{randint(100000,999999)}",
                        "text": text,
                        "reply_to_message_id": message_id,
                    },
                    self.cli,
                ),
            ).show()

    def editMessage(self, guid, new, message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "editMessage",
                {"message_id": message_id, "object_guid": guid, "text": new},
                self.cli,
            ),
        ).show()

    def deleteMessages(self, guid, message_ids, All=False):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "deleteMessages",
                {
                    "object_guid": guid,
                    "message_ids": message_ids,
                    "type": "Local" if All == False else "Global",
                },
                self.cli,
            ),
        ).show()

    def getMessagefilter(self, guid, filter_whith):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "getMessages",
                    {
                        "filter_type": filter_whith,
                        "max_id": "NaN",
                        "object_guid": guid,
                        "sort": "FromMax",
                    },
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("messages")
        )

    def getMessages(self, guid, min_id):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "getMessagesInterval",
                    {"object_guid": guid, "middle_message_id": min_id},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("messages")
        )

    def getMessagesbySort(self, guid, message_id, Type):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getMessages",
                {
                    "object_guid": guid,
                    "sort": "FromMax" if Type == "max" else "FromMin",
                    "max_id" if Type == "max" else "min_id": message_id,
                },
                self.cli,
            ),
        ).show()

    def searchMessages(self, guid, text):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "searchChatMessages",
                {
                    "search_text": text.replace("#", ""),
                    "type": "Hashtag" if text.startswith("#") else "Text",
                    "object_guid": guid,
                },
                self.cli,
            ),
        ).show()

    # Hashtag #Text.....

    def getChats(self, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getChats", {"start_id": start_id}, self.cli),
        ).show()

    def getMapView(self, latitude, longitude):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getMapView",
                {"location": {"latitude": latitude, "longitude": longitude}},
                self.cli,
            ),
        ).show()

    def sendMap(self, guid, latitude, longitude):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "sendMessage",
                {
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "location": {"latitude": latitude, "longitude": longitude},
                },
                self.cli,
            ),
        ).show()

    def getMessagesUpdates(self, guid):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getMessagesUpdates",
                {"object_guid": guid, "state": state},
                self.cli,
            ),
        ).show()

    @property
    def getChatsUpdate(self):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getChatsUpdates", {"state": state}, self.cli),
        ).show()

    def deleteUserChat(self, user_guid, last_message):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "deleteUserChat",
                {"last_deleted_message_id": last_message, "user_guid": user_guid},
                self.cli,
            ),
        ).show()

    def startSupperBot(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "sendMessage",
                {"object_guid": guid, "rnd": randint(100000, 999999), "text": "/start"},
                self.cli,
            ),
        ).show()

    def stoptSupperBot(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "stopBot", {"bot_guid": guid}, self.cli),
        ).show()

    def getBotInfo(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getBotInfo", {"bot_guid": guid}, self.cli),
        ).show()

    def sendChatActivity(self, user_guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "sendChatActivity",
                {"object_guid": user_guid, "activity": "Typing"},
                self.cli,
            ),
        ).show()

    def getInfoByUsername(self, username):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getObjectByUsername",
                {"username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def banGroupMember(self, guid_gap, user_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "banGroupMember",
                {"group_guid": guid_gap, "member_guid": user_id, "action": "Set"},
                self.cli,
            ),
        ).show()

    def unbanGroupMember(self, guid_gap, user_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "banGroupMember",
                {"group_guid": guid_gap, "member_guid": user_id, "action": "Unset"},
                self.cli,
            ),
        ).show()

    def banChannelMember(self, guid_channel, user_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "banChannelMember",
                {"channel_guid": guid_channel, "member_guid": user_id, "action": "Set"},
                self.cli,
            ),
        ).show()

    def unbanChannelMember(self, guid_channel, user_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "banChannelMember",
                {
                    "channel_guid": guid_channel,
                    "member_guid": user_id,
                    "action": "Unset",
                },
                self.cli,
            ),
        ).show()

    def getGroupMentionList(self, guid_group, text):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getGroupMentionList",
                {"group_guid": guid_group, "search_mention": text},
                self.cli,
            ),
        ).show()

    def shaireContect(self, guid, phone_number, first_name, last_name=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "sendMessage",
                {
                    "object_guid": "u09pbi05e46fa119166489d14a3f0562",
                    "type": "ContactMessage",
                    "message_contact": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone_number": f"98{phone_number[1:]}",
                        "user_guid": guid,
                    },
                    "rnd": randint(100000, 999999),
                },
                self.cli,
            ),
        ).show()

    # report account or channell or group
    def report(self, guid, reportType):
        if not reportType in [102, 101, 104, 103, 105, 106, 100]:
            raise ErrorMethod("the numerTypeReport is wrong! ")
        else:
            return GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "reportObject",
                    {
                        "object_guid": guid,
                        "report_type": reportType,
                        "report_type_object": "Object",
                    },
                    self.cli,
                ),
            ).show()

    def reportPost(self, guid, reportType, message_ids):
        if not reportType in [102, 101, 104, 103, 105, 106, 100]:
            raise ErrorMethod("the numerTypeReport is wrong ! ")
        else:
            return GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "reportObject",
                    {
                        "object_guid": guid,
                        "message_id": message_ids,
                        "report_type": reportType,
                        "report_type_object": "Message",
                    },
                    self.cli,
                ),
            ).show()

    def otherReport(self, TYPE, guid, text, message_ids=None):
        if TYPE == "message":
            if message_ids != None:
                return GetDataMethod(
                    target=self.methods.methodsShad,
                    args=(
                        "json",
                        "reportObject",
                        {
                            "object_guid": guid,
                            "message_id": message_ids,
                            "report_type": 100,
                            "report_type_object": "Message",
                            "report_description": text,
                        },
                        self.cli,
                    ),
                ).show()
            else:
                raise ErrorMethod("in method report << message_id is None ! >> ")
        elif TYPE == "pv" or "channel":
            return GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "reportObject",
                    {
                        "object_guid": guid,
                        "report_type": 100,
                        "report_type_object": "Object",
                        "report_description": text,
                    },
                    self.cli,
                ),
            ).show()

    def getbanGroupUsers(self, guid_gap, text=None, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getBannedGroupMembers",
                {"group_guid": guid_gap, "search_text": text, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def getbanChannelUsers(self, guid_channel, text=None, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getBannedChannelMembers",
                {
                    "channel_guid": guid_channel,
                    "search_text": text,
                    "start_id": start_id,
                },
                self.cli,
            ),
        ).show()

    def getGroupInfo(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getGroupInfo", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getChannelInfo(self, guid_channel):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getChannelInfo", {"channel_guid": guid_channel}, self.cli),
        ).show()

    def addMemberGroup(self, guid_gap, user_ids):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "addGroupMembers",
                {"group_guid": guid_gap, "member_guids": user_ids},
                self.cli,
            ),
        ).show()

    def addMemberChannel(self, guid_channel, user_ids):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "addChannelMembers",
                {"channel_guid": guid_channel, "member_guids": user_ids},
                self.cli,
            ),
        ).show()

    def getGroupAdmins(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getGroupAdminMembers", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getChannelAdmins(self, guid_channel):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getChannelAdminMembers",
                {"channel_guid": guid_channel},
                self.cli,
            ),
        ).show()

    def AddNumberPhone(self, first_num, last_num, numberPhone):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "addAddressBook",
                {"phone": numberPhone, "first_name": first_num, "last_name": last_num},
                self.cli,
            ),
        ).show()

    def getMessagesInfo(self, guid, message_ids: list):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getMessagesByID",
                {"object_guid": guid, "message_ids": message_ids},
                self.cli,
            ),
        ).show()

    def getGroupMembers(self, guid_gap, text=None, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getGroupAllMembers",
                {"group_guid": guid_gap, "search_text": text, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def getChannelMembers(self, channel_guid, text=None, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getChannelAllMembers",
                {
                    "channel_guid": channel_guid,
                    "search_text": text,
                    "start_id": start_id,
                },
                self.cli,
            ),
        ).show()

    def lockGroup(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setGroupDefaultAccess",
                {"access_list": ["AddMember"], "group_guid": guid_gap},
                self.cli,
            ),
        ).show()

    def unlockGroup(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setGroupDefaultAccess",
                {"access_list": ["SendMessages", "AddMember"], "group_guid": guid_gap},
                self.cli,
            ),
        ).show()

    def getGroupAccess(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getGroupDefaultAccess", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getGroupLink(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getGroupLink", {"group_guid": guid_gap}, self.cli),
        ).show()

    def numberOnline(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getGroupOnlineCount", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getChannelLink(self, guid_channel):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "getChannelLink",
                    {"channel_guid": guid_channel},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("join_link")
        )

    def changeGroupLink(self, guid_gap):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=("json", "setGroupLink", {"group_guid": guid_gap}, self.cli),
            )
            .show()
            .get("data")
            .get("join_link")
        )

    def changeChannelLink(self, guid_channel):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "setChannelLink",
                    {"channel_guid": guid_channel},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("join_link")
        )

    def setGroupTimer(self, guid_gap, time):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getAvailableReactions",
                {
                    "group_guid": guid_gap,
                    "slow_mode": time,
                    "updated_parameters": ["slow_mode"],
                },
                self.cli,
            ),
        ).show()

    def getGroupMessageReadParticipants(self, guid_gap, message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getGroupMessageReadParticipants",
                {"group_guid": guid_gap, "message_id": message_id},
                self.cli,
            ),
        ).show()

    def setGroupAdmin(self, guid_gap, guid_member, access_admin=None):
        access_admin = (
            access_admin
            if access_admin != None
            else [
                "ChangeInfo",
                "SetJoinLink",
                "SetAdmin",
                "BanMember",
                "DeleteGlobalAllMessages",
                "PinMessages",
                "SetMemberAccess",
            ]
        )
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setGroupAdmin",
                {
                    "group_guid": guid_gap,
                    "access_list": access_admin,
                    "action": "SetAdmin",
                    "member_guid": guid_member,
                },
                self.cli,
            ),
        ).show()

    def deleteGroupAdmin(self, guid_gap, guid_admin):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setGroupAdmin",
                {
                    "group_guid": guid_gap,
                    "action": "UnsetAdmin",
                    "member_guid": guid_admin,
                },
                self.cli,
            ),
        ).show()

    def deleteGroup(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "removeGroup", {"group_guid": guid_gap}, self.cli),
        ).show()

    def setChannelAdmin(self, guid_channel, guid_member, access_admin=None):
        access_admin = (
            access_admin
            if access_admin != None
            else [
                "SetAdmin",
                "SetJoinLink",
                "AddMember",
                "DeleteGlobalAllMessages",
                "EditAllMessages",
                "SendMessages",
                "PinMessages",
                "ViewAdmins",
                "ViewMembers",
                "ChangeInfo",
            ]
        )
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setChannelAdmin",
                {
                    "channel_guid": guid_channel,
                    "access_list": access_admin,
                    "action": "SetAdmin",
                    "member_guid": guid_member,
                },
                self.cli,
            ),
        ).show()

    def deleteChannelAdmin(self, guid_channel, guid_admin):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setChannelAdmin",
                {
                    "channel_guid": guid_channel,
                    "action": "UnsetAdmin",
                    "member_guid": guid_admin,
                },
                self.cli,
            ),
        ).show()

    def getStickersByEmoji(self, emojee):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "getStickersByEmoji",
                    {"emoji_character": emojee, "suggest_by": "All"},
                    self.cli,
                ),
            )
            .show()
            .get("data")
        )

    def searchStickerSets(self, text, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "searchStickerSets",
                {"search_text": text, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def getTrendStickerSets(self, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getTrendStickerSets", {"start_id": start_id}, self.cli),
        ).show()

    def getStickerSetByID(self, sticker_set_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getStickerSetByID",
                {"sticker_set_id": sticker_set_id},
                self.cli,
            ),
        ).show()

    def actionStickerSet(self, action: int, sticker_set_id=None):
        Action = ["Add", "Remove"]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "actionOnStickerSet",
                {"sticker_set_id": sticker_set_id, "action": Action[action]},
                self.cli,
            ),
        ).show()

    def activenotification(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setActionChat",
                {"action": "Unmute", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def offnotification(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setActionChat",
                {"action": "Mute", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def sendPoll(self, guid, question, options: list):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "createPoll",
                {
                    "object_guid": guid,
                    "options": options,
                    "rnd": f"{randint(100000,999999999)}",
                    "question": question,
                    "type": "Regular",
                    "is_anonymous": False,
                    "allows_multiple_answers": True,
                },
                self.cli,
            ),
        ).show()

    def sendPollExam(self, guid, question, options: list, explanation):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "createPoll",
                {
                    "object_guid": guid,
                    "options": options,
                    "rnd": f"{randint(100000,999999999)}",
                    "question": question,
                    "type": "Quiz",
                    "is_anonymous": False,
                    "allows_multiple_answers": False,
                    "explanation": explanation,
                    "correct_option_index": 1,
                },
                self.cli,
            ),
        ).show()

    def getPollStatus(self, poll_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getPollStatus", {"poll_id": poll_id}, self.cli),
        ).show()

    def getVoters(self, poll_id, index):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getPollOptionVoters",
                {"poll_id": poll_id, "selection_index": index},
                self.cli,
            ),
        ).show()

    def votePoll(self, poll_id, index):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "votePoll",
                {"poll_id": poll_id, "selection_index": index},
                self.cli,
            ),
        ).show()

    def forwardMessages(self, From, message_ids, to):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "forwardMessages",
                {
                    "from_object_guid": From,
                    "message_ids": message_ids,
                    "rnd": f"{randint(100000,999999999)}",
                    "to_object_guid": to,
                },
                self.cli,
            ),
        ).show()

    def VisitChatGroup(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "editGroupInfo",
                {
                    "chat_history_for_new_members": "Visible",
                    "group_guid": guid_gap,
                    "updated_parameters": ["chat_history_for_new_members"],
                },
                self.cli,
            ),
        ).show()

    def HideChatGroup(self, guid_gap):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "editGroupInfo",
                {
                    "chat_history_for_new_members": "Hidden",
                    "group_guid": guid_gap,
                    "updated_parameters": ["event_messages"],
                },
                self.cli,
            ),
        ).show()

    def pin(self, guid, message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setPinMessage",
                {"action": "Pin", "message_id": message_id, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def unpin(self, guid, message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getAvailableReactions", {}, self.cli),
        ).show()
        return self.methods.methodsShad(
            "json",
            methode="setPinMessage",
            indata={"action": "Unpin", "message_id": message_id, "object_guid": guid},
            wn=self.cli,
        )

    @property
    def logout(self):
        return GetDataMethod(
            target=self.methods.methodsShad, args=("json", "logout", {}, self.cli)
        ).show()

    def joinGroup(self, link):
        hashLink = link.split("/")[-1]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "joinGroup", {"hash_link": hashLink}, self.cli),
        ).show()

    def joinChannelAll(self, guid):
        if ("https://" or "http://") in guid:
            link = guid.split("/")[-1]
            return GetDataMethod(
                target=self.methods.methodsShad,
                args=("json", "joinChannelByLink", {"hash_link": link}, self.cli),
            ).show()

        elif "@" in guid or not "@" in guid:
            IDE = guid.replace("@", "")
            guid = self.getInfoByUsername(IDE)["data"]["channel"]["channel_guid"]
            return GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "joinChannelAction",
                    {"action": "Join", "channel_guid": guid},
                    self.cli,
                ),
            ).show()

        elif guid.startswith("c0"):
            return GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "joinChannelAction",
                    {"action": "Join", "channel_guid": guid},
                    self.cli,
                ),
            ).show()

    def joinChannelByLink(self, link):
        hashLink = link.split("/")[-1]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "joinChannelByLink", {"hash_link": hashLink}, self.cli),
        ).show()

    def joinChannelByID(self, ide):
        IDE = ide.replace("@", "")
        GUID = self.getInfoByUsername(IDE)["data"]["channel"]["channel_guid"]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "joinChannelAction",
                {"action": "Join", "channel_guid": GUID},
                self.cli,
            ),
        ).show()

    def joinChannelByGuid(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "joinChannelAction",
                {"action": "Join", "channel_guid": guid},
                self.cli,
            ),
        ).show()

    def leaveGroup(self, guid_gap):
        if "https://" in guid_gap:
            guid_gap = self.joinGroup(guid_gap)["data"]["group"]["group_guid"]
        else:
            guid_gap = guid_gap
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "leaveGroup", {"group_guid": guid_gap}, self.cli),
        ).show()

    def leaveChannel(self, guid_channel):
        if "https://" in guid_channel:
            guid_channel = self.joinChannelByLink(guid_channel)["data"]["chat_update"][
                "object_guid"
            ]
        elif "@" in guid_channel:
            guid_channel = self.joinChannelByID(guid_channel)["data"]["chat_update"][
                "object_guid"
            ]
        else:
            guid_channel = guid_channel
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "joinChannelAction",
                {"action": "Leave", "channel_guid": guid_channel},
                self.cli,
            ),
        ).show()

    def EditNameGroup(self, groupgu, namegp):
        biogp = self.getGroupInfo(groupgu).get("data").get("group").get("description")
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "editGroupInfo",
                {
                    "group_guid": groupgu,
                    "title": namegp,
                    "description": biogp,
                    "updated_parameters": ["title", "description"],
                },
                self.cli,
            ),
        ).show()

    def EditBioGroup(self, groupgu, biogp):
        namegp = self.getGroupInfo(groupgu).get("data").get("group").get("group_title")
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "editGroupInfo",
                {
                    "group_guid": groupgu,
                    "title": namegp,
                    "description": biogp,
                    "updated_parameters": ["title", "description"],
                },
                self.cli,
            ),
        ).show()

    def block(self, guid_user):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setBlockUser",
                {"action": "Block", "user_guid": guid_user},
                self.cli,
            ),
        ).show()

    def unblock(self, guid_user):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setBlockUser",
                {"action": "Unblock", "user_guid": guid_user},
                self.cli,
            ),
        ).show()

    # startVoiceChat channel or group
    def startVoiceChat(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "createGroupVoiceChat", {"chat_guid": guid}, self.cli),
        ).show()

    def addUserContact(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setAskSpamAction",
                {"object_guid": guid, "action": "AddToContact"},
                self.cli,
            ),
        ).show()

    def getVoiceChatId(self, guid):
        if guid.startswith("g0"):
            return self.getGroupInfo(guid)["data"]["chat"]["group_voice_chat_id"]
        elif guid.startswith("c0"):
            return self.getChannelInfo(guid)["data"]["chat"]["group_voice_chat_id"]
        else:
            return "error only guid channel or group"

    def getGroupVoiceChat(self, guid):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                f"getGroupVoiceChat",
                {"voice_chat_id": voice_chat_id, "chat_guid": guid},
                self.cli,
            ),
        ).show()

    # getGroupVoiceChatParticipants channel or group
    def getGroupVoiceChatParticipants(self, guid, start_id=None):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                f"getGroupVoiceChatParticipants",
                {
                    f"chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "start_id": start_id,
                },
                self.cli,
            ),
        ).show()

    # *
    #  join_muted = true  Members can speak join_muted = false Members can not speak  channel or group
    def editVoiceChat(self, guid, bol: bool = True):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setGroupVoiceChatSetting",
                {
                    "chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "join_muted": bol,
                    "updated_parameters": ["join_muted"],
                },
                self.cli,
            ),
        ).show()

    # changeTitleVoiceChat channel or group
    def changeTitleVoiceChat(self, guid, title):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setGroupVoiceChatSetting",
                {
                    f"chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "title": title,
                    "updated_parameters": ["title"],
                },
                self.cli,
            ),
        ).show()

    # finishVoiceChat channel or group
    def finishVoiceChat(self, guid):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "discardGroupVoiceChat",
                {"chat_guid": guid, "voice_chat_id": voice_chat_id},
                self.cli,
            ),
        ).show()

    # leaveGroupVoiceChat group or channel
    def leaveGroupVoiceChat(self, guid):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "leaveGroupVoiceChat",
                {"chat_guid": guid, "voice_chat_id": voice_chat_id},
                self.cli,
            ),
        ).show()

    def getDisplayAsInGroupVoiceChat(self, guid, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getDisplayAsInGroupVoiceChat",
                {"chat_guid": guid, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def sendGroupVoiceChatActivity(self, guid, activity, guiduser):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getGroupVoiceChatActivity",
                {
                    "group_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "activity": activity,
                    "participant_object_guid": guiduser,
                },
                self.cli,
            ),
        ).show()

    def getGroupVoiceChatUpdates(self, guid):
        voice_chat_id, state = self.getVoiceChatId(guid), str(
            round(datetime.datetime.today().timestamp()) - 200
        )
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getGroupVoiceChatUpdates",
                {"chat_guid": guid, "voice_chat_id": voice_chat_id, "state": state},
                self.cli,
            ),
        ).show()

    def setGroupVoiceChatState(self, guid, state, guid_member):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setGroupVoiceChatState",
                {
                    "chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "action": "Mute" if state == False else "Unmute",
                    "participant_object_guid": guid_member,
                },
                self.cli,
            ),
        ).show()

    def getUserInfo(self, guid_user):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getUserInfo", {"user_guid": guid_user}, self.cli),
        ).show()

    def getUserInfoByIDE(self, IDE_user):
        guiduser = self.getInfoByUsername(IDE_user.replace("@", ""))["data"]["user"][
            "user_guid"
        ]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getUserInfo", {"user_guid": guiduser}, self.cli),
        ).show()

    def seeGroupbyLink(self, link_gap):
        link = link_gap.replace("https://rubika.ir/joing/", "")
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=("json", "groupPreviewByJoinLink", {"hash_link": link}, self.cli),
            )
            .show()
            .get("data")
        )

    def seeChannelbyLink(self, link_channel):
        link = link_channel.replace("https://rubika.ir/joinc/", "")
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "channelPreviewByJoinLink",
                    {"hash_link": link},
                    self.cli,
                ),
            )
            .show()
            .get("data")
        )

    def getAvatars(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getAvatars", {"object_guid": guid}, self.cli),
        ).show()

    def uploadAvatar_replay(self, files_ide):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "uploadAvatar",
                {
                    "thumbnail_file_id": files_ide,
                    "main_file_id": files_ide,
                },
                self.cli,
            ),
        ).show()

    def uploadAvatar(self, main, thumbnail=None):
        mainID = str(self.Upload.uploadFile(main)[0]["id"])
        thumbnailID = str(self.Upload.uploadFile(thumbnail or main)[0]["id"])
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "uploadAvatar",
                {
                    "thumbnail_file_id": thumbnailID,
                    "main_file_id": mainID,
                },
                self.cli,
            ),
        ).show()

    def removeAvatar(self, guid):
        avatar_id = self.getAvatars(guid)["data"]["avatars"][0]["avatar_id"]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "deleteAvatar",
                {"object_guid": guid, "avatar_id": avatar_id},
                self.cli,
            ),
        ).show()

    def removeAllAvatars(self, guid):
        while 1:
            try:
                avatar = self.getAvatars(guid)["data"]["avatars"]
                if avatar != []:
                    avatar_id = self.getAvatars(guid)["data"]["avatars"][0]["avatar_id"]
                    GetDataMethod(
                        target=self.methods.methodsShad,
                        args=(
                            "json",
                            "deleteAvatar",
                            {"object_guid": guid, "avatar_id": avatar_id},
                            self.cli,
                        ),
                    ).show()
                else:
                    return "Ok remove Avatars"
                    break
            except:
                continue

    def Devicesrubika(self, service_guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getServiceInfo", {"service_guid": service_guid}, self.cli),
        ).show()

    def getPaymentInfo(self, payment_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getPaymentInfo", {"payment_id": payment_id}, self.cli),
        ).show()

    def deleteChatHistory(self, guid, last_message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "deleteChatHistory",
                {"last_message_id": last_message_id, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def addFolder(
        self,
        Name="Arsein",
        include_chat=None,
        include_object=None,
        exclude_chat=None,
        exclude_object=None,
    ):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "addFolder",
                {
                    "exclude_chat_types": exclude_chat,
                    "exclude_object_guids": exclude_object,
                    "include_chat_types": include_chat,
                    "include_object_guids": include_object,
                    "is_add_to_top": True,
                    "name": Name,
                },
                self.cli,
            ),
        ).show()

    def deleteFolder(self, folder_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "deleteFolder", {"folder_id": folder_id}, self.cli),
        ).show()

    def addGroup(self, title, guidsUser: list):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "addGroup",
                {"member_guids": guidsUser, "title": title},
                self.cli,
            ),
        ).show()

    def deleteGroup(self, guid_group):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "deleteNoAccessGroupChat",
                {"group_guid": guid_group},
                self.cli,
            ),
        ).show()

    def addChannel(self, title, typeChannell: int, bio, guidsUser: list):
        TypeChannell = ["Private", "Public"]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "addChannel",
                {
                    "channel_type": TypeChannell[typeChannell],
                    "description": bio,
                    "member_guids": guidsUser,
                    "title": title,
                },
                self.cli,
            ),
        ).show()

    def editUser(self, first_name=None, last_name=None, bio=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "updateProfile",
                {
                    "bio": bio,
                    "first_name": first_name,
                    "last_name": last_name,
                    "updated_parameters": ["first_name", "last_name", "bio"],
                },
                self.cli,
            ),
        ).show()

    def editusername(self, username):
        ide = username.replace("@", "")
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "updateUsername", {"username": ide}, self.cli),
        ).show()

    def Postion(self, guid, guiduser):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "requestChangeObjectOwner",
                {"new_owner_user_guid": guiduser, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def getPostion(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getPendingObjectOwner", {"object_guid": guid}, self.cli),
        ).show()

    def AcceptPostion(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "replyRequestObjectOwner",
                {"action": "Accept", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def RejectPostion(self, guid):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "replyRequestObjectOwner",
                {"action": "Reject", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def sendLive(self, guid, titlelive):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "sendLive",
                {
                    "object_guid": guid,
                    "title": titlelive,
                    "device_type": "Software",
                    "thumb_inline": self.thumb_inline,
                    "rnd": randint(100000, 999999),
                },
                self.cli,
            ),
        ).show()

    @property
    def ClearAccounts(self):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "terminateOtherSessions", {}, self.cli),
        ).show()

    @property
    def DeleteAccount(self):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "requestDeleteAccount", {}, self.cli),
        ).show()

    def selectionClearAccount(self, session_key):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "terminateSession", {"session_key": session_key}, self.cli),
        ).show()

    def HidePhone(self, **kwargs):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setSetting",
                {"settings": kwargs, "update_parameters": ["show_my_phone_number"]},
                self.cli,
            ),
        ).show()

    def HideOnline(self, **kwargs):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setSetting",
                {"settings": kwargs, "update_parameters": ["show_my_last_online"]},
                self.cli,
            ),
        ).show()

    def search_inaccount(self, text):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "searchGlobalMessages",
                    {"search_text": text, "start_id": None, "type": "Text"},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("messages")
        )

    def search_inrubika(self, text):
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=("json", "searchGlobalObjects", {"search_text": text}, self.cli),
            )
            .show()
            .get("data")
            .get("objects")
        )

    def getAbsObjects(self, guids: list):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getAbsObjects", {"objects_guids": guids}, self.cli),
        ).show()

    def Infolinkpost(self, linkpost):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getLinkFromAppUrl", {"app_url": linkpost}, self.cli),
        ).show()

    def addToMyGifSet(self, guid, message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "addToMyGifSet",
                {"message_id": message_id, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def deleteMyGifSet(self, file_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "removeFromMyGifSet", {"file_id": file_id}, self.cli),
        ).show()

    def getContactsLastOnline(self, user_guids: list):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getContactsLastOnline",
                {"user_guids": user_guids},
                self.cli,
            ),
        ).show()

    def SignMessageChannel(self, guid_channel, sign: bool):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "editChannelInfo",
                {
                    "channel_guid": guid_channel,
                    "sign_messages": sign,
                    "updated_parameters": ["sign_messages"],
                },
                self.cli,
            ),
        ).show()

    @property
    def ActiveContectJoin(self):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setSetting",
                {
                    "settings": {"can_join_chat_by": "MyContacts"},
                    "update_parameters": ["can_join_chat_by"],
                },
                self.cli,
            ),
        ).show()

    @property
    def ActiveEverybodyJoin(self):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setSetting",
                {
                    "settings": {"can_join_chat_by": "Everybody"},
                    "update_parameters": ["can_join_chat_by"],
                },
                self.cli,
            ),
        ).show()

    def CalledBy(self, typeCall: str):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setSetting",
                {
                    "settings": {"can_called_by": typeCall},
                    "update_parameters": ["can_called_by"],
                },
                self.cli,
            ),
        ).show()

    def changeChannelID(self, guid_channel, username):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "updateChannelUsername",
                {"channel_guid": guid_channel, "username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def getMessageShareUrl(self, guid, messageId):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getMessageShareUrl",
                {"object_guid": guid, "messageId": messageId},
                self.cli,
            ),
        ).show()

    def getBlockedUsers(self, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getBlockedUsers", {"start_id": start_id}, self.cli),
        ).show()

    def deleteContact(self, guid_user):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "deleteContact", {"user_guid": guid_user}, self.cli),
        ).show()

    def checkUserUsername(self, username):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "checkUserUsername",
                {"username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def checkChannelUsername(self, username):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "checkChannelUsername",
                {"username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def getContacts(self, start_id=None):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getContacts", {"start_id": start_id}, self.cli),
        ).show()

    def getLiveStatus(self, live_id, token_live):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getLiveStatus",
                {"live_id": live_id, "access_token": token_live},
                self.cli,
            ),
        ).show()

    def getLiveComments(self, live_id, token_live):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "getLiveComments",
                {"live_id": live_id, "access_token": token_live},
                self.cli,
            ),
        ).show()

    @property
    def getdatabaseReaction(self):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getAvailableReactions", {}, self.cli),
        ).show()

    def Reaction(self, guid, typeReaction, reaction, message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "actionOnMessageReaction",
                {
                    "action": "Add" if typeReaction == "add" else "Remove",
                    "reaction_id": reaction,
                    "message_id": message_id,
                    "object_guid": guid,
                },
                self.cli,
            ),
        ).show()

    def commonGroup(self, guid_user):
        IDE = guid_user.replace("@", "")
        GUID = self.getInfoByUsername(IDE)["data"]["user"]["user_guid"]
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getCommonGroups", {"user_guid": GUID}, self.cli),
        ).show()

    def setTypeChannel(self, guid_channel, type_Channel):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "editChannelInfo",
                {
                    "channel_guid": guid_channel,
                    "channel_type": (
                        "Private" if type_Channel == "Private" else "Public"
                    ),
                    "updated_parameters": ["channel_type"],
                },
                self.cli,
            ),
        ).show()

    def getChatAds(self, user_guids: list):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getChatAds", {"state": state}, self.cli),
        ).show()

    def clickMessageUrl(self, guid, message_id, link):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "clickMessageUrl",
                {"object_guid": guid, "message_id": message_id, "link_url": link},
                self.cli,
            ),
        ).show()

    def seenChat(self, guid, message_id):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "seenChat",
                {"seen_list": {f"{guid}": f"{message_id}"}},
                self.cli,
            ),
        ).show()

    @property
    def getContactsUpdates(self):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "getContactsUpdates", {"state": state}, self.cli),
        ).show()

    def twolocks(self, ramz, hide):
        locked = GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "setupTwoStepVerification",
                {"hint": hide, "password": ramz},
                self.cli,
            ),
        ).show()
        if locked["status"] == "ERROR_GENERIC":
            return locked["self.client_show_message"]["link"]["alert_data"]["message"]
        else:
            return locked

    def deletetwolocks(self, password):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "turnOffTwoStep", {"password": password}, self.cli),
        ).show()

    def checkPassword(self, password):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "checkTwoStepPasscode", {"password": password}, self.cli),
        ).show()

    def passwordChange(self, password):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "resendCodeRecoveryEmail", {"password": password}, self.cli),
        ).show()

    def loginforgetPassword(self, emailCode, password, phone_number):
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=(
                "json",
                "loginDisableTwoStep",
                {
                    "email_code": emailCode,
                    "forget_password_code_hash": password,
                    "phone_number": phone_number,
                },
                self.cli,
            ),
        ).show()

    def ProfileEdit(self, first_name=None, last_name=None, bio=None, username=None):
        while 1:
            try:
                for tekrar in range(1):
                    self.editUser(first_name=first_name, last_name=last_name, bio=bio)
                    if username != None:
                        self.editusername(username.replace("@", ""))
                    return "Profile edited"
                break
            except:
                continue

    def getChatGroup(self, guid_gap):
        while 1:
            try:
                for tekrar in range(1):
                    lastmessages = self.getGroupInfo(guid_gap)["data"]["chat"][
                        "last_message_id"
                    ]
                    messages = self.getMessages(guid_gap, lastmessages)
                    return messages
                break
            except:
                continue

    def getChatChannel(self, guid_channel):
        while 1:
            try:
                for tekrar in range(1):
                    lastmessages = self.getChannelInfo(guid_channel)["data"]["chat"][
                        "last_message_id"
                    ]
                    messages = self.getMessages(guid_channel, lastmessages)
                    return messages
                break
            except:
                continue

    def getChatUser(self, guid_User):
        while 1:
            try:
                for tekrar in range(1):
                    lastmessages = self.getUserInfo(guid_User)["data"]["chat"][
                        "last_message_id"
                    ]
                    messages = self.getMessages(guid_User, lastmessages)
                    return messages
                break
            except:
                continue

    @property
    def Authrandom(self):
        auth = ""
        meghdar = "qwertyuiopasdfghjklzxcvbnm0123456789"
        for string in range(32):
            auth += choice(meghdar)
        return auth

    # method send Files

    def requestSendFile(self, addressfile):
        return GetDataMethod(
            target=self.methods.methodsShad,
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

    def resend(self, guid, message_id: list):
        datamsg = self.getMessagesInfo(guid, message_id).get("data").get("messages")[0]
        resend = makeJsonResend(guid, datamsg.get("file_inline"))
        if "text" in datamsg.keys():
            resend["text"] = datamsg.get("text")
        else:
            resend["text"] = None
        return GetDataMethod(
            target=self.methods.methodsShad,
            args=("json", "sendMessage", resend, self.cli),
        ).show()

    def downloadFiles(self, guid, message_id: list, link=False):
        getdatafile = (
            self.getMessagesInfo(guid, message_id)
            .get("data")
            .get("messages")[0]
            .get("file_inline")
        )
        if link == False:
            return self.methods.methodsShad(
                "download",
                downloads=[
                    self.Auth,
                    getdatafile.get("dc_id"),
                    getdatafile.get("file_id"),
                    getdatafile.get("size"),
                    getdatafile.get("access_hash_rec"),
                ],
            )
        elif link == True:
            Link: str = (
                f"https://messenger{getdatafile.get('dc_id')}.iranlms.ir/InternFile.ashx?id={getdatafile.get('file_id')}&ach={getdatafile.get('access_hash_rec')}"
            )
            file: bin = httpx.get(Link).content
            return [file, True]

    def Http(self, link, formats):
        while True:
            try:
                for tek in range(1):

                    async def download_file(link, formatt):
                        async with aiohttp.ClientSession() as session:
                            async with session.get(link) as response:
                                if response.status == 200:
                                    while True:
                                        buildnamefiles = f"LibraryArseinShad{randint(0,1000)}.{formatt}"
                                        checkname = os.path.exists(buildnamefiles)
                                        if checkname == False:
                                            for tek in range(1):
                                                with open(buildnamefiles, "wb") as file:
                                                    content = await response.read()
                                                    file.write(content)
                                                return buildnamefiles
                                            break
                                        else:
                                            continue
                                else:
                                    return 404

                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(download_file(link, formats))
                break
            except Exception as Error:
                continue

    def SendSticker(
        self,
        guid,
        emoji_character,
        w_h_ratio,
        sticker_id,
        file_id,
        dc_id,
        access_hash_rec,
        sticker_set_id,
    ):
        return self.methods.methodsShad(
            "json",
            methode="sendMessage",
            indata={
                "object_guid": guid,
                "rnd": randint(100000, 999999999),
                "sticker": {
                    "emoji_character": emoji_character,
                    "w_h_ratio": w_h_ratio,
                    "sticker_id": sticker_id,
                    "file": {
                        "file_id": file_id,
                        "mime": "png",
                        "dc_id": dc_id,
                        "access_hash_rec": access_hash_rec,
                        "file_name": "sticker.png",
                        "cdn_tag": "PR5",
                        "size": 0,
                    },
                    "sticker_set_id": sticker_set_id,
                },
            },
            wn=self.cli,
        )

    def SendImage(
        self,
        guid,
        addressfile,
        spoil: bool = False,
        thumbinline=None,
        caption=None,
        message_id=None,
    ):
        addressfile: str = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "png")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getphoto = Image.open(addressfile)
            up = self.Upload.uploadFile(addressfile)
            width, height = getphoto.size
            thumbinline = (
                self.thumb_inline
                if thumbinline == None
                else str(getThumbInline(open(addressfile, "rb").read()))
            )
            getphoto.close()
            if addressfile.startswith("LibraryArseinShad"):
                os.remove(addressfile)
            return self.methods.methodsShad(
                "json",
                methode="sendMessage",
                indata={
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "Image",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "is_spoil": spoil,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "thumb_inline": thumbinline,
                        "width": width,
                        "height": height,
                        "access_hash_rec": up[1],
                    },
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error sendPhoto"

    def SendFile(self, guid, addressfile, formats=None, caption=None, message_id=None):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, formats)
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            up = self.Upload.uploadFile(addressfile)
            if addressfile.startswith("LibraryArseinShad"):
                os.remove(addressfile)
            return self.methods.methodsShad(
                "json",
                methode="sendMessage",
                indata={
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "File",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "access_hash_rec": up[1],
                    },
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendFile"

    def SendVideo(
        self,
        guid,
        addressfile,
        spoil: bool = False,
        breadth=None,
        thumbinline=None,
        caption=None,
        message_id=None,
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp4")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getvideo = TinyTag.get(addressfile)
            width, height = [100, 100]
            up = self.Upload.uploadFile(addressfile)
            thumbinline = (
                self.thumb_inline
                if thumbinline == None
                else str(getThumbInline(open(addressfile, "rb").read()))
            )
            if addressfile.startswith("LibraryArseinShad"):
                os.remove(addressfile)
            return self.methods.methodsShad(
                "json",
                methode="sendMessage",
                indata={
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "Video",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "is_spoil": spoil,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "thumb_inline": thumbinline,
                        "width": width,
                        "height": height,
                        "time": int(getvideo.duration * 1000),
                        "access_hash_rec": up[1],
                    },
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendVideo"

    def SendGif(
        self,
        guid,
        addressfile,
        breadth=None,
        thumbinline=None,
        caption=None,
        message_id=None,
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp4")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getvideo = TinyTag.get(addressfile)
            width, height = [100, 100]
            up = self.Upload.uploadFile(addressfile)
            thumbinline = (
                self.thumb_inline
                if thumbinline == None
                else str(getThumbInline(open(addressfile, "rb").read()))
            )
            if addressfile.startswith("LibraryArseinShad"):
                os.remove(addressfile)
            return self.methods.methodsShad(
                "json",
                methode="sendMessage",
                indata={
                    "file_inline": {
                        "access_hash_rec": up[1],
                        "auto_play": False,
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "file_name": os.path.basename(addressfile),
                        "height": height,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "size": getSize,
                        "thumb_inline": thumbinline,
                        "time": int(getvideo.duration * 1000),
                        "type": "Gif",
                        "width": width,
                    },
                    "is_mute": False,
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendGif"

    def SendVoice(
        self, guid, addressfile, timevoice=None, caption=None, message_id=None
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp3")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getMP3 = MP3(addressfile)
            time = getMP3.info.length if timevoice == None else timevoice
            up = self.Upload.uploadFile(addressfile)
            if addressfile.startswith("LibraryArseinShad"):
                os.remove(addressfile)
            return self.methods.methodsShad(
                "json",
                methode="sendMessage",
                indata={
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "Voice",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "time": time,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "access_hash_rec": up[1],
                    },
                    "object_guid": guid,
                    "rnd": f"{randint(100000,999999999)}",
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendVoice"

    def SendMusic(self, guid, addressfile, caption=None, message_id=None):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp3")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getMP3 = MP3(addressfile)
            width, height, time = (
                getMP3.info.channels,
                getMP3.info.sample_rate,
                getMP3.info.length,
            )
            up = self.Upload.uploadFile(addressfile)
            if addressfile.startswith("LibraryArseinShad"):
                os.remove(addressfile)
            return self.methods.methodsShad(
                "json",
                methode="sendMessage",
                indata={
                    "file_inline": {
                        "access_hash_rec": up[1],
                        "auto_play": False,
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "file_name": os.path.basename(addressfile),
                        "height": height,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "music_performer": "library ArseinRubika",
                        "size": getSize,
                        "time": time,
                        "type": "Music",
                        "width": width,
                    },
                    "is_mute": False,
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendMusic"

    # method logins

    def register(self, typeauth=None):
        if not typeauth == None:
            self.TypePlatform = typeauth
        return (
            GetDataMethod(
                target=self.methods.methodsShad,
                args=("json", "registerDevice", DeviceTelephone.DeviceWeb, self.cli),
            ).show()
            if self.TypePlatform == "web"
            else GetDataMethod(
                target=self.methods.methodsShad,
                args=(
                    "json",
                    "registerDevice",
                    DeviceTelephone.DeviceAndroid,
                    self.cli,
                ),
            ).show()
        )


def sendCode(platforms, numberphone: str, send_type: bool = False, password=None):
    cli, method = clien(platforms).platform, method_Shad()
    send_type = "Internal" if send_type != False else "SMS"
    return method.methodsShad(
        "login",
        methode="sendCode",
        indata={
            "phone_number": f"98{numberphone[1:]}",
            "send_type": send_type,
            "pass_key": password,
        },
        wn=cli,
    )


def signIn(platforms, numberphone: str, codehash, phone_code, save=None):
    publicKey, privateKey = encoderjson.rsaKeyGenerate()
    method, cli = method_Shad(), clien(platforms).platform
    if platforms and numberphone and codehash and phone_code:
        GetDataSignIn = method.methodsShad(
            "login",
            methode="signIn",
            indata={
                "phone_number": f"98{numberphone[1:]}",
                "phone_code_hash": codehash,
                "phone_code": phone_code,
                "public_key": publicKey,
                "private_key": privateKey,
            },
            wn=cli,
        )
        if GetDataSignIn.get("data").get("status") == "OK":
            data_account = dict(
                Auth=encoderjson.decryptRsaOaep(
                    privateKey, GetDataSignIn.get("data").get("auth")
                ),
                Key=privateKey,
            )
            if save != None:
                with open(f"{save}.json", "a+") as f:
                    dump(data_account, f)
            return data_account

        elif GetDataSignIn.get("data").get("status") == "CodeIsInvalid":
            raise ErrorMethod("Invalid Shad login code")
    elif not platforms or numberphone or codehash or phone_code:
        raise ErrorMethod("Enter the complete values ​​into the method")


class Robot_Shad(Messenger): ...
