import blinker
import config
try:
    import network
    from micropython import const
    import utime as time
except:
    import moc.network as network
    from moc.micropython import const
    import time


class WifiError(Exception):
    def __init__(self):
        super(WifiError, self).__init__('network connection timed out')


_CONNECT_MAX_TRIES = const(10)
_tries = 0
_is_connected = False


def __connect():
    print("try connect to network")
    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(config.wifi_ssid, config.wifi_password)


def __has_reached_max_reconnection():
    global _tries
    print("wifi tries: {}".format(_tries))
    return _tries >= 10


def __increase_tries():
    global _tries
    _tries = _tries + 1


def connect_and_wait():
    global _is_connected
    if _is_connected:
        print("already connected to wifi")
        return

    global _tries
    blinker.on()
    _tries = 0
    __connect()
    while True:
        if not sta_if.isconnected():
            if __has_reached_max_reconnection():
                raise WifiError()

            __increase_tries()
            time.sleep(1)
            continue
        else:
            blinker.off()
            _is_connected = True
            return


def is_connected():
    return sta_if.isconnected()
