import requests
import aiohttp
import asyncio
import aiofiles
import time
import ssl

# Change the header to your System/ PC
USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


async def download_page(session, url, item, timestr):
    """this is the function which calls individual requests"""
    response = await session.request(method="GET", url=url, ssl=gcontext)
    filename = item + timestr + ".txt"
    async with aiofiles.open(filename, "ba") as f:
        async for content in response.content.iter_chunked(1024):
            await f.write(content)
    return filename


async def download_all_pages(timestr, list_items):
    """This is the functon which loops over all the requests"""
    timeout = aiohttp.ClientTimeout(total=10 * 60)
    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(
        connector=connector, headers=USER_AGENT, timeout=timeout
    ) as session:  #
        tasks = []
        for item in list_items:
            search_url = "https://www.google.de/search?" + item
            task_asyn = asyncio.ensure_future(
                download_page(session, search_url, item, timestr)
            )
            tasks.append(task_asyn)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    dummy_list = ["alpha", "beta"]
    timestr = time.strftime("%Y%m%d-%H%M%S")

    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_pages(timestr, dummy_list))
    print("Finish")
