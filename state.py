from flask import Flask
import copy

class State:
    def __init__(self, flasks, parent_state=None):
        self._flasks = flasks
        self.parent_state = parent_state

    @property
    def flask_count(self):
        return len(self._flasks)

    def as_dict(self):
        res = {'flasks': []}
        for flask_num in range(len(self._flasks)):
            res['flasks'].append(self._flasks[flask_num].get_stack())
        return str(res)

    def __str__(self):
        return str(self.as_dict())

    @property
    def is_win_state(self):
        return all([x.is_one_colour or x.is_empty for x in self._flasks])

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        if sum([x.is_empty for x in other._flasks]) != sum([x.is_empty for x in self._flasks]):
            return False

        visited = []
        for flask_num in range(len(self._flasks)):
            if self._flasks[flask_num].is_empty:
                continue
            for other_flask_num in range(other.flask_count):
                if other_flask_num not in visited and self._flasks[flask_num] == other._flasks[other_flask_num]:
                    visited.append(other_flask_num)

        return len(self._flasks) == (sum([x.is_empty for x in self._flasks]) + len(visited))

    def compare(self, other):
        if (not isinstance(other, State)):
            return None
        for flask_num in range(len(self._flasks)):
            if not (self._flasks[flask_num] == other._flasks[flask_num]):
                return flask_num
        return None

    def get_next_states(self):
        out = []

        # attempt to move any top piece to another flask
        for flask_num in range(len(self._flasks)):
            # current flask is empty or all the same color
            if self._flasks[flask_num].is_empty or self._flasks[flask_num].is_one_colour:
                continue

            last_item = self._flasks[flask_num].get_last_item()

            for other_flask_num in range(len(self._flasks)):
                if other_flask_num == flask_num:
                    continue
                if self._flasks[other_flask_num].will_accept(last_item):
                    new_flasks = copy.deepcopy(self._flasks)
                    new_state = State(new_flasks, self)
                    new_state._move_top_item_index(other_flask_num, flask_num)
                    out.append(new_state)

        return out

    def _move_top_item_index(self, i, j):
        self._flasks[i].add_item(self._flasks[j].get_last_item_and_pop())
