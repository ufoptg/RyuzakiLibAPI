## RyuzakiLib API

## Disclaimer
```
        ⚠️ WARNING FOR YOU ️ ️⚠️
RyuzakiLib API is used to help your account activities on Telegram
We are not responsible for what you misuse in this repository
!  Be careful when using this repository!
If one of the members misuses this repository, we are forced to ban you
Never ever abuse this repository
```

- Tutorial FastAPI
```python
from fastapi import FastAPI
from RyuzakiLib.hackertools.chatgpt import RendyDevChat
from RyuzakiLib.hackertools.openai import OpenAiToken

app = FastAPI()

@app.get("/read")
def hello():
    return {"message": "Hello World"}

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0")
```

### How to secret via Hosting Cloud
```.env
MONGO_URL=url
REVERSE_IMAGE_API=apikey
OCR_API_KEY=apikey
ONLY_DEVELOPER_API_KEYS=random
HUGGING_TOKEN=apikey
SOURCE_UNSPLASH_URL=url
SOURCE_OCR_URL=url
SOURCE_ALPHA_URL=url
SOURCE_WAIFU_URL=url
SOURCE_TIKTOK_WTF_URL=url
SOURCE_TIKTOK_TECH_URL=url
DEVELOPER_ID=0
```
### Troubleshoot
Sometimes errors occur, but we are here to help! This guide covers some of the most common issues we’ve seen and how you can resolve them. However, this guide isn’t meant to be a comprehensive collection of every 🤗 FastAPI issue. For more help with troubleshooting your issue, try:
* [Contact Support](https://t.me/xtdevs)

### Contributing
* [Fork the project](https://github.com/TeamKillerX/RyuzakiLib) and send pull requests

### Credits
* [![TeamKillerX-Devs](https://img.shields.io/static/v1?label=TeamkillerX&message=devs&color=critical)](https://t.me/xtdevs)
* [FastApi](https://github.com/CYCNO/Direct-Download-API)
