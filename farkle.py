import collections
import random


def getScore(dice):
    '''Return a Farkle score and the indicies of the scoring dice'''
    dice.sort()
    if dice == [1, 2, 3, 4, 5, 6]:
        return 1500, range(6)
    elif any([dice == [x, x, x, y, y, y] for x in range(1, 4)
              for y in range(4, 7)]):
        return 2500, range(6)
    elif any([dice.count(x) == 4 and dice.count(y) == 2
              for x in range(1, 7) for y in range(1, 7)]):
        return 1500, range(6)
    elif any([dice == [x, x, y, y, z, z] for x in range(1, 3)
              for y in range(3, 5) for z in range(5, 7)]):
        return 1500, range(6)
    elif any([dice.count(x) == 6 for x in range(1, 7)]):
        return 3000, range(6)
    cumScore = 0
    counter = collections.Counter(dice)
    for i in range(1, 7):
        if counter[i] == 5:
            cumScore += 2000
            cumScore += addOnesFives(i, counter)
            return cumScore, getIndexScoring(dice, i)
        if counter[i] == 4:
            cumScore += 1000
            cumScore += addOnesFives(i, counter)
            return cumScore, getIndexScoring(dice, i)
        if counter[i] == 3:
            if i != 1:
                cumScore += i*100
            else:
                cumScore += 300
            cumScore += addOnesFives(i, counter)
            return cumScore, getIndexScoring(dice, i)
    cumScore += counter[1]*100
    cumScore += counter[5]*50
    return cumScore, getIndexScoring(dice, 0)


def getIndexScoring(dice, i):
    return [ix for ix in range(len(dice))
            if dice[ix] == i or dice[ix] == 5 or dice[ix] == 1]


def addOnesFives(i, counter):
    score = 0
    if i != 1:
        score += counter[1]*100
    if i != 5:
        score += counter[5]*50
    return score


def testScore():
    assert getScore([5, 4, 3, 2, 1, 6])[0] == 1500
    assert getScore([6, 6, 6, 2, 2, 2])[0] == 2500
    assert getScore([4, 4, 4, 1, 1, 1])[0] == 2500
    assert getScore([6, 6, 6, 6, 1, 1])[0] == 1500
    assert getScore([6, 6, 2, 2, 4, 4])[0] == 1500
    assert getScore([1, 1, 1, 1, 1, 1])[0] == 3000
    assert getScore([5, 5, 5, 5, 2, 3])[0] == 1000
    assert getScore([5, 5, 5, 5, 5, 2])[0] == 2000
    assert getScore([2, 2, 2, 2, 2, 1])[0] == 2100
    assert getScore([2, 2, 2, 2, 1, 5])[0] == 1150
    assert getScore([6, 6, 6, 2, 3, 3])[0] == 600
    assert getScore([6, 6, 6, 1, 1, 5])[0] == 850
    assert getScore([2, 2, 2, 1, 3, 3])[0] == 300
    assert getScore([1, 1, 1, 5, 5, 2])[0] == 400
    assert getScore([1, 1, 2, 3, 4, 4])[0] == 200
    assert getScore([1, 5, 2, 3, 4, 4])[0] == 150
    assert getScore([2, 3, 4, 6, 6, 2])[0] == 0
    assert getScore([1, 2, 3, 4, 5, 6])[1] == [0, 1, 2, 3, 4, 5]
    assert getScore([1, 1, 2, 3, 4, 5])[1] == [0, 1, 5]
    assert getScore([1, 1, 1, 2, 5, 6])[1] == [0, 1, 2, 4]
    print("Scoring test passed!")


testScore()


def rollDice(numDice):
    return [random.randint(1, 6) for x in range(numDice)]


