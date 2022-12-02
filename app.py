import mqtt
import json
import led
import uasyncio as asyncio

_led = led.Led()
task = None


def on_wake_up():
    print("on wake up")
    mqtt.connect(on_command)
    while True:
        asyncio.run(start())


async def check_msg():
    while True:
        while _led.in_progress:
            mqtt.check_msg()
            await asyncio.sleep_ms(500)
        mqtt.wait_for_msg()


async def start():
    await asyncio.create_task(check_msg())


def on_command(topic, msg):
    print(f'new msg (%s, %s)', (topic, msg))
    try:
        jmsg = json.loads(msg)
        global task
        if task:
            task.cancel()

        if jmsg["action"] is "off":
            print('cmd: off')
            _led.in_progress = True
            task = asyncio.create_task(_led.fade(0, 0, 0))
        elif jmsg["action"] is "demo":
            print('cmd: demo')
            _led.in_progress = True
            task = asyncio.create_task(_led.demo())
    except Exception as e:
        print(str(e))
        return


