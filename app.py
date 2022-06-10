try:
    from machine import Pin
    import neopixel
    import utime as time
except:
    from moc.machine import Pin
    import time

import mqtt
import json

_np = neopixel.NeoPixel(Pin(0), 144)


def on_command(topic, msg):
    print((topic, msg))
    try:
        color=json.loads(msg)
    except Exception as e:
        print(str(e))
        return

    _np.fill((color["r"], color["g"], color["b"]))
    _np.write()


def power_leds():
    _np.fill((0, 10, 0))
    _np.write()
    pass


def on_powered_on():
    print("on powered on")
    power_leds()


def on_wake_up():
    print("on wake up")
    mqtt.connect(on_command)
    mqtt.wait_for_msg()
