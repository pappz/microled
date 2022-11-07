import asyncio
import time
from threading import Thread
from lib.queue import Queue

task_list = []

async def async_func():
    print('1. Velotio ...')
    await asyncio.sleep(2)
    print('1. ... Blog!')


async def async_func2():
    print('2. Velotio ...')
    await asyncio.sleep(2)
    print('2. ... Blog!')


async def start(tasks):
    while True:
        for t in tasks:
            print("new task")
            await t
        time.sleep(0.1)


def looper(tasks):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start(tasks))
    # asyncio.run(start(tasks))


def main():
    print("starting thread")
    t = Thread(target=looper, args=(task_list,), daemon=True)
    t.start()
    time.sleep(1)


class LedService:
    active_task = None
    loop = asyncio.get_event_loop()

    queue = Queue(1)

    def __init__(self):
        t = Thread(target=self.__looper, daemon=True)
        t.start()

    def __looper(self):
        # self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.__handler())

    async def __handler(self):
        while True:
            task = self.queue.get()
            await task

    def demo(self):
        task = self.loop.create_task(self.__start_demo())
        print("write to queue")
        self.active_task = task
        self.queue.put(task)

    def off(self):
        self.stop()
        task = self.loop.create_task(self.__off())
        self.queue.put(task)

    async def __start_demo(self):
        while True:
            for i in range(1, 5):
                print(i)
                time.sleep(1)
            print("this is demo")
            await asyncio.sleep(1)

    def stop(self):
        self.active_task.cancel()

    async def __off(self):
        print("off")


s = LedService()
s.demo()
time.sleep(2)
print("try to stop")
s.off()
print("sleep 10")
time.sleep(10)
