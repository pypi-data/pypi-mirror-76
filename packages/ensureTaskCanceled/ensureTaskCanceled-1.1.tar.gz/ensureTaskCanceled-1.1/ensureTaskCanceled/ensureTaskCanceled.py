import asyncio


async def ensureTaskCanceled(asyncio_task: asyncio.Task) -> None:
    while not asyncio_task.done():
        try:
            asyncio_task.cancel()
        except:
            pass
        finally:
            await asyncio.sleep(0)


if __name__ == '__main__':
    async def main():
        task = asyncio.create_task(asyncio.sleep(10))
        await asyncio.sleep(2)
        await ensureTaskCanceled(task)
        print(task)


    asyncio.run(main())
