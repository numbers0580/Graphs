from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

reverse_path = []

reverse = {'n':'s', 's':'n', 'w':'e', 'e':'w'}

graph = {}

current = player.current_room.id

rooms = []

while len(graph) < len(world.rooms):
    if current not in graph:
        graph[current] = {}
        new_room = graph[current]
        for direction in player.current_room.get_exits():
            new_room[direction] = '?'
    
    for i in graph[current]:
        room = graph[current]
        direction = room[i]
        if direction == '?':
            # Player travels in that direction
            player.travel(i)
            traversal_path.append(i)
            # Save the previous room
            previous = current
            # Current room is updated
            current = player.current_room.id
            if current not in graph:
                graph[current] = {}
                new_room = graph[current]
                for x in player.current_room.get_exits():
                    new_room[x] = '?'
            # Previous room's map is updated
            room[i] = current

            reverse_direction = reverse[i]
            graph[current][reverse_direction] = previous
            reverse_path.append(reverse_direction)
            break

    explored = True
    for i in graph[current]:
        if graph[current][i] == '?':
            explored = False

    if explored == True:
        # Retrace steps to previous room
        retrace = reverse_path.pop()
        player.travel(retrace)
        traversal_path.append(retrace)

        # Current room is updated
        current = player.current_room.id


# print("===== GRAPH =====")
# for i in graph:
#     print(f'{i:3}: {graph[i]}')




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")