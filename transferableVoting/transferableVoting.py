#SOME COOL CHANGES
# an alternate reality here
class Vote(object):
    def __init__(self,ballot = None):
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
        except ValueError,IndexError:
            return 'None'

    def output(self):
        print self.votes

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
        if votelist:
            for f in votelist:
                self.submit(f)
        super(election, self).__init__(*args)
        
    def submit(self,vote):
        return self.append(vote)

    def transferVote(self,knockoutvote):
        for f in self:
            f.transferVote(knockoutvote)

    def getNumberOfVotes(self):
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
        assert e.getNumberOfVotes() == 4 , 'vote count fails'
        
        r = results()
        print r.calculateWinner(e)

class results(list):
    ''' given an election object, this counts the results '''
    def calculateVotes(self,election):
        import operator
        self.results  = {}
        for f in election:
            currentVote = f.getCurrentVote()
            if self.results.has_key(currentVote):
                self.results[currentVote] += 1
            else:
                self.results[currentVote] = 1
        # convert results to a list of tuples
        sortedresults = sorted(self.results.iteritems(), key=operator.itemgetter(1))
        return   sortedresults

    def outputResults(self,results):
        print'(candidate, # votes)'
        for r in results:
            print r


    def calculateWinner(self,e):
        print  'start calc'
        e.output()
        results = self.calculateVotes(e)
        winner = results[-1]
        loser = results[0]
        while winner[1]<(e.getNumberOfVotes() % 2):
            e.transferVote(loser[0])
            results = self.calculateVotes(e)
            winner = results[-1]
            loser = results[0]
            print 'winner, loser '
            print winner, loser
        print 'winner'
        print winner    

     
if __name__ == "__main__":
    print "Start Transferable vote"
    v= Vote()
    v.testVote()
    e = election()
    e.electionTest()
    
    #r.testresults()
    e = election([
        Vote([3,4,5]),
        Vote([3,5,4]),
        Vote([3,5,6]),
        Vote([4,5,3]),
        ])
    e.output(   )
    r = results()
    r = r.calculateWinner(e)


    print "bye World!"

