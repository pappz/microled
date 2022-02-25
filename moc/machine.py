from typing import Optional

IDLE = ...  # type: int
SLEEP = ...  # type: int
DEEPSLEEP = ...  # type: int

PWRON_RESET = ...  # type: int
HARD_RESET = ...  # type: int
WDT_RESET = ...  # type: int
DEEPSLEEP_RESET = ...  # type: int
PIN_WAKE = ...  # type: int
RTC_WAKE = ... # type: int


def reset() -> None:
    ...


def reset_cause():
    pass


def deepsleep():
    pass


def unique_id():
    return b"mocmachine"


class ADC:
    def __init__(self, port):
        pass

    def read(self):
        return 8


class Pin(object):
    OUT = ...

    def __init__(self, pin, direction):
        pass

    def on(self):
        pass

    def off(self):
        pass


class RTC(object):
    ALARM0 = ...

    def __init__(self):
        pass

    def datetime(self, tm=None):
        return 0

    def irq(self, trigger, wake):
        pass

    def alarm(self, alarm_id, time):
        pass


class UART(object):
    def __init__(self, id: int, baudrate: int = 115200) -> None:
        ...

    def init(self, baudrate: int, bits: int = 8, parity: Optional[int] = 0, stop: int = 1,
             timeout: int = 0, timeout_char: int = 0) -> None:
        ...

    def write(self, buf: bytearray) -> Optional[int]:
        """
        Write the buffer of bytes to the bus.

        :param buf: Data that needs to be written.
        :return: Number of bytes written or ``None`` on timeout.
        """
        ...

    def readinto(self, buf: bytearray, nbytes: Optional[int]):
        buf[0] = 0xff
        buf[1] = 0x86
        buf[2] = 0x00
        buf[3] = 0x00
        buf[4] = 0x00
        buf[5] = 0x00
        buf[6] = 0x00
        buf[7] = 0x00
        buf[8] = 0x7A

        return 9