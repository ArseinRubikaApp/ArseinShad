from re import findall

from arsein import Messenger

from .Copyright import copyright
from .Error import AuthError, TypeAnti
from .PostData import method_Shad


class Antiadvertisement:
    def __init__(self, Sh_account: str):
        self.Auth = str("".join(findall(r"\w", Sh_account)))
        self.prinet = copyright.CopyRight
        self.methods = method_Shad(Sh_account)
        self.bot = Messenger(Sh_account)

        if self.Auth.__len__() < 32:
            raise AuthError("The Auth entered is incorrect")
        elif self.Auth.__len__() > 32:
            raise AuthError("The Auth entered is incorrect")

    def Anti(
        self,
        Type: str = None,
        admins: list = None,
        guid_gap: str = None,
        msg: str = None,
    ):
        if Type == "Gif":
            while 1:
                try:
                    if admins == None:
                        if msg["file_inline"]["type"] == "Gif":
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Gif"
                            break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if (
                            msg["file_inline"]["type"] == "Gif"
                            and not msg["author_object_guid"] in admins
                        ):
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Gif"
                            break
                        else:
                            break
                except:
                    continue

        elif Type == "Sticker":
            while 1:
                try:
                    if admins == None:
                        if msg["file_inline"]["type"] == "Sticker":
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Sticker"
                            break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if (
                            msg["file_inline"]["type"] == "Sticker"
                            and not msg["author_object_guid"] in admins
                        ):
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Sticker"
                            break
                        else:
                            break
                except:
                    continue

        elif Type == "Image":
            while 1:
                try:
                    if admins == None:
                        if msg["file_inline"]["type"] == "Image":
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Image"
                            break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if (
                            msg["file_inline"]["type"] == "Image"
                            and not msg["author_object_guid"] in admins
                        ):
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Image"
                            break
                        else:
                            break
                except:
                    continue

        elif Type == "Music":
            while 1:
                try:
                    if admins == None:
                        if msg["file_inline"]["type"] == "Music":
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Music"
                            break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if (
                            msg["file_inline"]["type"] == "Music"
                            and not msg["author_object_guid"] in admins
                        ):
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Music"
                            break
                        else:
                            break
                except:
                    continue

        elif Type == "Video":
            while 1:
                try:
                    if admins == None:
                        if msg["file_inline"]["type"] == "Video":
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Video"
                            break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if (
                            msg["file_inline"]["type"] == "Video"
                            and not msg["author_object_guid"] in admins
                        ):
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Video"
                            break
                        else:
                            break
                except:
                    continue

        elif Type == "Voice":
            while 1:
                try:
                    if admins == None:
                        if msg["file_inline"]["type"] == "Voice":
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Voice"
                            break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if (
                            msg["file_inline"]["type"] == "Voice"
                            and not msg["author_object_guid"] in admins
                        ):
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete Voice"
                            break
                        else:
                            break
                except:
                    continue

        elif Type == "File":
            while 1:
                try:
                    if admins == None:
                        if msg["file_inline"]["type"] == "File":
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete File"
                            break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if (
                            msg["file_inline"]["type"] == "File"
                            and not msg["author_object_guid"] in admins
                        ):
                            self.bot.deleteMessages(guid_gap, [msg.get("message_id")])
                            return "delete File"
                            break
                        else:
                            break
                except:
                    continue

        elif Type == "forward":
            while 1:
                try:
                    if admins == None:
                        if "forwarded_from" in msg.keys():
                            msge = self.bot.getMessagesInfo(
                                guid_gap, [msg.get("message_id")]
                            )
                            messag = msge["data"]["messages"]
                            for ms in messag:
                                msgID = ms["message_id"]
                                getjsfor = ms["forwarded_from"]["type_from"]
                                if getjsfor == "Channel" or "User":
                                    self.bot.deleteMessages(guid_gap, [msgID])
                                    return "delete forward"
                                    break
                                else:
                                    break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        if "forwarded_from" in msg.keys():
                            msge = self.bot.getMessagesInfo(
                                guid_gap, [msg.get("message_id")]
                            )
                            messag = msge["data"]["messages"]
                            for ms in messag:
                                msgID = ms["message_id"]
                                getjsfor = ms["forwarded_from"]["type_from"]
                                if (
                                    getjsfor == "Channel"
                                    or "User"
                                    and not msg["author_object_guid"] in admins
                                ):
                                    self.bot.deleteMessages(guid_gap, [msgID])
                                    return "delete forward"
                                    break
                                else:
                                    break
                        else:
                            break
                except:
                    continue

        elif Type == "link":
            while 1:
                try:
                    if admins == None:
                        msgID = msg.get("message_id")
                        if msg["type"] == "Text" and not "forwarded_from" in msg.keys():
                            if (
                                findall(r"https://rubika.ir/joing/\w{32}", msg["text"])
                                or findall(
                                    r"https://rubika.ir/joinc/\w{32}", msg["text"]
                                )
                                or findall(r"https://rubika.ir/\w{32}", msg["text"])
                                or findall(r"https://\w", msg["text"])
                                or findall(r"http://\w", msg["text"])
                                or findall(r"@\w", msg["text"]) != []
                            ):
                                self.bot.deleteMessages(guid_gap, [msgID])
                                return "delete link"
                                break
                            else:
                                break
                        else:
                            break
                    elif type(admins) == list and admins != []:
                        msgID = msg.get("message_id")
                        if (
                            msg["type"] == "Text"
                            and not "forwarded_from" in msg.keys()
                            and not msg["author_object_guid"] in admins
                        ):
                            if (
                                findall(r"https://rubika.ir/joing/\w{32}", msg["text"])
                                or findall(
                                    r"https://rubika.ir/joinc/\w{32}", msg["text"]
                                )
                                or findall(r"https://rubika.ir/\w{32}", msg["text"])
                                or findall(r"https://\w", msg["text"])
                                or findall(r"http://\w", msg["text"])
                                or findall(r"@\w", msg["text"]) != []
                            ):
                                self.bot.deleteMessages(guid_gap, [msgID])
                                return "delete link"
                                break
                            else:
                                break
                        else:
                            break
                except:
                    continue
        else:
            raise TypeAnti("The TypeAnti entered is incorrect")
