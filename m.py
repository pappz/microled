
color = [1,2,3]


def __calc_steps(max_steps, diff):
    highest_diff = max(abs(i) for i in diff)
    return min([highest_diff, max_steps])


def fade(r, g, b, max_steps=50, sleep_time=None):
    global color
    diff = [0] * 3

    diff[0] = color[0] - r
    diff[1] = color[1] - g
    diff[2] = color[2] - b

    n_steps = __calc_steps(max_steps, diff)

    for i in range(0, 3):
        diff[i] = int(diff[i] / n_steps)

    for i in range(1, n_steps+1):
        color = (color[0] - diff[0], color[1] - diff[1], color[2] - diff[2])
        '''
        if sleep_time is not None:
            time.sleep(sleep_time)
        '''
    color = (r, g, b)

fade(255, 255, 255, 10)