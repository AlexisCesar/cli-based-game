from pynput import keyboard

default_map_size = 20

map = list()

id_counter = 0
for i in range(default_map_size):
    layer = list()

    layer.append(id_counter)
    id_counter = id_counter + 1

    for j in range(default_map_size):
        layer.append(' ')
    map.append(layer)

for layer in map:
    if layer[0] == 0 or layer[0] == (default_map_size - 1):
        layer_aux = list()
        layer_aux.append(layer[0])
        for i in range(default_map_size):
            layer_aux.append('-')
        map[map.index(layer)] = layer_aux
    for index, column in enumerate(layer):
        if index == 1 or index == (default_map_size):
            layer[index] = '|'


def printMap():
    print('\n' * 100)
    for layer in map:
        for index, column in enumerate(layer[1:]):
            print(column, end=' ')
        print()

player_column = player_row = 0
player_column = int(default_map_size / 2)
player_row = (default_map_size - 2)
map[player_row][player_column] = 'X'

printMap()


def on_press(key):
    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in ['w', 'a', 's', 'd']:
        performMove(k)


def performMove(key):
    global player_row
    global player_column

    if key == 'w':
        if map[(player_row - 1)][(player_column)] == ' ':
            map[player_row][player_column] = ' '
            player_row = player_row - 1
            map[player_row][player_column] = 'X'
    elif key == 'a':
        if map[(player_row )][(player_column - 1)] == ' ':
            map[player_row][player_column] = ' '
            player_column = player_column - 1
            map[player_row][player_column] = 'X'
    elif key == 's':
        if map[(player_row + 1)][(player_column)] == ' ':
            map[player_row][player_column] = ' '
            player_row = player_row + 1
            map[player_row][player_column] = 'X'
    elif key == 'd':
        if map[(player_row )][(player_column + 1)] == ' ':
            map[player_row][player_column] = ' '
            player_column = player_column + 1
            map[player_row][player_column] = 'X'
    printMap()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

listener = keyboard.Listener(on_press=on_press)
listener.start()
