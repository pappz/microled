from umqtt.simple import MQTTClient
import config
import utime


_c = MQTTClient("led", config.mqtt_address, 1883, config.mqtt_user, config.mqtt_pwd, 0)
_topic = "kesmarki/led"


def connect(cb):
    _c.set_callback(cb)
    reconnect()


def reconnect():
    while 1:
        try:
            print("try to connect")
            _c.connect(True)
            _c.subscribe(_topic)
            return
        except OSError as e:
            utime.sleep(2)


def wait_for_msg():
    while 1:
        try:
            print("wait for msg")
            _c.wait_msg()
        except OSError as e:
            print("mqtt: %r" % e)
            reconnect()
