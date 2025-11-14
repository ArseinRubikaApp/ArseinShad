import os
import re
from setuptools import setup,find_packages


requires = ["pycryptodome==3.16.0","aiohttp==3.8.3","asyncio==3.4.3","httpx==0.26.0","tinytag==1.10.1","mutagen==1.47.0","pillow==12.0.0","httpx[http2]","nest_asyncio==1.6.0"]
_long_description = """

## ArseinShad

> Elegant, modern and asynchronous Shad MTProto API framework in Python for users and bots

<p align="center">
    <img src="https://s6.uupload.ir/files/img_20240111_123815_369_5ni9.jpg" alt="ArseinShad" width="128">
    <br>
    <b>library Arsein Shad</b>
    <br>
</p>

###  Arsein library documents soon...


### How to import the Shad's library

``` bash
from arsein_shad import Messenger

Or

from arsein_shad import Robot_Shad
```

### How to import the anti-advertising class

``` bash
from arsein_shad.Zedcontent import Antiadvertisement
```

### How to install the library

``` bash
pip install arseinshad==1.0.0
```

### My ID in Telegram

``` bash
@Team_Arsein
```
## An example:
``` python
from arsein_shad import Messenger

bot = Messenger("Your Auth Account"," key Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"libraryArsein")
```

## And Or:
``` python
from arsein_shad import Robot_Shad

bot = Robot_Shad("Your Auth Account"," key Account")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"libraryArsein")
```

## Or if the privatekey was decoded under the web
``` python
from arsein_shad import Messenger

bot = Messenger("Your Auth Account"," key Account","web")

gap = "your guid or gap or pv or channel"

bot.sendMessage(gap,"libraryArsein")
```


### Installing

``` bash
pip install arseinshad==1.0.0
```

### Or

> And if pip was filtered, enter the following code in the terminal to install the library

``` bash
pip install --trusted-host https://pypi.tuna.tsinghua.edu.cn -i https://pypi.tuna.tsinghua.edu.cn/simple/arseinshad==1.0.0
```


Made by Team ArianBot

Address of our team's GitHub :

https://github.com/Arseinlibrary/Arsein__library.git


### Key Features

- **Ready**: Install ArseinShad with pip and start building your applications right away.
- **Easy**: Makes the Shad API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by pycryptodome, a high-performance cryptography library written in C.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Shad's API to execute any official client action and more.


### Our channel in messengers

``` bash
Our channel in Ita

https://eitaa.com/ArseinTeam

Our channel in Soroush Plus

https://splus.ir/ArseinTeam

Our channel in Rubika

https://rubika.ir/Support_libdaryArseinRubika

Our channel in the Gap

https://gap.im/ArseinTeam

Our channel on Telegram

https://t.me/ArseinTeam
```
"""

setup(
    name = "ArseinShad",
    version = "1.0.0",
    author = "arian abasi nedamane",
    author_email = "aryongram@gmail.com",
    description = (" library Robot Shad"),
    license = "MIT",
    keywords = ["Arsein","Arseinshad","ArseinShad","arsein","bot","Bot","BOT","Robot","ROBOT","robot","self","api","API","Api","shad","Shad","SHAD","Python","python","aiohttp","asyncio","Arseinshad","ArseinShad"],
    url = "https://github.com/Arseinlibrary/Arsein__library.git",
    packages = find_packages(),
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    install_requires=requires,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
    ],
)
