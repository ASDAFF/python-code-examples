__author__ = 'julian'
''' http://programming-challenges.com/pg.php?page=downloadproblem&probid=110502&format=html

Start with a number (n) and reverse the digits then add it back to n. Continue until the result
is a palindrome number (same digits forwards as reverse)
ie: aaabbcbbaa etc
'''
def reverseNumber(n):
    '''
     >> reverseNumber(123)
     321
    '''
    l = list(str(n))
    l.reverse()
    r = ''.join(l)
    return int(r)

def is_palindrome(n):
    '''
    >>> is_palindrome(12345)
    False
    >>> is_palindrome(123454321)
    True
    '''
    chopStringfn = lambda s : s[:len(s)//2]
    s = str(n)

    s_list_fwd = list(s)
    s_list_rev = list(s)
    s_list_rev.reverse()
    r = chopStringfn(s_list_rev) == chopStringfn(s_list_fwd)
    return r

def revAndAdd(n):
    '''
    >>> revAndAdd(195)
    (195, 591) = 786
    (786, 687) = 1473
    (1473, 3741) = 5214
    (5214, 4125) = 9339
    9339 is a palindrome
    '''
    loops = 0
    while not is_palindrome(n):
        loops += 1
        if loops >1000:
            raise Exception( 'No palindrome found for that number.')
        m = reverseNumber(n)
        r = n + m
        print ((str((n,m))) + ' = '+ str(r))
        n = r
    print (str(n) + ' is a palindrome')

if __name__ == "__main__":
    import doctest
    doctest.testmod()

print ("Start reverse and add")
revAndAdd(197)
