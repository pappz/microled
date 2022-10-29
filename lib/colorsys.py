"""Conversion functions between RGB and other color systems.
This modules provides two functions for each color system ABC:
  rgb_to_abc(r, g, b) --> a, b, c
  abc_to_rgb(a, b, c) --> r, g, b
All inputs and outputs are triples of floats in the range [0.0...1.0].
Inputs outside the valid range may cause exceptions or invalid outputs.
Supported color systems:
RGB: Red, Green, Blue components
HLS: Hue, Luminance, Saturation
HSV: Hue, Saturation, Value

origin source: https://docs.python.org/3/library/colorsys.html
"""

# References:
# http://en.wikipedia.org/wiki/YIQ
# http://en.wikipedia.org/wiki/HLS_color_space
# http://en.wikipedia.org/wiki/HSV_color_space

__all__ = ["rgb_to_hls", "hls_to_rgb"]


ONE_THIRD = 1.0/3.0
ONE_SIXTH = 1.0/6.0
TWO_THIRD = 2.0/3.0


def rgb_to_hls(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    sumc = (maxc+minc)
    rangec = (maxc-minc)
    l = sumc/2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = rangec / sumc
    else:
        s = rangec / (2.0-sumc)
    rc = (maxc-r) / rangec
    gc = (maxc-g) / rangec
    bc = (maxc-b) / rangec
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, l, s


def hls_to_rgb(h, l, s):
    if s == 0.0:
        return l, l, l
    if l <= 0.5:
        m2 = l * (1.0+s)
    else:
        m2 = l+s-(l*s)
    m1 = 2.0*l - m2
    return _v(m1, m2, h + ONE_THIRD), _v(m1, m2, h), _v(m1, m2, h - ONE_THIRD)


def _v(m1, m2, hue):
    hue = hue % 1.0
    if hue < ONE_SIXTH:
        return m1 + (m2-m1)*hue*6.0
    if hue < 0.5:
        return m2
    if hue < TWO_THIRD:
        return m1 + (m2-m1)*(TWO_THIRD-hue)*6.0
    return m1