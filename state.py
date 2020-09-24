from flask import Flask
import copy


class State:
    def __init__(self, flasks, parent_state=None):
        self.flaskSize = flasks[0].length
        self._flasks = flasks
        self.parentState = parent_state

    @property
    def flask_count(self):
        return len(self._flasks)

    def getFlasks(self):
        ret = copy.deepcopy(self._flasks)
        return ret

    def setFlasks(self, flasks):
        self._flasks = flasks

    def __str__(self):
        return ",".join([str(x) for x in self._flasks])

    @property
    def isWinState(self):
        return all([x.isOneColor or x.isEmpty for x in self._flasks])

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        other_flasks = other.getFlasks()
        if sum([x.isEmpty for x in other_flasks]) != sum([x.isEmpty for x in self._flasks]):
            return False

        visited = []
        for flask_num in range(len(self._flasks)):
            if self._flasks[flask_num].isEmpty:
                continue
            for other_flask_num in range(len(other_flasks)):
                if other_flask_num not in visited and self._flasks[flask_num] == other_flasks[other_flask_num]:
                    visited.append(other_flask_num)

        return len(self._flasks) == (sum([x.isEmpty for x in self._flasks]) + len(visited))

    def compare(self, other):
        if (not isinstance(other, State)):
            return None
        otherFlasks = other.getFlasks()
        for flaskNum in range(len(self._flasks)):
            if not (self._flasks[flaskNum] == otherFlasks[flaskNum]):
                return flaskNum
        return None

    def toDict(self):
        res = { 'flasks': [] }
        for flaskNum in range(len(self._flasks)):
            res['flasks'].append(self._flasks[flaskNum].getStack())
        return res

    def get_next_states(self):
        out = []

        flasks = self.getFlasks()
        # attempt to move any top piece to another flask
        for flaskNum in range(len(flasks)):

            # current flask is empty or all the same color
            if flasks[flaskNum].isEmpty or flasks[flaskNum].isOneColor or flasks[flaskNum].isNeedOneMore:
                continue

            last_item = flasks[flaskNum].getLastItem()

            for otherFlaskNum in range(len(flasks)):
                if otherFlaskNum == flaskNum or flasks[otherFlaskNum].isFull:
                    continue

                if flasks[otherFlaskNum].isEmpty or (not flasks[otherFlaskNum].isFull and flasks[otherFlaskNum].isLastValueEqual(last_item)):
                    new_flasks = copy.deepcopy(flasks)
                    new_flasks[otherFlaskNum].addItem(new_flasks[flaskNum].getLastItemAndPop())
                    new_state = State(new_flasks, self)
                    out.append(new_state)

        return out
