from room import Room
from player import Player
from world import World
from util import Graph, Queue, Stack


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

graph = Graph()


# creates the graph by traversing all the room 
def create_graph(): 
    visited = set()
    stack = Stack() #rename variable 
    stack.push(world.starting_room)
    

    while stack.size() > 0:
        room = stack.pop()
        room_id = room.id

        if room_id not in graph.vertices: 
            graph.add_vertex(room_id)

        exits = room.get_exits()

        for direction in exits:
            # this finds the next rooms and adds to graph
            upcoming_rooms = room.get_room_in_direction(direction) 
            upcoming_rooms_id = upcoming_rooms.id

            if upcoming_rooms_id not in graph.vertices:
                graph.add_vertex(upcoming_rooms_id)

            # connect rooms as directed edges 
            graph.add_edge(room_id, upcoming_rooms_id, direction)

            if upcoming_rooms_id not in visited:
                stack.push(upcoming_rooms)
        visited.add(room_id)


def find_upcoming_path(room_id, visited, g=graph):
    v = set()
    v.add(room_id)

    queue = Queue()
    queue.enqueue({room_id: []})

    while queue.size() > 0:
        room_info = queue.dequeue()
        # Room is current room, moves is what moves it took to get here
        room = list(room_info.keys())[0]
        moves = room_info[room]

        # gets the rooms neighbors
        neighbors = g.get_neighbors(room)

        # grabs keys, keys = directions
        neighbors_keys = list(neighbors.keys())

        # Dead end.. Returns set of directions for player to continue
        if len(neighbors_keys) == 1 and neighbors[neighbors_keys[0]] not in visited:
            dead_end = list(moves) + [neighbors_keys[0]]
            return dead_end


        else:
            # continues to traverse the graph until we hit a dead end 
            for direction in neighbors:
                upcoming_room = neighbors[direction]
                next_moves = moves + [direction]

                if upcoming_room not in visited:
                    return next_moves

                if upcoming_room not in v:
                    queue.enqueue({upcoming_room: next_moves})
                    v.add(upcoming_room)


visited = set()
traversal_path = []
create_graph()




visited.add(world.starting_room.id)

current_room_id = world.starting_room.id
total_rooms = len(graph.vertices)

while len(visited) < total_rooms:
    moves = find_upcoming_path(current_room_id, visited)
    # traverses the returned list of moves
    for direction in moves:
        player.travel(direction)
        traversal_path.append(direction)
        visited.add(player.current_room.id)
    # updates the current room
    current_room_id = player.current_room.id

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
