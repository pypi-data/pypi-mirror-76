# obify
A python library that will provide all algorithms working on object 

### This library can be used following way

```python
from obify import heap

class Node():
    def __init__(self, data):
        self.data = data

    def compare(self, node):
        if self.data < node.data:
            return -1
        elif self.data > node.data:
            return 1
        else:
            return 0

def test_heap():
    h = heap.MinHeap()
    h.insert(Node(12))
    h.insert(Node(2))
    h.insert(Node(20))
    h.remove()
    h.insert(Node(0))
```
