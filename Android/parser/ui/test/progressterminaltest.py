import time
import sys


def progress_test():
    bar_length = 20
    for percent in xrange(0, 100):
        hashes = '#' * int(percent / 100.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [%s] %d%%" % (hashes + spaces, percent))
        sys.stdout.flush()
        time.sleep(0.1)


progress_test()