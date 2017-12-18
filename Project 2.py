"""
    Nicholas Walters
    22243339
    Project 2
"""

# OPTIONAL PREFERENTIAL VOTING NOT ALLOWED

import operator
# import may not be needed

def getCandidates(f):
    # open text file, and put all content of it into an array/list
    lines = []
    try:
        with open(f) as file:
            pass
            for line in file:
                if any(x.isalpha() for x in line.strip('\n')):
                    lines.append(line.strip('\n'))
    except IOError:
        print("Cannot find file: " + f)
    return lines


inf_count = 0
def getVotes(g, candCount):
    # open text file containing votes, put all contents of it, into list of lists
    finalArray = []
    contents = open(g, "r")
    voteCount = 0
    for line in contents:
        lineArray = list(map(int, line.strip('\n').split(",")))
        finalArray.append(lineArray)
    return finalArray



def countCandidates(f):
    # count number of candidates
    result = getCandidates(f)
    count = 0
    for person in result:
        count = count + 1
    return count



def checkMajority(results):
    # check if a specific candidate has reached the majority of votes
    # where candidate wins, 50% all votes + 1
    sumVotes = sum(results)
    cutoff = (sumVotes / 2) + 1
    for candTotal in results:
        if(candTotal >= cutoff):
            return True
    return False



def countVotes(vList):
    # count the frequency of first preference votes (function used only once)
    candPrefs = []

    for vote in vList:
        minIndex = vote.index(min(vote))
        candPrefs.append(minIndex)
    return candPrefs



def countPrefs(candPrefs, candCount):
    # get the frequency of votes from countvotes() and format it correctly
    results = []

    for index_of_cand in range(0, candCount):
        voteCount = candPrefs.count(index_of_cand)
        results.append(voteCount)
    return results





def eliminateCand(results, elimCand):
    # put all results in a temporary array to fiddle with
    temp_results = []
    for x in results:
        temp_results.append(x)

    # change temporary array, so that you wont get the index of an already eliminated candidate
    for ci in elimCand:
        temp_results[ci] = 90000000

    minIndex = temp_results.index(min(temp_results))
    return minIndex


                 
                
def redistrobute(vList, results, candIndex, n, elimCand):

    for ballot in vList:
        # search every ballot paper, for votes where an eliminated candidate has had #1 vote
        value = ballot[candIndex]
        if(value == 1):
            next = True
            # the next preference is #2, it will be incremented if needed
            pref = 2
            while(next):
                #find the index of the candidate which has vote of #2 or specified preference (eg #3, #4, #5, #6)
                index = ballot.index(pref)
                count = 0
                for ci in elimCand:
                    count = count + 1
                    if(index == ci):
                        pref = pref + 1
                        count = -111
                    # if the specified preference belongs to a candidate who is already eliminated..
                    # then find the next preference

                if(count == len(elimCand)):
                    # the preference is found, and that preferences candidate is incremented
                    # next is false, because the program has found the next preference
                    iBallot = ballot.index(pref)
                    results[iBallot] = results[iBallot] + 1
                    count = 0
                    next = False
    return results
                    



def printCount(n, results, candidatesList, elimCand):
    print("Count " + str(n))
    
    d = {}
    i = 0
    # sort the results from largest to smallest
    for cand in candidatesList:
        d[cand] = results[i]
        i = i+1
    sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

    # get rid of eliminated candidates from results list
    # this prevents them from being printed out
    for i in range(0, len(elimCand)-1):
        del sorted_d[-1]
        
    # print out values of each candidate
    for x in sorted_d:
        print(str(x[1]) + "    " + x[0])

    candNum = elimCand[-1]
    if(len(sorted_d) > 2):
        print()
        print("Candidate " + candidatesList[candNum] + " has the smallest number of votes and is eliminated from the count")
        print()
    else:
        print()
        print()
        value_one = 0
        value_two = 0
        i = 0
        for x in sorted_d:
            if(i==0):
                value_one = x[1]
                person_one = x[0]
            if(i==1):
                value_two = x[1]
                person_two = x[0]
            i = i + 1
        # find the highest value of the two remaining candidates
        if(value_one > value_two):
            print("Candidate " + person_one + " is elected")
        elif(value_two > value_one):
            print("Candidate " + person_two + " is elected")
        else:
            print("Candidates are tied. Please elect candidate outside voting.")
        print(str(inf_count) + " papers excluded as informal")
        

    
def main(candidates_file_name, ballots_file_name, optional=False):
    # provide starting values
    candtxt = candidates_file_name
    paperstxt = ballots_file_name
    candidatesList = getCandidates(candtxt)
    candCount  = countCandidates(candtxt)
    vList = getVotes(paperstxt, candCount)
    candPrefs = countVotes(vList)
    elimCand = []
    n = 1

    # initiate calculation
    results = countPrefs(candPrefs, candCount)
    elimCand.append(eliminateCand(results, elimCand))
    printCount(n, results, candidatesList, elimCand)
    majority = checkMajority(results)

    # provide two conditions, to be extra sure when to stop the program
    while((not majority) or (candCount-1 == n)):
        n = n + 1
        results = redistrobute(vList, results, elimCand[-1], n, elimCand)
        elimCand.append(eliminateCand(results, elimCand))
        printCount(n, results, candidatesList, elimCand)
        majority = checkMajority(results)

        # extra check
        if(n == candCount-1):
            break