def getFarklePercentages(numRolls):
    '''Monte Carlo simulation of rolling 1, 2, 3, ... dice for numRolls and
    counting the number of times the score is zero'''
    farkleCount = []
    for x in range(1, 7):
        scores = [getScore(dice)[0]
                  for dice in [rollDice(x) for y in range(numRolls)]]
        farkleCount.append(scores.count(0))

    farklePcts = [x*100.0/numRolls for x in farkleCount]
    str2print = "Farkle percent for {} {}: {:5.2f}"
    for i, farklePct in enumerate(farklePcts):
        diceTxt = "dice" if i != 0 else "die "
        print(str2print.format(i+1, diceTxt, farklePct))
    print("")


getFarklePercentages(10000)


def summation(vals):
    return reduce(lambda x, y: x + y, vals)


def average(vals):
    return summation(vals)/float(len(vals))


def stdDev(vals):
    mean = average(vals)
    return (summation([(x - mean)**2 for x in vals])/float(len(vals)-1))**0.5


def getExpectedValues(numRolls):
    '''Get the expected value or average score for each roll of a number of
    dice based on Monte Carlo simulation'''
    expectedValues = []
    for x in range(1, 7):
        scores = [getScore(dice)[0]
                  for dice in [rollDice(x) for y in range(numRolls)]]
        expectedValues.append(average(scores))

    str2print = "Expected value for {} {}: {:6.2f}"
    for i, expectedValue in enumerate(expectedValues):
        diceTxt = "dice" if i != 0 else "die "
        print(str2print.format(i+1, diceTxt, expectedValue))
    print("")


getExpectedValues(10000)


def simulateStrategy(func, numSims):
    '''Pass a function (func) and the number of simulations to run (numSims) and
    this function will print the average number of plays to reach 10,000 points
    , a winning score.

    The function needs to return only the  number of plays that it took to get
    to 10,000 points'''
    counts = []
    for i in range(numSims):
        counts.append(func())
    avg = average(counts)
    std = stdDev(counts)
    str2print = "Average number of plays to {} points for {}: {}"
    print(str2print.format(numSims, func.__name__, avg))
    str2print = "Std. deviation for number of plays for {}: {}"
    print(str2print.format(func.__name__, std))


def keepGreaterThanX(X):
    '''A farkle strategy where one keeps any amount of points obtained greater
    than X and also naively keeping all points on a roll'''
    score, currentTurnScore, numDice, numTurns = 0, 0, 6, 0
    while score < 10000:
        currentRollScore, scoringIdx = getScore(rollDice(numDice))
        currentTurnScore += currentRollScore
        if currentRollScore == 0:
            numDice, currentTurnScore = 6, 0
            numTurns += 1
            continue
        if currentTurnScore > X:
            score += currentTurnScore
            currentTurnScore = 0
            numDice = 6
            numTurns += 1
        else:
            numDice -= len(scoringIdx)
    return numTurns


def strategy1():
    '''A slightly better strategy, maybe the best?'''
    score, currentTurnScore, numDice, numTurns = 0, 0, 6, 0
    while score < 10000:
        dice = rollDice(numDice)
        currentRollScore, scoringIdx = getScore(dice)
        takeScoreLimit = 13.55*numDice**2-34.19*numDice+54.1
        if currentRollScore == 0:
            numDice, currentTurnScore = 6, 0
            numTurns += 1
            continue
        if len(scoringIdx) == numDice:
            currentTurnScore += currentRollScore
            numDice = 6
            continue
        if currentRollScore+currentTurnScore > takeScoreLimit:
            score += currentTurnScore+currentRollScore
            numDice, currentTurnScore = 6, 0
            numTurns += 1
        else:
            numOnes = dice.count(1)
            numFives = dice.count(5)
            if numOnes > 0:
                currentTurnScore += 100
                numDice -= 1
            elif numFives > 0 and len(scoringIdx) < 3:
                currentTurnScore += 50
                numDice -= 1
            else:
                currentTurnScore += currentRollScore
                numDice -= len(scoringIdx)
    return numTurns


simulateStrategy(lambda: keepGreaterThanX(220), 10000)
simulateStrategy(strategy1, 10000)
