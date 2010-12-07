__author__ = 'julian'
''' Calculate and manipulate the series formed by:
    taking a number (n), half it if even; 3n+1 if odd.
    Then calculate the longest series for n up to 1000.

    Code uses simple recursion & 'functions as objects'
'''

def cascadeSeries(step, r = [] ):
    '''
    >>> cascadeSeries(6)
    [6, 3, 10, 5, 16, 8, 4, 2, 1]
    '''
    def evencascade(s):
        return s // 2
    def oddcascade(s):
        return (s*3) + 1

    r.append(step)
    if step % 2 == 0:
        nextfn = evencascade
    else:
        nextfn = oddcascade
    step = nextfn(step)
    if step > 1:
        cascadeSeries(step,r)
    else:
        r.append(step)
    return r

def getmaxbyvalue(cyclelengths):
    '''
    >>> getmaxbyvalue({'a':3,'b':4,'c':2,'d':6,'e':3,'f':1})
    'd'
    '''
    return max(cyclelengths,key = lambda a: cyclelengths.get(a))

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
    leader = getmaxbyvalue(cyclelengths)
    return i, j ,  cyclelengths[leader]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print ("Start series")
    j = maxCycleLength(0,1000)
    print(j)