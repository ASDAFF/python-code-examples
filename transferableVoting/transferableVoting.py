class Vote(object):
    '''
    Votes for one person: candidates are listed in order
    >>> v = Vote()
    >>> v.castVote(1)
    >>> v.castVote(2)
    >>> v.getVotes()
    [1, 2]
    >>> v = Vote()
    >>> v.castBallot([2,3,4])
    >>> v.castVote(5)
    >>> v.getVotes()
    [2, 3, 4, 5]
     
'''
    def __init__(self,ballot = None):
        ''' Vote object holds a persons multiple transferable votes'''
        self.votes = [ ]
        if ballot:
            self.votes = ballot
        
    def castVote(self,vote):
        self.votes.append (vote)

    def getVotes(self):
        return self.votes

    def getCurrentVote(self):
        try:
            return self.votes[0]
        except IndexError:
            return 'None'

    def castBallot(self,vote):
        self.votes = vote

    def transferVote(self,knockoutvote):
        ''' who is being removed from consideration? '''
        try:            
            self.votes.remove(knockoutvote)
        except (ValueError,IndexError):
            return 'None'

    def output(self):
        print (self.votes)

    def testVote(self):
        v = Vote()
        v.castVote(1)
        v.castVote(2)        
        assert v.getVotes() == [1,2] , 'cast individual Votes fails'
    
        v = Vote()
        v.castBallot([2,3,4])
        v.castVote(5)
        assert v.getVotes() == [2,3,4,5] , 'cast ballot fails' 
    
        v = Vote()
        v.castBallot([2,3,4])
        v.transferVote(2)
        assert v.getVotes() == [3,4] , 'transfer vote fails'
        v.transferVote(3)
        assert v.getVotes() == [4] , 'transfer vote fails'

class election(list):
    ''' an election is a collection of votes'''
    def __init__(self,votelist = [],*args):
        super(election, self).__init__(*args)
        if votelist:
            for f in votelist:
                self.submit(f)

        
    def submit(self,vote):
        '''submit a vote into the election'''
        return self.append(vote)

    def transferVote(self,knockoutvote):
        ''' someone has been removed from the contest, so all of their votes are applied to the remaining contestants'''
        for f in self:
            f.transferVote(knockoutvote)

    @property
    def getNumberOfVoters(self):
        ''' How many people have voted?'''
        return len(self)

    def output(self):
        for f in self:
            f.output()
    
    def electionTest(self):
        e = election()
        v = Vote()
        v.castVote(1)
        e.submit(v)
        assert e[0] == v, 'vote not counted'
        assert len(e) == 1, '# votes wrong'
        w = Vote()
        w.castVote(2)
        w.castVote(3)
        e.submit(w)
        assert e[0] == v, 'vote not counted'
        assert e[1] == w, 'vote not counted'
        assert len(e) == 2, '# votes wrong'
        e.transferVote(1) # votes for '1' will now be ignored.
        assert len(e) == 2, '# votes wrong'
        assert v.getVotes() == []
        assert w.getVotes() == [2,3], 'w should not change'
        e.transferVote(2) # votes for '2' will now be ignored.
        assert w.getVotes() == [3], 'w not changed'
        x = Vote()
        x.castVote(3)
        x.castVote(2)
        e.submit(x)
        e.submit(w)
        assert e.getNumberOfVoters == 4 , 'vote count fails'
        
        r = results(e)

class results(dict):
    ''' when given an election object this processes,counts and outputs the results '''
    def __init__(self,election):
        self.election = election
        self.NoVotesCast = election.getNumberOfVoters

    def calculateVotes(self):
        for f in self.election:
            currentVote = f.getCurrentVote()
            if currentVote in self:
                self[currentVote] += 1
            else:
                self[currentVote] = 1

    def calculatewinner(self):
        self.calculateVotes()
        d = self
        loser = min (d,key = lambda a: d.get(a))
        leader = max(d,key = lambda a: d.get(a))
        leaderVoteCount = self[leader]
        if leaderVoteCount > self.NoVotesCast // 2 :
            # we have a winner
            print (str(leader) + ' is the winner')
            return leader
        else:
            if loser == 'None':
                # this means there's a tie
                print ('No clear winner of this election.')
                print (self.election)
                raise Exception( 'No winner for the election.')
            #another round of tranferable voting
            print (str(loser) + ' is knocked out of the race')
            # remove the loser from the election consideration
            e = self.election
            e.transferVote(loser)
            # see if we have a winner again
            self = results(e)
            self.calculatewinner()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    print ("Start Transferable vote")
    v= Vote()
    v.testVote()
    e = election()
    e.electionTest()

    f = election([
        Vote([1, 4, 5]),
        Vote([3, 5, 4]),
        Vote([3, 5, 6]),
        Vote([4, 5, 3]),
        Vote([1, 5, 3]),        
        ])
    f.output()
    r = results(f)
    r.calculatewinner()
    ''' produces:
    
    [1, 4, 5]
    [3, 5, 4]
    [3, 5, 6]
    [4, 5, 3]
    [1, 5, 3]
    4 is knocked out of the race
    5 is knocked out of the race
    3 is the winner
    '''