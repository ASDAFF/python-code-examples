__author__ = 'julian'
"""
Given a list of palindromes & non-palindrome strings,
return only the actual palindromes.

Notes:

 Solution: use a deque to test for is_palindrome:

 A deque is a list-like data construction optimized to pop from either end of the structure
 Hence:
 pop - remove the right-most element
 popleft - remove the left-most element

 Other notes:

 - while - else clause
 - simultaneous variable assignment:
    ie  a, b = fn(a), fn(b)
 - there's some tests. Not enough, but some.

"""

import unittest
from collections import deque

def is_palindrome(sss):
    """
    >>> is_palindrome('aa')
    True
    >>> is_palindrome('aaaab')
    False
    """
    pal = deque(sss)
    left_end_char, right_end_char = '',''
    while pal:
        try:
            left_end_char,right_end_char = pal.popleft(), pal.pop()
            if left_end_char != right_end_char:
                return False
        except IndexError:
            #     one element remaining: so is a odd-number-of-letters palindrome
            # and we've exhausted the string
            pal = ''
    else:
        return True

def palindromefilter(pallist):
    return [word for word in pallist if is_palindrome(word)]

class TestPalindrome(unittest.TestCase):

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome('aaaa'))
        self.assertTrue(is_palindrome('aa'))
        self.assertTrue(is_palindrome('aaa'))
        self.assertTrue(is_palindrome('abba'))
        self.assertFalse(is_palindrome('aaab'))
        self.assertFalse(is_palindrome('aaabb'))
        self.assertFalse(is_palindrome('aaabbb'))
        self.assertFalse(is_palindrome('aaacbbb'))

    def test_list_of_strings(self):
        testlist = ['aa','bb']
        self.assertEqual(palindromefilter(testlist),testlist)
        self.assertEqual(palindromefilter(['aa','bb','ab']),testlist)
        self.assertEqual(palindromefilter(['aa','bba','bb','ab']),testlist)