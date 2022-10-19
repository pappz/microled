try:
    from machine import Pin
    import neopixel
    import utime as time
except:
    from moc.machine import Pin
    import time


class Led:
    color = (100, 100, 100)
    np = neopixel.NeoPixel(Pin(0), 144)

    def fade(self, r, g, b):
        new_color = [0] * 3
        diff = [0] * 3

        diff[0] = self.color[0] - r
        diff[1] = self.color[1] - g
        diff[2] = self.color[2] - b
        n_steps = self.__calc_steps(diff)
        print("fade steps: ", n_steps)
        for i in range(1, n_steps):
            new_color[0] = self.color[0] - int(i * diff[0] / n_steps)
            new_color[1] = self.color[1] - int(i * diff[1] / n_steps)
            new_color[2] = self.color[2] - int(i * diff[2] / n_steps)

            self.np.fill(tuple(new_color))
            self.np.write()

        self.color = (r, g, b)
        self.np.fill(self.color)
        self.np.write()

    def __calc_steps(self, diff):
        highest_diff = max(abs(i) for i in diff)
        return min([highest_diff, 50])


