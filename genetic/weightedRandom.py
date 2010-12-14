import random

def WeightedPick(d):
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    for k, w in d.iteritems():
        s += w
        if r < s: return k
    return k

def Test():
    k = {'A': 68, 'B': 62, 'C': 47, 'D': 16, 'E': 81}
    results = {}
    for x in xrange(10000):
        p = WeightedPick(k)
        results[p] = results.get(p, 0) + 1
    print results

Test()
