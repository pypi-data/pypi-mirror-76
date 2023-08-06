from . import util

logger = util.getlogger()

class MinHeap():
    def __init__(self):
        self.size = 0
        self.arr = []

    def insert(self, element):
        logger.debug('inserting' + str(element.data))
        self.size += 1
        self.arr.append(element)
        self.swim(self.size -1 )

    def remove(self):
        logger.debug('Deleting' + str(self.arr[0].data))
        self.arr[0] = self.arr[-1]
        del self.arr[-1]
        self.size -= 1
        self.sink(0)


    def sink(self, index):
        while index < (self.size - 1 )/2:
            left = self.getChild(index)
            small = left
            if left  < self.size -1:
                right = left + 1
                if self.compare(left, right) > 0:
                    small = right
            if self.compare(small, index ) == -1:
                self.swap(small, index)
                index = small
            else:
                break
     

    def swim(self, index):

        while index > 0:
            parent = self.getparent(index)
            if self.compare(index, parent) == -1:
                self.swap(index, parent)
                #logger.debug('index value' + str(index))
                index = parent
                #logger.debug('index value after' + str(index))
            else:
                break
            

    def compare(self, element1, element2):
        return self.arr[element1].compare(self.arr[element2])

    def getparent(self, index):
        return (index -1) // 2

    def getChild(self, index):
        left = 2 * index + 1
        logger.debug(f'child {left} {left + 1}')
        return left

    def swap(self, index1, index2):
        logger.debug('Swapping' + str(self.arr[index1].data) + str(self.arr[index2].data))
        self.arr[index1], self.arr[index2] = self.arr[index2], self.arr[index1]

    def getall(self):
        return self.arr