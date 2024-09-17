from typing import Any

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self) -> bool:
        return not self.items
    
    def peek(self) -> Any:
        try:
            return self.items[-1]
        except IndexError:
            return None
        
    def push(self, item: Any) -> None:
        self.items.append(item)

    def pop(self) -> Any:
        try:
            return self.items.pop()
        except IndexError:
            return None
        