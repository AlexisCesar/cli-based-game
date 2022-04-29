import random
from pynput import keyboard
import os

clearConsole = lambda: os.system('cls' if os.name=='nt' else 'clear')

DEFAULT_MAP_SIZE = 20

def generate_map():
    map = list()

    id_counter = 0
    for i in range(DEFAULT_MAP_SIZE):
        layer = list()

        layer.append(id_counter)
        id_counter = id_counter + 1

        for j in range(DEFAULT_MAP_SIZE):
            layer.append(' ')
        map.append(layer)

    for layer in map:
        if layer[0] == 0 or layer[0] == (DEFAULT_MAP_SIZE - 1):
            layer_aux = list()
            layer_aux.append(layer[0])
            for i in range(DEFAULT_MAP_SIZE):
                layer_aux.append('-')
            map[map.index(layer)] = layer_aux
        for index, column in enumerate(layer):
            if index == 1 or index == (DEFAULT_MAP_SIZE):
                layer[index] = '|'
    
    map[0][1] = '/'
    map[0][-1] = '\\'
    map[-1][1] = '\\'
    map[-1][-1] = '/'

    # Generate random door
    door_direction = random.choice(['n', 's', 'e', 'w'])
    indexes = list(range(0, DEFAULT_MAP_SIZE))[4:-4]

    if door_direction == 'n':
        map[0][random.choice(indexes)] = '#'

    elif door_direction == 's':
        map[-1][random.choice(indexes)] = '#'

    elif door_direction == 'e':
        map[random.choice(indexes)][-1] = '#'

    elif door_direction == 'w':
        map[random.choice(indexes)][1] = '#'

    return map


def print_map(map):
    clearConsole()
    for layer in map:
        for index, column in enumerate(layer[1:]):
            print(column, end=' ')
        print()


game_map = generate_map()

player_column = player_row = 0
player_column = int(DEFAULT_MAP_SIZE / 2)
player_row = (DEFAULT_MAP_SIZE - 2)
game_map[player_row][player_column] = 'X'

# Player status
player_money = 0
player_hp = 100
player_atk = 10

# Game status
current_room = 1

def print_hud():
    print('-' * DEFAULT_MAP_SIZE)
    print(f'${player_money}')
    print(f'HP: {player_hp}')
    print(f'ATK: {player_atk}')
    print(f'ROOM: {current_room}')
    print('-' * DEFAULT_MAP_SIZE)
    

def on_press(key):
    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in ['w', 'a', 's', 'd']:
        performMove(k)


print_map(game_map)
print_hud()

def performMove(key):
    global player_row
    global player_column
    global game_map
    global player_money
    global current_room

    if key == 'w':
        if game_map[(player_row - 1)][(player_column)] == ' ':
            game_map[player_row][player_column] = ' '
            player_row = player_row - 1
            game_map[player_row][player_column] = 'X'

        elif game_map[(player_row - 1)][(player_column)] == '#':
            game_map = generate_map()
            player_row = -2
            game_map[player_row][player_column] = 'X'
            current_room = current_room + 1

    elif key == 'a':
        if game_map[(player_row )][(player_column - 1)] == ' ':
            game_map[player_row][player_column] = ' '
            player_column = player_column - 1
            game_map[player_row][player_column] = 'X'

        elif game_map[(player_row )][(player_column - 1)] == '#':
            game_map = generate_map()
            player_column = -2
            game_map[player_row][player_column] = 'X'
            current_room = current_room + 1

    elif key == 's':
        if game_map[(player_row + 1)][(player_column)] == ' ':
            game_map[player_row][player_column] = ' '
            player_row = player_row + 1
            game_map[player_row][player_column] = 'X'

        elif game_map[(player_row + 1)][(player_column)] == '#':
            game_map = generate_map()
            player_row = 1
            game_map[player_row][player_column] = 'X'
            current_room = current_room + 1

    elif key == 'd':
        if game_map[(player_row )][(player_column + 1)] == ' ':
            game_map[player_row][player_column] = ' '
            player_column = player_column + 1
            game_map[player_row][player_column] = 'X'

        elif game_map[(player_row )][(player_column + 1)] == '#':
            game_map = generate_map()
            player_column = 2
            game_map[player_row][player_column] = 'X'
            current_room = current_room + 1

    print_map(game_map)
    print_hud()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

listener = keyboard.Listener(on_press=on_press)
listener.start()
