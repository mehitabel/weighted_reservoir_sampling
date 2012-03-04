import numpy as np
import heapq as hq

#
# Single-pass sampling, with weights, with or without replacement.
# The philosophy is to start independent poisson processes for each item and gather the first events
# We simulate these Poisson processes using their exponential waiting times.
# 
# Note: In order to use an out-of-the-box min-heap for book-keeping, we work in negative time.
#
#
# TODO: add tests, demo of correctness.
#
#

def weighted_reservoir_noreplace(iter,k):
    """ Eats an iterator over tuples (item, weight) and returns k weighted samples without replacement """

    heap = []

    hkey = lambda w: -np.random.exponential(1.0/w)

    for (item, weight) in iter:
        if len(heap) < k:
            hq.heappush(heap, (hkey(weight),item))
        elif hkey(weight) > heap[0][0]:
            hq.heapreplace(heap, (hkey(weight),item))

    while len(heap) > 0:
        yield hq.heappop(heap)[1]

def weighted_reservoir_replace(iter, k):
    """ Eats an iterator over tuples (item, weight) and returns k weighted samples with replacement"""
    
    heap = []

    def negtimes(w):
        current = 0.0
        while True:
            current -= np.random.exponential(1.0/w)
            yield current
    

    for (item, weight) in iter:
        for t in negtimes(weight):
            if len(heap) < k:
                hq.heappush(heap, (t, item))
            elif t > heap[0][0]:
                hq.heapreplace(heap, (t,item))
	    else:
                break

    while len(heap) > 0:
        yield hq.heappop(heap)[1]        

def demo():
    """ Uses weighted_reservoir_replace to generate 1000 fair coin flips,
        then samples the alphabet in threes.
    """
    q = [('H', 1.0), ('T', 1.0)]

    s = list(weighted_reservoir_replace(q, 1000))
   
    print "1000 flips, using weighted reservoir sampling with replacement"
    print s.count('H'), " Heads."
    print s.count('T'), " Tails."
    print "Look fair to you?"
    print ""

    print "Now we'll sample 1000 triples from the first ten letters of the alphabet"

    alpha = [ (c,1.0) for c in "abcdefghij" ]

    counts = dict([(c,0) for c in "abcdefghij"])

    for i in xrange(1000):
        for c in weighted_reservoir_noreplace(alpha,3):
            counts[c] += 1
    
    print "Got the following counts."
    print counts
