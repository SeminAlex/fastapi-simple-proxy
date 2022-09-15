import aiohttp
from typing import Union


class SingletonAiohttp:
    aiohttp_client = None

    @classmethod
    def get_aiohttp_client(cls):
        if cls.aiohttp_client is None:
            cls.aiohttp_client = aiohttp.ClientSession()
        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def query_url(cls, url: str, params: dict):
        client = cls.get_aiohttp_client()
        try:
            async with client.get(url, params=params) as response:
                if response.status != 200:
                    return None, {"ERROR": str(await response.text())}

                json_result = await response.json()
                headers = response.headers
        except Exception as e:
            return None, {"ERROR": e}
        return json_result, headers
