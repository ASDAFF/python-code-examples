''' Fun example of how iterators work
From the classic site: http://99-bottles-of-beer.net/language-python-1028.html

Potential improvements for v0.2?:
- use namedtuple for the data
- on completion should use urllib to open amazon and order some more tasty fermented beverage.
- use polymorphism for the if statement. And for other beverages too.
'''

class Song:
    def __init__(self):
        self.n = 100

    def __iter__(self):
        return self

    def next(self):
        if self.n == 0:
            raise StopIteration
        self.n = self.n - 1
        return self._get_verse(self.n)

    def _get_verse(self,n):
        lines = []
        data  = []
        if n > 1:
            data.append(["%s bottles" % n,"%s bottles" % n])
            data.append(["Take one down pass it around","%s bottles" % (n-1)])
        elif n == 1:
            data.append(["%s bottle" % n,"%s bottle" % n])
            data.append(["Take one down pass it around","%s bottles" % "no more"])
        elif n == 0:
            data.append(["No more bottles","no more bottles"])
            data.append(["Go to the store and buy some more","%s bottles" % 99])

        lines.append("%s of beer on the wall, %s of beer" % tuple(data[0]))
        lines.append("%s, %s of beer on the wall" % tuple(data[1]))
        lines.append("")
        return "\n".join(lines)

song = Song()
for stanza in song:
    print stanza