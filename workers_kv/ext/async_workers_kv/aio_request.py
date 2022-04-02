import aiohttp


async def get(url, headers: dict):
    async with aiohttp.request("GET", url, headers=headers) as resp:
        assert resp.status == 200
        return await resp.text()


async def put(url, headers: dict, data=None):
    async with aiohttp.request("PUT", url, data=data, headers=headers) as resp:
        assert resp.status == 200
        return await resp.text()


async def delete(url, headers: dict, data=None):
    async with aiohttp.request("DELETE", url, data=data, headers=headers) as resp:
        assert resp.status == 200
        return await resp.text()
