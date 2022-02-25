try:
    from machine import Pin
except:
    from moc.machine import Pin


_led = Pin(2, Pin.OUT)
_enabled = True


def blink():
    global _enabled
    if _enabled:
        _led.off()
    else:
        _led.on()

    _enabled = not _enabled
