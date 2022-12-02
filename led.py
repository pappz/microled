import uasyncio as asyncio

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
    color = (0, 0, 0)
    np = neopixel.NeoPixel(Pin(0), 144)
    in_progress = False

    def __init__(self):
        #self.demo()
        pass

    def run_effect(self):
        n = 144
        width = 10
        color = (100, 100, 100)
        for i in range(0, n+width):
            if i < n:
                self.np[i] = color

            if i >= width:
                self.np[i-width] = (0,0,0)

            self.np.write()
            time.sleep_ms(25)

    def fade_out(self):
        n = 144
        for i in range(n-1, -1, -1):
            self.np[i] = (0, 0, 0)
            self.np.write()
            time.sleep_ms(5)

    async def fade(self, r, g, b, max_steps=50, sleep_time=None):
        await self.__fade(r,g,b, max_steps, sleep_time)
        self.in_progress = False

    async def __fade(self, r, g, b, max_steps=50, sleep_time=None):
        diff = [0] * 3
        diff[0] = self.color[0] - r
        diff[1] = self.color[1] - g
        diff[2] = self.color[2] - b
        n_steps = self.__calc_steps(max_steps, diff)

        diff[0] = diff[0] / n_steps
        diff[1] = diff[1] / n_steps
        diff[2] = diff[2] / n_steps
        float_color = list(self.color)
        for i in range(1, n_steps):
            float_color[0] -= diff[0]
            float_color[1] -= diff[1]
            float_color[2] -= diff[2]
            self.color = tuple([round(float_color[0]), round(float_color[1]),round(float_color[2])])
            self.np.fill(self.color)
            self.np.write()
            if sleep_time:
                await asyncio.sleep(sleep_time)

        self.color = (r, g, b)
        self.np.fill(self.color)
        self.np.write()

    async def demo(self):
        print('start demo')
        color = hsl_to_rgb(300, 70, 30)
        await self.__fade(color[0], color[1], color[2], max_steps=255)
        await asyncio.sleep(5)

        while True:
            h = self.__random_range(0, 360)
            s = self.__random_range(70, 80)
            color = hsl_to_rgb(h, s, 30)
            await self.__fade(color[0], color[1], color[2], max_steps=255, sleep_time=self.__random_range(0.3, 0.5))
            await asyncio.sleep(self.__random_range(14, 19))

    @staticmethod
    def __calc_steps(max_steps, diff):
        highest_diff = max(abs(i) for i in diff)
        return min([highest_diff, max_steps])

    @staticmethod
    def __random_range(i, j):
        b = getrandbits(16)
        diff = abs(j - i)
        ration = b / 65535
        return i + int(diff * ration)
