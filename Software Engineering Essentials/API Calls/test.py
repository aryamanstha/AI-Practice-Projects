import asyncio
import aiohttp
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt


REQUESTS_PER_SECOND = 5  
TIME_PERIOD = 10

@sleep_and_retry
@limits(calls=REQUESTS_PER_SECOND, period=TIME_PERIOD)
@retry(stop=stop_after_attempt(15))
async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 429:  
            raise Exception("Rate limit exceeded, retrying...")
        response.raise_for_status()  
        return await response.json()

async def main():
    urls=[
    'https://api.zippopotam.us/us/33162',
    'https://api.zippopotam.us/us/64093'
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
