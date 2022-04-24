default_map_size = 20

map = list()

id_counter = 0
for i in range(default_map_size):
	layer = list()

	layer.append(id_counter)
	id_counter = id_counter + 1

	for j in range (default_map_size):
		layer.append(0)
	map.append(layer)

for layer in map:
	print(layer[1:-1])

