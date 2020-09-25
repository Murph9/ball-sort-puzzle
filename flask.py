import copy

class Flask:
    def __init__(self, stack, max_count):
        self.max = max_count
        self._stack = tuple(stack)

    def __str__(self):
        return str(self._stack)

    @property
    def is_empty(self):
        return not self._stack

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
        return self._stack

    def accepts(self, item):
        if self.is_empty:
            return True
        if self.is_full:
            return False
        return self._stack[-1] == item
    
    def pop(self):
        ret = self._stack[-1]
        self._stack = tuple(self._stack[:-1])
        return ret

    def peek(self):
        return self._stack[-1]

    def add(self, item):
        self._stack = tuple(self._stack + (item,))

    def __eq__(self, other):
        if not isinstance(other, Flask):
            return False
        return self._stack == other._stack

    def __hash__(self):
        return hash(self._stack)
