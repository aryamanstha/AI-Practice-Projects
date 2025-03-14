import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    urls=[
    'https://api.zippopotam.us/us/33162'
    ]
    async with aiohttp.ClientSession() as session:
        data=[fetch(session, url) for url in urls]
        results=await asyncio.gather(*data)
        print(results)
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print("Exception: ", e)
