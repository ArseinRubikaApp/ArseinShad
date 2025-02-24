from random import randint


def TypeText(Type: str = None, text: str = None, link: str = None, guid: str = None):
    if Type == "MentionText":
        if guid and text != None:
            if guid.startswith("u0"):
                typeMention = "User"
            return [
                {
                    "type": "MentionText",
                    "mention_text_object_guid": guid,
                    "from_index": 0,
                    "length": len(text),
                    "mention_text_object_type": typeMention,
                }
            ]
    elif Type != "MentionText" and Type != "hyperlink":
        return [{"from_index": 0, "length": len(text), "type": Type}]
    elif Type == "hyperlink":
        return [
            {
                "from_index": 0,
                "length": len(text),
                "link": {"hyperlink_data": {"url": link}, "type": "hyperlink"},
                "type": "Link",
            }
        ]


def makeJsonResend(guid, file_inline):
    return {
        "object_guid": guid,
        "rnd": randint(100000, 999999999),
        "file_inline": file_inline,
        "text": "868937185613347",
    }


def deleteRSAset(key):
    return key.replace("-----BEGIN RSA PRIVATE KEY-----\n", "").replace(
        "\n-----END RSA PRIVATE KEY-----", ""
    )
