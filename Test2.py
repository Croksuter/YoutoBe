import asyncio
import time

async def wait():
    for i in range(5):
        await loop.run_in_executor(None, waiting)
    print("Done!")

def waiting():
    time.sleep(1)
    print(1)

async def main():
    await wait(), wait()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())