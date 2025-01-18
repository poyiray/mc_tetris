import random
from copy import deepcopy
from shape import name, typ, weight
from basic import top
from tetro import Tetro

#7 bag, a type of Random Generator in Tetris
class Bag_7():
    def __init__(self):
        #two lists are needed
        self.queue = [] #queue 1
        self.queue_t = [] #queue

        #shuffle the list (name)
        #name[] = {O, I, S, Z, L, J, T}, there are 7 different shapes 
        random.shuffle(name)
        
        #then add these 7 tetromino to the first queue
        for i in range(7):
            #the type of the tetromino will be randomly selected
            self.queue.append(Tetro((name[i], random.choices(typ, weight)[0]), 4, top - 2))
        
        #shuffle the list (name) again, and then store it into the list (queue_t)
        random.shuffle(name)
        self.queue_t = deepcopy(name)

        #define the head and the tail of the queue
        self.hh = 0
        self.tt = len(self.queue) % 7

    def get(self):
        #get the value at the head of the queue, then pop
        x = self.queue[self.hh]
        self.hh = (self.hh + 1) % 7

        #push one tetromino from the queue_t into the queue
        self.queue[self.tt] = Tetro((self.queue_t.pop(), random.choices(typ, weight)[0]), 4, top - 2)
        self.tt = (self.tt + 1) % 7

        #only when the queue_t is empty, the list name will be shuffled again and stored in queue_t
        if not len(self.queue_t):
            random.shuffle(name)
            self.queue_t = deepcopy(name)
            
        return x #return the value