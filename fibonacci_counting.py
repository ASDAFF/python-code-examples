import unittest
from collections import defaultdict
import pprint
FIB_LIST = [233, 144 , 89, 55, 34, 21, 13, 8, 5, 3, 2, 1]
NUMBER_OF_TERMS = 20
"""
Manipulating numbers using Fibonacci coding
http://en.wikipedia.org/wiki/Fibonacci_coding

which is (briefly):
normal base-10 counting uses ones,tens, hundeds for each column
and base-2 binary uses 1,2,4,8 etc.
Fibonacci coding uses the numbers 1,2,3,5 .. for each column so:
'0100100011' is in base-10 = 65
"""

def get_fib_value(fibstring):
    """
    turns a string into it's value using fibonacci counting
    example
    >>> get_fib_value('101')
    4
    """
    fib_list = list(FIB_LIST)
    result = 0
    for s in fibstring[::-1]:
        column_value = fib_list.pop()
        if s == '1':
            result += column_value
    return result


def generate_binary_string(n):
    """
    given a decimal number, provides a string representation of binary
    """
    return bin(n)[2:]


def build_fib_combination_dict(number_of_terms):
    """
    make a look up table for all fibonacci representations
    pow(2,FIB_LIST) -1  represents as binary 111111(...1)
    """

    r = defaultdict(list)
    for i in range(1, pow(2, len(FIB_LIST)) - 1):
        binstring = generate_binary_string(i)
        fibvalue = get_fib_value(binstring)
#        number_of_terms - if we only want to count up to a certain number
        if (fibvalue <= number_of_terms):
            r[fibvalue].append(binstring)
    return r


def zeckendorf(fib_dict):
#    zeckendorf's theorem
    filteredDictionary = {}
    for key in fib_dict:
        filteredDictionary[key] = [i for i in fib_dict[key] if '11' not in i]
    return filteredDictionary


FIBONACCI_LOOKUP = build_fib_combination_dict(number_of_terms= NUMBER_OF_TERMS)
ZECKENDORF_LOOKUP = zeckendorf(FIBONACCI_LOOKUP)
pprint.pprint(ZECKENDORF_LOOKUP)
class TestFibonacci(unittest.TestCase):
    def setUp(self):
        pass

    def test_fib(self):
        # make sure the shuffled sequence does not lose any elements
        self.assertEqual(get_fib_value('1'), 1)
        self.assertEqual(get_fib_value('10'), 2)
        self.assertEqual(get_fib_value('100'), 3)
        self.assertEqual(get_fib_value('11'), 3)
        self.assertEqual(get_fib_value('101'), 4)
        self.assertEqual(get_fib_value('1000'), 5)
        self.assertEqual(get_fib_value('110'), 5)
        self.assertEqual(get_fib_value('100000'), 13)

    def test_binarycreator(self):
        self.assertEqual(generate_binary_string(1), '1')
        self.assertEqual(generate_binary_string(2), '10')
        self.assertEqual(generate_binary_string(3), '11')
        self.assertEqual(generate_binary_string(4), '100')
        self.assertEqual(generate_binary_string(5), '101')


    def test_fib_convert(self):
        self.assertEqual(FIBONACCI_LOOKUP[1], ['1'])
        self.assertEqual(FIBONACCI_LOOKUP[2], ['10'])
        self.assertEqual(FIBONACCI_LOOKUP[3], ['11', '100'])
        self.assertEqual(FIBONACCI_LOOKUP[4], ['101'])
        self.assertEqual(FIBONACCI_LOOKUP[5], ['110', '1000'])
        self.assertEqual(FIBONACCI_LOOKUP[20], ['101010'])
        self.assertEqual(len(FIBONACCI_LOOKUP), NUMBER_OF_TERMS)

    def test_zendorf_convert(self):
        self.assertEqual(ZECKENDORF_LOOKUP[1], ['1'])
        self.assertEqual(ZECKENDORF_LOOKUP[2], ['10'])
        self.assertEqual(ZECKENDORF_LOOKUP[3], ['100'])
        self.assertEqual(ZECKENDORF_LOOKUP[4], ['101'])
        self.assertEqual(ZECKENDORF_LOOKUP[5], ['1000'])
        self.assertEqual(ZECKENDORF_LOOKUP[20], ['101010'])
        self.assertEqual(len(ZECKENDORF_LOOKUP), NUMBER_OF_TERMS)




if __name__ == '__main__':
    unittest.main()
