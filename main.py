from readchar import readkey
from json import load, dump
import caveman
from argparse import ArgumentParser
from sys import stdout
from colorama import Fore, Back, init
Config = {
    'listFile': 'list.json',
    'MovementBase': '\x1b[',
    'up': 'A',
    'down': 'B',
    'right': 'C',
    'left': 'D',
    'exit': '\x05',
    'save': '\x13',
    'enter': '\r'
}


def _print(*args, **kwargs):
    '''Print without newline, because adding parameter end='' looks ugly'''
    kwargs['end'] = ''
    stdout.write("\033[K")
    print(*args, **kwargs)


def GetTodo():
    '''Gets Todo from json file named in config.'''
    File = open(Config['listFile'], 'r')
    return load(File)


def CheckIfFileExists():
    try:
        open(Config['listFile'], 'r')
    except:
        open(Config['listFile'], 'w').write('[]')


def _ArgumentParser():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="To-Do File")
    args = parser.parse_args()
    if args.file:
        Config['listFile'] = args.file


def Init():
    init()
    stdout.write(Fore.RED)
    _ArgumentParser()
    CheckIfFileExists()


def DisplayLists(Cursor, Lists):
    caveman.move(0, 0)
    for Index, List in enumerate(Lists):
        stdout.write(Fore.RED)
        if Index == Cursor[1]:
            stdout.write(Fore.BLUE)
        caveman.addstr(f'[{"x" if List["checked"] else " "}] {List["name"]}\n')


def Save(Lists):
    FileName = Config['listFile']
    File = open(FileName, 'w')
    dump(Lists, File, indent=4, sort_keys=True)


def IsVaildMove(pos1, pos2):
    '''pos1 should be in range of pos2's list.Returns True if vaild,False if not'''
    for _pos2 in pos2:
        for _pos1 in pos1:
            if _pos1 < 0:
                return False
            if _pos1 >= _pos2:
                return False
    return True


def CheckMovement(Cursor, Key, Lists):
    '''Handles key events'''
    Up = Config['MovementBase']+Config['up']
    Down = Config['MovementBase']+Config['down']
    if Up == Key:
        if IsVaildMove([0, Cursor[1]-1], [len(Lists), len(Lists)]):
            Cursor[1] -= 1
    elif Down == Key:
        if IsVaildMove([0, Cursor[1]+1], [len(Lists), len(Lists)]):
            Cursor[1] += 1
    return Cursor


def Prompt(PlaceHolder, Cursor):
    caveman.move(10, 5)
    NewName = input('Task Name:')

    caveman.move(10, 5)
    stdout.write("\033[K")
    caveman.move(*Cursor)
    return NewName


def Main():
    Lists = GetTodo()
    Cursor = [0, 0]
    Key = ''
    while Key != Config['exit']:
        ToPrint = f'{Cursor[1]}'
        if Key == Config['save']:
            Save(Lists)
            ToPrint += f'| Saved in {Config["listFile"]}'
        elif Config['enter'] == Key:
            Lists[Cursor[1]]['checked'] = not Lists[Cursor[1]]['checked']
        elif Key == 'r':
            Lists[Cursor[1]]['name'] = Prompt('Task Name:', Cursor)
        elif Key == 'n':
            Dummy = {}
            Dummy['name'] = Prompt('Name:', Cursor)
            Dummy['checked'] = False
            Lists.append(Dummy)
        elif Key == '\x1b[3~':
            del Lists[Cursor[1]]  # Delete
            if Cursor[1] != 0:
                Cursor[1] -= 1
        else:
            Cursor = CheckMovement(Cursor, Key, Lists)
        stdout.write("\033[?25l")
        DisplayLists(Cursor, Lists)
        stdout.write("\033[?25h")
        stdout.write(Fore.LIGHTYELLOW_EX)
        print(ToPrint)
        caveman.move(*Cursor)

        Key = readkey()
        pass

    return 0


if __name__ == '__main__':
    Init()
    Main()
