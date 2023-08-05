class Stack:
    def __init__(self):
        self._top = -1
        self.stack = []
    
    def __len__(self):
        return self._top + 1
    
    def is_empty(self):
        return self._top == -1

    def push(self, elem):
        self.stack.append(elem)
        self._top += 1
    
    def pop(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        self._top += 1
        return self.stack.pop()
    
    def peek(self):
        """returns the current top element of the stack."""
        if self.is_empty():
            raise IndexError("stack is empty")
        return self.stack[self._top]
    
    def __str__(self):
        return ''.join([str(elem) for elem in self.arr])