import os,sys

isWindows = os.name == 'nt'

addstr = None
move = None

if isWindows:
    import ctypes
    from ctypes import c_long, c_wchar_p, c_ulong, c_void_p

    # ==== GLOBAL VARIABLES ======================

    gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

    def move(x, y):
        # Move cursor to position indicated by x and y.
        value = x + (y << 16)
        ctypes.windll.kernel32.SetConsoleCursorPosition(
            gHandle, c_ulong(value))

    def addstr(string):
        # Write string
        ctypes.windll.kernel32.WriteConsoleW(gHandle, c_wchar_p(
            string), c_ulong(len(string)), c_void_p(), None)
else:
    def move(x, y):
        return print("\033[%d;%dH" % (x,y),end='')
    addstr = sys.stdout.write
