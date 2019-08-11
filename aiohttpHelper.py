import aiohttp, asyncio

async def main(pool):
    sem = asyncio.Semaphore(pool)
    async with aiohttp.ClientSession() as session:
        tasks = []
        [tasks.append(control_sem(sem, 'https://api.github.com/events?a={}'.format(i), session)) for i in range(10)]
        await asyncio.wait(tasks)

async def control_sem(sem, url, session):
    async with sem:
        await fetch(url, session)

async def fetch(url, session):
    async with session.get(url) as resp:
        json = await resp.json()
        print(json)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(pool=2))
