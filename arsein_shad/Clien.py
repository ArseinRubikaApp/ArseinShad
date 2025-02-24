class clien:
    def __init__(self, platform: str) -> dict:
        if platform == "android":
            self.platform = dict(
                {
                    "app_name": "Main",
                    "app_version": "3.5.5",
                    "lang_code": "fa",
                    "package": "ir.medu.shad",
                    "temp_code": "31",
                    "platform": "Android",
                }
            )
        elif platform == "web":
            self.platform = dict(
                {
                    "app_name": "Main",
                    "app_version": "4.4.7",
                    "platform": "Web",
                    "package": "web.shad.ir",
                    "lang_code": "fa",
                }
            )
        else:
            self.platform = dict(
                {
                    "app_name": "Main",
                    "app_version": "2.1.3",
                    "platform": "PWA",
                    "package": "my.shad.ir",
                    "lang_code": "fa",
                }
            )
