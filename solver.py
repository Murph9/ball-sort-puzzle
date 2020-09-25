from collections import deque
from state import State
from flask import Flask
import json
import copy
import heapq

class Solver:

    def parse_object(self, parsed):
        if (not parsed['flasks'] or len(parsed['flasks']) < 1):
            raise ValueError("No flasks given. format {'flasks':[...]}")
        flask_length = max([len(x) for x in parsed['flasks']])
        if (flask_length < 1):
            raise ValueError("Flasks must contain something")

        # TODO validate that the correct number of colours and enough of each colour exists
        return State([Flask([chr(x) for x in f], flask_length) for f in parsed['flasks']])

    def solve(self, parsed):
        init_state = self.parse_object(parsed)
    
        queue = [] #queue list
        heapq.heappush(queue, init_state)
        visited = []

        solved_state = None

        while len(queue) != 0:
            current_state = heapq.heappop(queue)
            if current_state in visited:
                continue

            visited.append(current_state)
            if current_state.is_win_state:
                solved_state = current_state
                break

            new_states = current_state.get_next_states()
            [heapq.heappush(queue, x) for x in new_states if x not in queue]

        if solved_state == None:
            raise ValueError("Can't solve !!!!")

        res = []
        while solved_state != None:
            com_pared = solved_state.compare(solved_state.parent_state)
            if com_pared is None:
                solved_state = solved_state.parent_state
                continue

            res.append(solved_state)
            solved_state = solved_state.parent_state
        res.append(init_state) # add 'final state'

        print("Solved. In " + str(len(res)) + " steps. Search space: " + str(len(visited)))

        return reversed(res) # return it in step order

    def pretty_print_solution(self, result):
        for state in result:
            print(state)
            print('')

########################
start_basic = {
    'flasks': [
        [ord(x) for x in ['R', 'P', 'R']],
        [ord(x) for x in ['P', 'R', 'P']],
        [],
        []
    ]
}

start_basic2 = {
    'flasks': [
        [ord(x) for x in ['R', 'P', 'R']],
        [ord(x) for x in ['P', 'R', 'P']],
        [ord(x) for x in ['W', 'W', 'W']],
        [],
        []
    ]
}

start_medium = {
    'flasks': [
        [ord(x) for x in ['Y', 'R', 'B', 'R']],
        [ord(x) for x in ['B', 'B', 'R', 'Y']],
        [ord(x) for x in ['Y', 'R', 'B', 'Y']],
        [],
        []
    ]
}

start_complex = {
    'flasks': [
        [ord(x) for x in ['R', 'P', 'N', 'G']],
        [ord(x) for x in ['T', 'L', 'O', 'L']],
        [ord(x) for x in ['P', 'B', 'T', 'A']],
        [ord(x) for x in ['B', 'G', 'N', 'V']],
        [ord(x) for x in ['T', 'R', 'G', 'B']],
        [ord(x) for x in ['O', 'A', 'Y', 'C']],
        [ord(x) for x in ['Y', 'Y', 'R', 'V']],
        [ord(x) for x in ['T', 'V', 'N', 'G']],
        [ord(x) for x in ['N', 'L', 'L', 'V']],
        [ord(x) for x in ['A', 'C', 'C', 'O']],
        [ord(x) for x in ['A', 'R', 'P', 'B']],
        [ord(x) for x in ['O', 'Y', 'C', 'P']],
        [],
        []
    ]
}

start_73 = {
    'flasks': [
        [ord(x) for x in ['9', '0', '7', '1']],
        [ord(x) for x in ['A', '9', '8', '1']],
        [ord(x) for x in ['6', '0', '5', '2']],
        [ord(x) for x in ['6', '5', 'A', '1']],
        [ord(x) for x in ['0', '4', '3', '3']],
        [ord(x) for x in ['8', '8', '5', '4']],
        [ord(x) for x in ['3', '3', '6', '4']],
        [ord(x) for x in ['0', '9', '2', '5']],
        [ord(x) for x in ['1', '2', 'A', '6']],
        [ord(x) for x in ['A', '8', '7', '4']],
        [ord(x) for x in ['9', '7', '2', '7']],
        [],
        []
    ]
}


# originally from https://github.com/akcio/ball_sort_puzzle_solver
if __name__ == "__main__":
    solver = Solver()
    result = solver.solve(start_73)
    solver.pretty_print_solution(result)
