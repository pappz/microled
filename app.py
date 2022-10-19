import mqtt
import json
import led

_led = led.Led()


def on_command(topic, msg):
    print((topic, msg))
    try:
        color=json.loads(msg)
    except Exception as e:
        print(str(e))
        return

    _led.fade(color["r"], color["g"], color["b"])


def power_leds():
    _led.fade(0, 10, 0)


def on_powered_on():
    print("on powered on")
    power_leds()


def on_wake_up():
    print("on wake up")
    mqtt.connect(on_command)
    mqtt.wait_for_msg()
