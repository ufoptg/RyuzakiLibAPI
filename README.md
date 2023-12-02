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

### Contributing
* [Fork the project](https://github.com/TeamKillerX/RyuzakiLib) and send pull requests

### Credits
* [![TeamKillerX-Devs](https://img.shields.io/static/v1?label=TeamkillerX&message=devs&color=critical)](https://t.me/xtdevs)
* [FastApi](https://github.com/CYCNO/Direct-Download-API)
