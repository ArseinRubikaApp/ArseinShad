from random import choices


class DeviceTelephone:
    DeviceAndroid: dict = {
        "app_version": "MA_3.5.5",
        "device_hash": "".join(choices("0123456789", k=26)),
        "device_model": "Arsein-library",
        "is_multi_account": False,
        "lang_code": "fa",
        "system_version": "SDK 28",
        "token": "",
        "token_type": "Firebase",
    }

    DeviceWeb: dict = {
        "app_version": "WB_4.4.7",
        "device_hash": "".join(choices("0123456789", k=26)),
        "device_model": "Arsein-library",
        "is_multi_account": False,
        "lang_code": "fa",
        "system_version": "Windows 11",
        "token": "",
        "token_type": "Web",
    }
