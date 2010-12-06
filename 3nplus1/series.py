__author__ = 'julian'

def cascadeSeries(step, r = [] ):
    '''
    >>> cascadeSeries(6,[])
    [6, 3, 10, 5, 16, 8, 4, 2, 1]
    '''
    r.append(step)
    if step % 2 == 0:
        step = step // 2
    else:
        step = (step*3) + 1
    if step > 1:
        cascadeSeries(step,r)
    else:
        r.append(step)
    return r

def maxCycleLength(i,j):
    '''
    >>> maxCycleLength(2,6)
    (2, 6, 8)
    '''
    cyclelengths = dict()
    for n in range(i, j):
        cyclelength = len(cascadeSeries(n,[]))
        #print (str(n) + ' ' + '*' * cyclelength)
        cyclelengths[n] = cyclelength
    leader = max(cyclelengths,key = lambda a: cyclelengths.get(a))
    return i, j ,  cyclelengths[leader]



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print ("Start series")
    j = maxCycleLength(900,1000)
    print(j)