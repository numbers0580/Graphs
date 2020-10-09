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
# print(f"MY TEST -- current room is {player.current_room.id}")

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# So I need to create an empty set to test the rooms I'll visit. I also need to initialize player's starting room
testvisit = {}
roomid = player.current_room.id
revpath = []

# Pulled a duplicate conditional out of the while-loop to use here as initialization instead
testvisit[roomid] = {}
nextroom = testvisit[roomid]
for x in player.current_room.get_exits():
    nextroom[x] = '?'

# Loop for as long as the total rooms I visit are less than the total available
while len(testvisit) < len(world.rooms):
    # if roomid not in testvisit:
    #     testvisit[roomid] = {} # testvisit = { 0: {} }
    #     nextroom = testvisit[roomid] # nextroom = {}
    #     for d in player.current_room.get_exits():
    #         # According to room.py, d should be n, s, w, e
    #         nextroom[d] = '?'
    #         # nextroom = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
    #         # testvisit = { 0: {'n': '?', 's': '?', 'w': '?', 'e': '?'} }
    #         # print(f"NEXTROOM TEST: d is {d}, nextroom is {nextroom[d]}")
    #         # print(f"TESTVISIT: {testvisit}") # Working as expected, so far

    for d in testvisit[roomid]:
        space = testvisit[roomid]
        adjacent = space[d] # tried 'dir', but disallowed
        # d is n, space is {'n': '?', 's': '?', 'w': '?', 'e': '?'}, adjacent is ?
        # repeats for s, w, and e
        # print(f"TESTING: d is {d}, space is {space}, adjacent is {adjacent}")
        if adjacent == '?':
            # Undiscovered room and can travel to that room
            traversal_path.append(d) # Record the direction taken
            player.travel(d)

            # Created a "prev_room" temp variable in order to reverse direction
            prev_room = roomid

            # Update roomid for the new room
            roomid = player.current_room.id

            if roomid not in testvisit:
                testvisit[roomid] = {}
                nextroom = testvisit[roomid]
                for dd in player.current_room.get_exits():
                    nextroom[dd] = '?'

            space[d] = roomid
            # Once this for-loop is done, we should have space['n'] = #, space['s'] = #, space['w'] = #, space['e'] = #
            # But I need to return to this previous room each time to peek into all the other directions
            # Created a variable "prev_room" above to store the id of the room "0" before I start peeking in all directions

            revd = '?'
            if d == 'n':
                revd = 's'
            elif d == 's':
                revd = 'n'
            elif d == 'w':
                revd = 'e'
            elif d == 'e':
                revd = 'w'

            testvisit[roomid][revd] = prev_room
            revpath.append(revd)
            # The plan was to loop through all directions, but getting an error
            # Breaking out of for-loop and will check visits with boolean within while-loop
            break

    hasvisited = True
    # Check all available directions
    for i in testvisit[roomid]:
        if testvisit[roomid][i] == '?':
            hasvisited = False

    # if all available adjacent rooms had been visited
    if hasvisited:
        backup = revpath.pop()
        player.travel(backup)
        # Since I still moved to a room, store that move in the travel history
        traversal_path.append(backup)
        # Get updated room id
        roomid = player.current_room.id


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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
