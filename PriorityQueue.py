from heapq import *

class PriorityQueue:
    def __init__(self, max, eq ):
        self.list = []
        self.eq = eq
        self.max_num = max

    def top(self):
        return heappop(self.list)
    def max(self):
        return self.list[0]
    def size(self):
        return len(self.list)

    def push(self, value):
        # if len(self.list) >= self.max_num:
        #     if value < self.list[0]:
        #         self.top()
        #         heappush(self.list, value)
        #         return True
        #     else:
        #         return False
        # else:
            heappush(self.list, value)
            return True
    '''
    find the rank of the item in list, if its rank bigger than max_rank, return the max_rank
    '''
    def getRank(self, value, max_rank = 0):
        if max_rank == 0 :
            max_rank = len(self.list)
        rank = 0
        tmp = self.list.copy()
        while len(self.list) > 0:
            rank += 1
            i = self.top()
            if self.eq(i,value) or rank >= max_rank:
                break
        self.list = tmp
        return rank
    '''
    remove the item in list whose value equal to value  
    '''
    def remove(self, value):
        for i in self.list:
            if self.eq(i,value):
                self.list.remove(i)
                break
