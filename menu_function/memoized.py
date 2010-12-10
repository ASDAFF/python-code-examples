''' Neat cache idea from
http://ubuntuforums.org/showthread.php?t=671254
try with and without the @memoized decorator : big difference in performance!
'''

def memoized(func):
    def inner(*args):
        try:
            return inner.cache[args]
        except KeyError:
            value = inner.cache[args] = func(*args)
            return value
        except TypeError:
            return func(*args)
    inner.cache = {}
    return inner


@memoized
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


@memoized
def binomial(m,n):
    if m < 0 or n > m:
        return 0
    if n == 0 or m == n:
        return 1
    return binomial(m - 1, n) + binomial(m - 1, n - 1)


print (fib(100))
print (binomial(40, 20))