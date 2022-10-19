try:
    from random import getrandbits
    from machine import Pin
    import neopixel
    import utime as time
except:
    from moc.machine import Pin
    import time


def hsl_to_rgb(i_h, i_s, i_l):

    h = (i_h % 360) / 360.0
    s = i_s / 100.0
    l = i_l / 100.0

    if s == 0:
        r = g = b = 255 * l
        return int(r), int(g), int(b)

    t1 = 0
    if l < 0.5:
        t1 = l * (1.0 + s)
    else:
        t1 = l + s - l * s

    t2 = 2 * l - t1
    tr = h + 1 / 3.0
    tg = h
    tb = h - 1 / 3.0

    r = hsl_convert(tr, t1, t2)
    g = hsl_convert(tg, t1, t2)
    b = hsl_convert(tb, t1, t2)

    return r, g, b


def hsl_convert(c, t1,t2):
    if c < 0:
        c += 1
    elif c > 1:
        c -= 1

    if 6 * c < 1 :
        c = t2 + ( t1 - t2 ) * 6 * c
    elif 2 * c < 1:
        c = t1
    elif 3 * c < 2:
        c = t2 + ( t1 - t2 ) * ( 2 / 3.0 - c ) * 6
    else:
        c = t2

    return int(c * 255)


class Led:
    color = (100, 100, 100)
    np = neopixel.NeoPixel(Pin(0), 144)

    def __init__(self):
        self.demo()

    def fade(self, r, g, b, max_steps=50, sleep_time=None):
        new_color = [0] * 3
        diff = [0] * 3

        diff[0] = self.color[0] - r
        diff[1] = self.color[1] - g
        diff[2] = self.color[2] - b
        n_steps = self.__calc_steps(max_steps,diff)
        for i in range(1, n_steps):
            new_color[0] = self.color[0] - int(i * diff[0] / n_steps)
            new_color[1] = self.color[1] - int(i * diff[1] / n_steps)
            new_color[2] = self.color[2] - int(i * diff[2] / n_steps)

            self.np.fill(tuple(new_color))
            self.np.write()
            if sleep_time is not None:
                time.sleep(sleep_time)

        self.color = (r, g, b)
        self.np.fill(self.color)
        self.np.write()

    def demo(self):
        l = 30
        while True:
            h = self.__random_range(0, 360)
            s = self.__random_range(0, 100)
            color = hsl_to_rgb(h, s, l)
            self.fade(color[0], color[1], color[2], max_steps=255, sleep_time=self.__random_range(0.3, 0.5))
            time.sleep(self.__random_range(15, 30))

    def __calc_steps(self, max_steps, diff):
        highest_diff = max(abs(i) for i in diff)
        return min([highest_diff, max_steps])

    def __random_range(self, i, j):
        b = getrandbits(16)
        diff = abs(j - i)
        ration = b / 65535
        return i + int(diff * ration)
