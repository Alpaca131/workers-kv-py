import aiohttp


async def get(url, headers: dict):
    async with aiohttp.request("GET", url, headers=headers) as resp:
        if resp.status == 404:
            return None
        if resp.status not in (200, 304):
            raise Exception(await resp.text())
        return await resp.text()


async def put(url, headers: dict, data=None):
    async with aiohttp.request("PUT", url, json=data, headers=headers) as resp:
        if resp.status not in (200, 304):
            raise Exception(await resp.text())
        return await resp.text()


async def delete(url, headers: dict, data=None):
    async with aiohttp.request("DELETE", url, json=data, headers=headers) as resp:
        if resp.status not in (200, 304):
            raise Exception(await resp.text())
        return await resp.text()
