import os

isWindows = os.name == 'nt'

addstr = None
move = None

if isWindows:
    import ctypes
    from ctypes import c_long, c_wchar_p, c_ulong, c_void_p

    # ==== GLOBAL VARIABLES ======================

    gHandle = ctypes.windll.kernel32.GetStdHandle(c_long(-11))

    def _move(x, y):
        # Move cursor to position indicated by x and y.
        value = x + (y << 16)
        ctypes.windll.kernel32.SetConsoleCursorPosition(
            gHandle, c_ulong(value))
    move = _move

    def _addstr(string):
        # Write string
        ctypes.windll.kernel32.WriteConsoleW(gHandle, c_wchar_p(
            string), c_ulong(len(string)), c_void_p(), None)
    addstr = _addstr
else:
    def _move(x, y):
        return print("\033[l;cH")
    move = _move
    addstr = print
