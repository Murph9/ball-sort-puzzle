from flask import Flask
import copy
import itertools

class State:
    # immutable pls
    def __init__(self, flasks, parent_state=None, moved='Start'):
        self._flasks = flasks
        self.parent_state = parent_state
        self.moved = moved
        self.max = max([f.max for f in self._flasks])

        self._hash_me()
        self._set_heuristic()

    def _hash_me(self):
        self._hash = hash(tuple(self._flasks))

    def flask_count(self):
        return len(self._flasks)

    @property
    def _flask_max_size(self):
        return self.max

    def __hash__(self):
        return self._hash

    def as_dict(self):
        res = {'flasks': []}
        for flask in self._flasks:
            res['flasks'].append(flask.get_stack())
        return str(res)

    def __str__(self):
        as_matrix = [f.get_stack() for f in self._flasks]
        result = []
        for i in reversed(range(self._flask_max_size)):
            cur = []
            for stack in as_matrix:
                if len(stack) <= i:
                    cur.append('_')
                else:
                    cur.append(stack[i])
            result.append('|'.join(cur))
        return str(self.moved) +'\n'+'\n'.join(result)

    @property
    def is_win_state(self):
        return all([x.is_one_colour or x.is_empty for x in self._flasks])

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self._hash == other._hash

    def compare(self, other):
        return 0 if self.__eq__(other) else 1

    def get_next_states(self):
        out = []

        # attempt to move any top piece to another flask
        for flask_num in range(len(self._flasks)):
            # current flask is empty or all the same color
            if self._flasks[flask_num].is_empty or self._flasks[flask_num].is_one_colour:
                continue

            last_item = self._flasks[flask_num].peek()

            for other_flask_num in range(len(self._flasks)):
                if other_flask_num == flask_num:
                    continue
                if self._flasks[other_flask_num].accepts(last_item):
                    new_state = self._create_from_move_index(last_item, flask_num, other_flask_num)
                    out.append(new_state)

        return out

    def _create_from_move_index(self, last_item, i, j):
        new_flasks = copy.deepcopy(self._flasks)
        new_flasks[j].add(new_flasks[i].pop())
        return State(new_flasks, self, '{0} from col {1} to {2}'.format(last_item, i, j))

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def heuristic(self):
        return self._heuristic

    # im just guessing whats good
    def _set_heuristic(self):
        total = 0
        for flask in self._flasks:
            uniq_array = State.unique_array(flask.get_stack())
            total += len(uniq_array) # ungrouped colors give a score

        # reduce value 
        total = total + sum([-1 if x.is_empty else 0 for x in self._flasks])
        self._heuristic = total
    
    @staticmethod
    def unique_array(array):
        return [key for key, grp in itertools.groupby(array)]

    def validate(self):
        flask_length = self._flask_max_size
        if flask_length < 1:
            raise ValueError("Flasks must contain something")

        flat_colours = [j for sub in self._flasks for j in sub.get_stack()]
        if len(flat_colours) % flask_length != 0:
            raise ValueError(
                "Incorrect number of elements, must be a multiple of " + str(flask_length))

        incorrect_colours = [x for x in set(flat_colours) if flat_colours.count(x) != flask_length]
        if len(incorrect_colours) > 0:
            raise ValueError("Colours need the correct (+"+str(flask_length)+") number: " + str(incorrect_colours))

        if len(set(flat_colours)) + 2 != len(self._flasks):
            raise ValueError("There must be 2 extra flasks")
