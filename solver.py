from collections import deque
from state import State
from flask import Flask
import json
import copy
import heapq

class Solver:

    def parse_string(self, string):
        flasks = []
        rows = reversed(string.splitlines())
        for r in rows:
            if len(r) == 0:
                continue
            i = 0
            for c in r:
                if len(flasks)-1 < i:
                    flasks.append([])
                flasks[i].append(c)
                i+=1

        # then the final 2 rows
        flasks.append([])
        flasks.append([])

        flask_length = max([len(x) for x in flasks])
        return State([Flask([x for x in f], flask_length) for f in flasks])

    def solve(self, state):
        init_state = state
        init_state.validate()
        print("Validated input correctly, searching for a solution.")

        queue = [] #queue list
        heapq.heappush(queue, init_state)
        visited = set()

        solved_state = None
        i = 0
        while len(queue) != 0:
            current_state = heapq.heappop(queue)
            if current_state in visited:
                continue

            visited.add(current_state)
            if current_state.is_win_state:
                solved_state = current_state
                break

            i+=1
            if i % 20 == 0:
                print(f"Current weight (goal is 0): {current_state.heuristic()}")

            new_states = current_state.get_next_states()
            [heapq.heappush(queue, x) for x in new_states if x not in queue]


        print("Search finished")

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
        res.append(init_state) # add 'final state'

        print("Solved. In " + str(len(res)) + " steps. Search space: " + str(len(visited)))

        return reversed(res) # return it in step order

    def pretty_print_solution(self, result):
        for state in result:
            print(state)
            print('')

########################
start_basic = """
RP
PR
RP
"""

start_basic2 = """
RPW
PRW
RPW
"""

start_medium = """
RYY34
BRB34
RBR43
YBY43
"""

start_complex = """
GLAVBCVGVOBP
NOTNGYRNLCPC
PLBGRAYVLCRY
RTPBTOYTNAAO
"""

start_73 = """
11213445647
785A3562A72
09054839287
9A6608301A9
""" 

start_371 = """
PPZAZRWSWRSA
BYMSNPBRSPOW
BGAMYWYBNMBY
YNGPGOAOOMNZ
GMRAORNZWZSG
"""

start_136 = """
bgg1rrdwpooa
odbwgydwbayp
syp1z1ar1gas
ybrszzsdowpz
"""

def run():
    solver = Solver()
    state = solver.parse_string(start_136)
    result = solver.solve(state)
    solver.pretty_print_solution(result)


# originally from https://github.com/akcio/ball_sort_puzzle_solver
if __name__ == "__main__":
    # run()
    # profiling:
    import cProfile
    cProfile.run('run()')
