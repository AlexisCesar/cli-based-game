default_map_size = 20

map = list()

id_counter = 0
for i in range(default_map_size):
	layer = list()

	layer.append(id_counter)
	id_counter = id_counter + 1

	for j in range (default_map_size):
		layer.append(' ')
	map.append(layer)

for layer in map:
	if layer[0] == 0 or layer[0] == (default_map_size - 1):
		layer_aux = list()
		layer_aux.append(layer[0])
		for i in range (default_map_size):
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


map[(default_map_size - 2)][int(default_map_size / 2)] = 'X'

while True:
	printMap()
	movement = input('waiting for command...')

