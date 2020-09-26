import copy
import heapq
import json
from collections import deque

from flask import Flask
from state import State


class Solver:
    def parse_object(self, parsed):
        if not parsed["flasks"] or len(parsed["flasks"]) < 1:
            raise ValueError("No flasks given. format {'flasks':[...]}")
        flask_length = max([len(x) for x in parsed["flasks"]])

        return State([Flask([x for x in f], flask_length) for f in parsed["flasks"]])

    def parse_string(self, string):
        flasks = []
        rows = reversed(string.splitlines())
        for r in rows:
            if len(r) == 0:
                continue
            i = 0
            for c in r:
                if len(flasks) - 1 < i:
                    flasks.append([])
                flasks[i].append(c)
                i += 1

        # then the final 2 rows
        flasks.append([])
        flasks.append([])

        flask_length = max([len(x) for x in flasks])
        return State([Flask([x for x in f], flask_length) for f in flasks])

    def solve(self, state):
        init_state = state
        init_state.validate()

        queue = []  # queue list
        heapq.heappush(queue, init_state)
        visited = set()

        solved_state = None

        while len(queue) != 0:
            current_state = heapq.heappop(queue)
            if current_state in visited:
                continue

            visited.add(current_state)
            if current_state.is_win_state:
                solved_state = current_state
                break

            new_states = current_state.get_next_states()
            [heapq.heappush(queue, x) for x in new_states if x not in queue]

        if solved_state == None:
            raise ValueError("Can't solve !!!!, tried: " + str(len(visited)))

        res = []
        while solved_state != None:
            com_pared = solved_state.compare(solved_state.parent_state)
            if com_pared is None:
                solved_state = solved_state.parent_state
                continue

            res.append(solved_state)
            solved_state = solved_state.parent_state
        res.append(init_state)  # add 'final state'

        print("Solved. In " + str(len(res)) + " steps. Search space: " + str(len(visited)))

        return reversed(res)  # return it in step order

    def pretty_print_solution(self, result):
        for state in result:
            print(state)
            print("")


########################
start_basic = {"flasks": [[x for x in ["R", "P", "R"]], [x for x in ["P", "R", "P"]], [], []]}

start_basic2 = {
    "flasks": [
        [x for x in ["R", "P", "R"]],
        [x for x in ["P", "R", "P"]],
        [x for x in ["W", "W", "W"]],
        [],
        [],
    ]
}

start_medium = {
    "flasks": [
        [x for x in ["Y", "R", "B", "R"]],
        [x for x in ["B", "B", "R", "Y"]],
        [x for x in ["Y", "R", "B", "Y"]],
        [x for x in ["4", "4", "3", "3"]],
        [x for x in ["3", "3", "4", "4"]],
        [],
        [],
    ]
}

start_complex = {
    "flasks": [
        [x for x in ["R", "P", "N", "G"]],
        [x for x in ["T", "L", "O", "L"]],
        [x for x in ["P", "B", "T", "A"]],
        [x for x in ["B", "G", "N", "V"]],
        [x for x in ["T", "R", "G", "B"]],
        [x for x in ["O", "A", "Y", "C"]],
        [x for x in ["Y", "Y", "R", "V"]],
        [x for x in ["T", "V", "N", "G"]],
        [x for x in ["N", "L", "L", "V"]],
        [x for x in ["A", "C", "C", "O"]],
        [x for x in ["A", "R", "P", "B"]],
        [x for x in ["O", "Y", "C", "P"]],
        [],
        [],
    ]
}

start_73 = {
    "flasks": [
        [x for x in ["9", "0", "7", "1"]],
        [x for x in ["A", "9", "8", "1"]],
        [x for x in ["6", "0", "5", "2"]],
        [x for x in ["6", "5", "A", "1"]],
        [x for x in ["0", "4", "3", "3"]],
        [x for x in ["8", "8", "5", "4"]],
        [x for x in ["3", "3", "6", "4"]],
        [x for x in ["0", "9", "2", "5"]],
        [x for x in ["1", "2", "A", "6"]],
        [x for x in ["A", "8", "7", "4"]],
        [x for x in ["9", "7", "2", "7"]],
        [],
        [],
    ]
}


def run():
    solver = Solver()
    state = solver.parse_string(
        """
PPZAZRWSWRSA
BYMSNPBRSPOW
BGAMYWYBNMBY
YNGPGOAOOMNZ
GMRAORNZWZSG"""
    )
    # state = solver.parse_object(start_73)
    result = solver.solve(state)
    solver.pretty_print_solution(result)


# originally from https://github.com/akcio/ball_sort_puzzle_solver
if __name__ == "__main__":
    run()
    # profiling:
    # import cProfile cProfile.run('run()')
