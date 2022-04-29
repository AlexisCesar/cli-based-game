from pynput import keyboard
import random
import sys
import os

clearConsole = lambda: os.system('cls' if os.name=='nt' else 'clear')

DEFAULT_MAP_SIZE = 10

# Map Objects
WALL = '*'
PLAYER = 'X'
FLOOR = ' '
MONEY = '$'
DOOR = '█'
HP = '♥'
ENEMY = '☻'
GRAVE = '┼'
PASSABLE_OBJETCS = [FLOOR, MONEY, HP, ENEMY]

# Consts
PLAYER_MAX_HP = 100
LIFE_POTION_HP = 5
ENEMY_DAMAGE = 10

# Player status
player_money = 0
player_hp = PLAYER_MAX_HP
player_kills = 0

# Game status
current_room = 1

def generate_map():
    map = list()

    id_counter = 0
    for i in range(DEFAULT_MAP_SIZE):
        layer = list()

        layer.append(id_counter)
        id_counter = id_counter + 1

        for j in range(DEFAULT_MAP_SIZE):
            layer.append(FLOOR)
        map.append(layer)

    for layer in map:
        if layer[0] == 0 or layer[0] == (DEFAULT_MAP_SIZE - 1):
            layer_aux = list()
            layer_aux.append(layer[0])
            for i in range(DEFAULT_MAP_SIZE):
                layer_aux.append(WALL)
            map[map.index(layer)] = layer_aux
        for index, column in enumerate(layer):
            if index == 1 or index == (DEFAULT_MAP_SIZE):
                layer[index] = WALL
    
    map[0][1] = '/'
    map[0][-1] = '\\'
    map[-1][1] = '\\'
    map[-1][-1] = '/'

    # Generate random door
    door_direction = random.choice(['n', 's', 'e', 'w'])
    indexes = list(range(0, DEFAULT_MAP_SIZE))[4:-4]

    if door_direction == 'n':
        map[0][random.choice(indexes)] = DOOR

    elif door_direction == 's':
        map[-1][random.choice(indexes)] = DOOR

    elif door_direction == 'e':
        map[random.choice(indexes)][-1] = DOOR

    elif door_direction == 'w':
        map[random.choice(indexes)][1] = DOOR

    # Drop enemies
    for i in range(random.choice(list(range(current_room, (current_room * 2))))):
        random_row = random.choice(list(range(0, DEFAULT_MAP_SIZE))[1:-1])
        random_column = random.choice(list(range(0, DEFAULT_MAP_SIZE))[2:])
        map[random_row][random_column] = ENEMY
    
    # Drop random coins
    for i in range(random.choice(list(range(2, 6)))):
        random_row = random.choice(list(range(0, DEFAULT_MAP_SIZE))[1:-1])
        random_column = random.choice(list(range(0, DEFAULT_MAP_SIZE))[2:])
        map[random_row][random_column] = MONEY

    # Drop random life potions
    for i in range(random.choice(list(range(3, 6)))):
        random_row = random.choice(list(range(0, DEFAULT_MAP_SIZE))[1:-1])
        random_column = random.choice(list(range(0, DEFAULT_MAP_SIZE))[2:])
        map[random_row][random_column] = HP

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
game_map[player_row][player_column] = PLAYER


def print_hud():
    print('█' * DEFAULT_MAP_SIZE * 2)
    print(f'{MONEY}: {player_money}')
    print(f'{HP}: {player_hp}')
    print(f'ROOM: {current_room}')
    print(f'ENEMIES KILLED: {player_kills}')
    print('█' * DEFAULT_MAP_SIZE * 2)
    

def print_death():
    print('█' * DEFAULT_MAP_SIZE * 2)
    print(f'{GRAVE} You died in the {current_room} room... {GRAVE}')
    print()
    print('Press enter and leave...')
    print('█' * DEFAULT_MAP_SIZE * 2)
    input()
    sys.exit(0)


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
print()
print_hud()

def performMove(key):
    global player_row
    global player_column
    global game_map
    global player_money
    global current_room
    global player_hp
    global player_kills

    if key == 'w':
        if game_map[(player_row - 1)][(player_column)] in PASSABLE_OBJETCS:
            game_map[player_row][player_column] = FLOOR
            player_row = player_row - 1

        elif game_map[(player_row - 1)][(player_column)] == DOOR:
            game_map = generate_map()
            player_row = -2
            current_room = current_room + 1

    elif key == 'a':
        if game_map[(player_row )][(player_column - 1)] in PASSABLE_OBJETCS:
            game_map[player_row][player_column] = FLOOR
            player_column = player_column - 1

        elif game_map[(player_row )][(player_column - 1)] == DOOR:
            game_map = generate_map()
            player_column = -2
            current_room = current_room + 1

    elif key == 's':
        if game_map[(player_row + 1)][(player_column)] in PASSABLE_OBJETCS:
            game_map[player_row][player_column] = FLOOR
            player_row = player_row + 1

        elif game_map[(player_row + 1)][(player_column)] == DOOR:
            game_map = generate_map()
            player_row = 1
            current_room = current_room + 1

    elif key == 'd':
        if game_map[(player_row )][(player_column + 1)] in PASSABLE_OBJETCS:
            game_map[player_row][player_column] = FLOOR
            player_column = player_column + 1

        elif game_map[(player_row )][(player_column + 1)] == DOOR:
            game_map = generate_map()
            player_column = 2
            current_room = current_room + 1

    if game_map[player_row][player_column] == MONEY:
        player_money = player_money + 1
    elif game_map[player_row][player_column] == HP:
        if player_hp <= (PLAYER_MAX_HP - LIFE_POTION_HP):
            player_hp = player_hp + LIFE_POTION_HP
        else: 
            player_hp = PLAYER_MAX_HP
    elif game_map[player_row][player_column] == ENEMY:
        player_hp = player_hp - ENEMY_DAMAGE
        if player_hp <= 0:
            print()
            print_death()
        player_kills = player_kills + 1

    game_map[player_row][player_column] = PLAYER

    print_map(game_map)
    print()
    print_hud()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

listener = keyboard.Listener(on_press=on_press)
listener.start()
