import requests
import aiohttp

class taromaru():
    """
        If your looking for async, use `taromaruasync()`

        Example:
        ```py
        taromaru = taromaru("Apikey")
        print(taromaru.image(taromaru))
        ```

        Result:
        ```json
        {"error": "false", "image": "url"}
        ```

        Current api calls:
            - image(type)
    """

    def __init__(self, apikey: str):
        self.apikey = apikey

    def image(self, type):
        r = requests.get(f'https://taromaruapi.cu.ma/api/{type}/', params={
            "apikey": self.apikey
        })
        return r.json()

class taromaruasync():
    """
        If you do not want async, use `taromaru()`

        Example:
        ```py
        taromaru = taromaru("Apikey")
        print(taromaru.image(taromaru))
        ```

        Result:
        ```json
        {"error": "false", "image": "url"}
        ```

        Current api calls:
            - image(type)
    """

    def __init__(self, apikey: str):
        self.apikey = apikey

    async def image(self, type):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://taromaruapi.cu.ma/api/{type}/', params={
                "apikey": self.apikey
            }) as resp:
                return await resp.json()