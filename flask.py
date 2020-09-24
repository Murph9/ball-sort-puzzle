import copy

class Flask:
    def __init__(self, stack, max_count):
        self.max = max_count
        self._stack = stack

    def __str__(self):
        return str(self._stack)

    @property
    def is_empty(self):
        return len(self._stack) == 0

    @property
    def length(self):
        return len(self._stack)

    @property
    def is_full(self):
        return len(self._stack) >= self.max

    @property
    def is_one_colour(self):
        return self.is_full and all([x == self._stack[0] for x in self._stack])

    def get_stack(self):
        ret = copy.deepcopy(self._stack)
        return ret

    @property
    def is_need_one_more(self):
        return len(self._stack) == (self.max - 1) and all(x == self._stack[0] for x in self._stack)

    def is_last_value_equal(self, item):
        return self._stack[-1] == item

    def get_last_item_and_pop(self):
        item = self._stack[-1]
        self._stack = self._stack[0:-1]
        return item

    def get_last_item(self):
        return self._stack[-1]

    def add_item(self, item):
        self._stack.append(item)

    def __eq__(self, other):
        if not isinstance(other, Flask):
            return False
        return len(self._stack) == len(other.get_stack()) and all([self._stack[x] == other.get_stack()[x] for x in range(len(self._stack))])
