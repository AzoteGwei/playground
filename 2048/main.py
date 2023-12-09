import keyboard
import datetime
import random

board : list[list[int]] = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

COLOR_MAP : dict[int,str] = {
    0:   '\x1b[1;30;40m',
    2:   '\x1b[1;31;40m',
    4:   '\x1b[1;31;40m',
    8:   '\x1b[1;31;40m',
    16:  '\x1b[1;32;40m',
    32:  '\x1b[1;32;40m',
    64:  '\x1b[1;32;40m',
    128: '\x1b[1;33;40m',
    256: '\x1b[1;34;40m',
    512: '\x1b[1;35;40m',
    1024:'\x1b[1;36;40m',
    2048:'\x1b[1;37;40m',
}

keyboard_data : dict[str,int] = {
    'lastkey' : (0,0),
    'time' : 0
}

def render(board : list[list[int]]) -> None:
    for row in board:
        for colomn in row:
            print(COLOR_MAP[colomn if colomn <= 2048 else 2048] + "%4d" % colomn + '\x1b[0m',end=" ")
        print("")
    return

def check_fail(board : list[list[int]]) -> bool:
    full = True
    dead = True
    for row in board:
        for colomn in row:
            full = full if not colomn == 0 else False
    if full:
        for row in range(len(board)):
            for colomn in range(len(board[row])):
                if not row == 0:
                    dead = dead if not board[row][colomn] == board[row - 1][colomn] else False
                if not colomn == 0:
                    dead = dead if not board[row][colomn] == board[row][colomn - 1] else False
    return full and dead

def check_keyboard(keyboard_data : dict[str,int]) -> tuple[int]:
    if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
        if keyboard_data['lastkey'] == (0,1) and int(datetime.datetime.now().timestamp() * 1000) - keyboard_data['time'] > 500:
            keyboard_data['time'] = int(datetime.datetime.now().timestamp() * 1000)
            return (0,1)
        else:
            if keyboard_data['lastkey'] != (0,1):
                keyboard_data['lastkey'] = (0,1)
                return (0,1)
    if keyboard.is_pressed('down') or keyboard.is_pressed('s'):
        if keyboard_data['lastkey'] == (0,-1) and int(datetime.datetime.now().timestamp() * 1000) - keyboard_data['time'] > 500:
            keyboard_data['time'] = int(datetime.datetime.now().timestamp() * 1000)
            return (0,-1)
        else:
            if keyboard_data['lastkey'] != (0,-1):
                keyboard_data['lastkey'] = (0,-1)
                return (0,-1)
    if keyboard.is_pressed('left') or keyboard.is_pressed('a'):
        if keyboard_data['lastkey'] == (-1,0) and int(datetime.datetime.now().timestamp() * 1000) - keyboard_data['time'] > 500:
            keyboard_data['time'] = int(datetime.datetime.now().timestamp() * 1000)
            return (-1,0)
        else:
            if keyboard_data['lastkey'] != (-1,0):
                keyboard_data['lastkey'] = (-1,0)
                return (-1,0)
    if keyboard.is_pressed('right') or keyboard.is_pressed('d'):
        if keyboard_data['lastkey'] == (1,0) and int(datetime.datetime.now().timestamp() * 1000) - keyboard_data['time'] > 500:
            keyboard_data['time'] = int(datetime.datetime.now().timestamp() * 1000)
            return (1,0)
        else:
            if keyboard_data['lastkey'] != (1,0):
                keyboard_data['lastkey'] = (1,0)
                return (1,0)
    return (0,0)

def insert_block(board : list[list[int]],fail : int = 0) -> None:
    if fail >= 10:
        for row in range(len(board)):
            for colomn in range(len(board[row])):
                if board[row][colomn] == 0:
                    board[row][colomn] = 2
                    return
        return
    rand = int(random.random() * 100)
    to_insert_num = 2 if get_max(board) <= 256 else int(get_max(board) / 256) * 4
    for row in range(len(board)):
            for colomn in range(len(board[row])):
                if board[row][colomn] == 0:
                    if int(random.random() * 100) + 10 < rand:
                        board[row][colomn] = to_insert_num
                        return
    if check_fail(board):
        return
    else:
        insert_block(board,fail + 1)

def get_max(board : list[list[int]]) -> int:
    max_num = 0
    for row in board:
        for colomn in row:
            max_num = max(colomn,max_num)
    return max_num

def move(board: list[list[int]], direction: tuple[int]) -> list[list[int]]:
    new_board = [[0] * 4 for _ in range(4)]

    if direction == (0, 1):  # up
        for column in range(4):
            i = 0
            for row in range(4):
                if board[row][column] != 0:
                    if new_board[i][column] == 0:
                        new_board[i][column] = board[row][column]
                    elif new_board[i][column] == board[row][column]:
                        new_board[i][column] *= 2
                        i += 1
                    else:
                        i += 1
                        new_board[i][column] = board[row][column]
    elif direction == (0, -1):  # down
        for column in range(4):
            i = 3
            for row in range(3, -1, -1):
                if board[row][column] != 0:
                    if new_board[i][column] == 0:
                        new_board[i][column] = board[row][column]
                    elif new_board[i][column] == board[row][column]:
                        new_board[i][column] *= 2
                        i -= 1
                    else:
                        i -= 1
                        new_board[i][column] = board[row][column]
    elif direction == (-1, 0):  # left
        for row in range(4):
            i = 0
            for column in range(4):
                if board[row][column] != 0:
                    if new_board[row][i] == 0:
                        new_board[row][i] = board[row][column]
                    elif new_board[row][i] == board[row][column]:
                        new_board[row][i] *= 2
                        i += 1
                    else:
                        i += 1
                        new_board[row][i] = board[row][column]
    elif direction == (1, 0):  # right
        for row in range(4):
            i = 3
            for column in range(3, -1, -1):
                if board[row][column] != 0:
                    if new_board[row][i] == 0:
                        new_board[row][i] = board[row][column]
                    elif new_board[row][i] == board[row][column]:
                        new_board[row][i] *= 2
                        i -= 1
                    else:
                        i -= 1
                        new_board[row][i] = board[row][column]
    return new_board

if __name__ == '__main__':
    print("\033c",end="")
    insert_block(board,0)
    insert_block(board,0)
    render(board=board)
    while True:
        direction = check_keyboard(keyboard_data=keyboard_data)
        if direction == (0,0):
            continue
        board = move(board=board,direction=direction)
        if check_fail(board=board):
            break
        insert_block(board=board)
        print("\033c",end="")
        render(board=board)
    print("Game Over!")