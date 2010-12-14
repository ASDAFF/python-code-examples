__author__ = 'julian'
''' From http://stackoverflow.com/questions/228181/zen-of-python
'''

# this is clever...
qsort1 = lambda lst : lst if len(lst) <= 1 else \
qsort1([i for i in lst[1:] if i < lst[0]]) + [lst[0]] + qsort1([i for i in lst[1:] if i >= lst[0]])
print (qsort1([2,4,2,3,7,5,4,8,77]))

# ... &this is succinct
def gcd(x, y):
    '''http://en.wikipedia.org/wiki/Greatest_common_divisor'''
    while y:
        x, y = y, x % y
    return x
print (gcd(8,12))

def _test():
    assert qsort1([2,4,77,3,7,5,4,8,2]) == [2, 2, 3, 4, 4, 5, 7, 8, 77], 'Quicksort does not work'
    assert gcd(8,12)== 4 , 'Greatest Common Divisor is broken!'
if __name__ == "__main__":
    _test()


print (' .. and now for something completely different')
import this