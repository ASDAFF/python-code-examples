__author__ = 'julian'
'''
PRESENT A MENU
Based on a thread ( http://ubuntuforums.org/showthread.php?t=674595 ) regarding the most elegant/pythonic/'clever' way to present a menu
Clever is not necessarily a good thing (takes twice as much cleverness to maintain code as it is to write it, so it's good not to be too clever
in the initial writing.

This would all be easier using oop but for a change not using that paradigm.

Objectives:
- investigate functions as 1st class objects
- DRY: (don't repeat yourself) ie: everything menu related is in one dict.
- Passing arguments to decorators

Non Objectives:
- Object based polymorphism
- Elaborate use of decorators
- avoid global variables
'''

userloggedin = False
class userloginStatusCheck(object):
    '''ref: http://www.artima.com/weblogs/viewpost.jsp?thread=240845'''
    def __init__(self, userStatusMustBe):
        self.userStatusMustBe = userStatusMustBe
    def __call__(self, f):
        def wrapped_f(*args):
            if userloggedin == self.userStatusMustBe :
                f(*args)
            else:
                print "**You cannot do that**"
        return wrapped_f

@userloginStatusCheck(userStatusMustBe = False)
def login():
    global userloggedin
    print ('\n\nyou are now logged in')
    userloggedin = True

@userloginStatusCheck(userStatusMustBe = True)
def logout():
    global userloggedin
    print ('\n\n you are now logged out')
    userloggedin = False

def exitapp():
    print ('\n\nBye!')
    return True

def loginstatusmessage(userloggedin):
    if userloggedin:
        print ('You are currently logged in ')
    else:
        print ('You are currently NOT logged in ')


def main():
    global userloggedin
    print ('welcome to pybank\n')
    loginstatusmessage(userloggedin)
    for opts in sorted(availableOptions):
        print (' '.join((str(opts) , (availableOptions[opts]['text_en']))))
    choice = input("Select an option")
    if choice in availableOptions:
        r = availableOptions[choice]['fn']()
        return r
    else:
        print ('invalid choice')

r = None
userloggedin = False
availableOptions = dict()
availableOptions[1] = {'text_en':'log me in','fn':login}
availableOptions[2] = {'text_en':'log me out','fn':logout}
availableOptions[3] = {'text_en':'Exit the application','fn':exitapp}
while r == None:
    r = main()