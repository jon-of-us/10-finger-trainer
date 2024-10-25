

import sys
import os
# Windows
if os.name == 'nt':
    import msvcrt
    getwch = msvcrt.getwch

# Unix
else:
    import termios
    import tty
    def getwch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

