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

# These from http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
''' idiom for formatting a human readable list'''
colors = ['red', 'blue', 'green', 'yellow']
print 'Choose', ', '.join(colors[:-1]), 'or', colors[-1]

def bad_append(new_item, a_list=[]):
    a_list.append(new_item)
    return a_list
print bad_append('one')
#['one']
print bad_append('two')
#['one', 'two']

def good_append(new_item, a_list=None):
    if a_list is None:
        a_list = []
    a_list.append(new_item)
    return a_list
print good_append('one')
#['one']
print good_append('two')
#['two']

# Advanced % String Formatting
values = {'name': 'bob', 'messages': 42}
print ('\nHello %(name)s, you have %(messages)i messages' % values)
#print locals()


print ('\n .. and now for something completely different...')
import this