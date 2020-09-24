from collections import deque
from state import State
from flask import Flask
import json
import copy

name = {
    'Blue': 1,
    'Green': 2,
    'Turquoise': 3,
    'Gray': 4,
    'Brown': 5,
    'LightGreen': 6,
    'Yellow': 7,
    'Violet': 8,
    'DarkBlue': 9,
    'Orange': 10,
    'Pink': 11,
    'Red': 12,
}

json_parsed = {
    'flasks': [
        [name[x] for x in ['Red', 'Pink', 'Red']],
        [name[x] for x in ['Pink', 'Red', 'Pink']],
        [],
        []
    ]
}

jsonParse = {
    'flasks': [
        [name[x] for x in ['Red', 'Pink', 'DarkBlue', 'Green']],
        [name[x] for x in ['Turquoise', 'LightGreen', 'Orange', 'LightGreen']],
        [name[x] for x in ['Pink', 'Brown', 'Turquoise', 'Gray']],
        [name[x] for x in ['Brown', 'Green', 'DarkBlue', 'Violet']],
        [name[x] for x in ['Turquoise', 'Red', 'Green', 'Brown']],
        [name[x] for x in ['Orange', 'Gray', 'Yellow', 'Blue']],
        [name[x] for x in ['Yellow', 'Yellow', 'Red', 'Violet']],
        [name[x] for x in ['Turquoise', 'Violet', 'DarkBlue', 'Green']],
        [name[x] for x in ['DarkBlue', 'LightGreen', 'LightGreen', 'Violet']],
        [name[x] for x in ['Gray', 'Blue', 'Blue', 'Orange']],
        [name[x] for x in ['Gray', 'Red', 'Pink', 'Brown']],
        [name[x] for x in ['Orange', 'Yellow', 'Blue', 'Pink']],
        [],
        []
    ]
}

class Solver:

    def parse_object(self, parsed):
        if (not parsed['flasks'] or len(parsed['flasks']) < 1):
            raise ValueError("No flasks given. format {'flasks':[...]}")
        flask_length = len(parsed['flasks'][0])
        if (flask_length < 1):
            raise ValueError("First flask must be full")

        return State([Flask([int(x) for x in f], flask_length) for f in parsed['flasks']])

    # TODO greedy search
    def solve(self, parsed):
        init_state = self.parse_object(parsed)
    
        queue_state = deque() # init queue
        queue_state.append(init_state)
        visited = []

        solved_state = None

        while len(queue_state) != 0:
            current_state = queue_state.pop()
            if current_state in visited:
                continue

            visited.append(current_state)
            if current_state.is_win_state:
                solved_state = current_state
                break

            new_states = current_state.get_next_states()
            [queue_state.append(x) for x in new_states if x not in queue_state]

        if solved_state == None:
            print("Can't solve")

        res = []
        while solved_state != None:
            com_pared = solved_state.compare(solved_state.parent_state)
            if com_pared is None:
                solved_state = solved_state.parent_state
                continue

            res.append(solved_state)
            solved_state = solved_state.parent_state
        
        print(parsed)
        for i in reversed(res):
            print(i)
        
        return res


# originally from https://github.com/akcio/ball_sort_puzzle_solver
if __name__ == "__main__":
    solver = Solver()
    solver.solve(json_parsed)
