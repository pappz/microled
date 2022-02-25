try:
    import machine
    import utime as time
except:
    import moc.machine as machine
    import time

import config


_sleep_time = config.deep_sleep_period


def is_woke_from_deep_sleep():
    cause = machine.reset_cause()
    if cause is machine.PWRON_RESET:
        print("cause is PWRON_RESET reset")
    elif cause is machine.HARD_RESET:
        print("cause is HARD_RESET reset")
    elif cause is machine.WDT_RESET:
        print("cause is WDT_RESET reset")
    elif cause is machine.DEEPSLEEP_RESET:
        print("cause is DEEPSLEEP_RESET reset")
    elif cause is machine.SOFT_RESET:
        print("cause is SOFT_RESET reset")
    elif cause is 2:
        print("cause is CRASH")

    if cause == machine.DEEPSLEEP_RESET:
        return True
    else:
        return False


def require_sleep(time):
    global _sleep_time
    _sleep_time = time


def deep_sleep():
    rtc = machine.RTC()

    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, _sleep_time)

    machine.deepsleep()


def time_since_power_on():
    return time.time()