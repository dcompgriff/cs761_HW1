import scipy.io
import numpy as np


def main():
    #Read data
    mat = scipy.io.loadmat('brain_data1.mat')
    #Parse data into a more useable format
    data = {'A':[], 'B':[], 'C': []}
    for row in mat['xA']:
        data['A'].append(row[0])
    for row in mat['xB']:
        data['B'].append(row[0])
    for row in mat['xC']:
        data['C'].append(row[0])

    #Calculate variation in exact probability, and independence assumed probability
    #  for random subsets of the data to determine magnitude of variation.
    calculateVariability(data)

    #Calculate variation of probabilities for data.
    print("Total summed difference in probability: " + str(getEmpiricalTotalConditionalProbabilityDifference(data)))
    print("Uniformly distributed error per calculation: " + str(getEmpiricalTotalConditionalProbabilityDifference(data)/8))


'''
Calculate variability of inter-probability calculations.
'''
def calculateVariability(data):
    for A in [0, 1]:
        for B in [0, 1]:
            for C in [0, 1]:
                # Calculate variation in exact probability, and independence assumed probability
                #  for random subsets of the data to determine magnitude of variation.
                exactProbVariationMean = 0
                assumedIndepVariationMean = 0
                randIndexList = list(range(0, len(data['A'])))
                for k in range(0, 30):
                    # Shuffle data indecies.
                    np.random.shuffle(randIndexList)
                    firstHalf = {'A': [], 'B': [], 'C': []}
                    secondHalf = {'A': [], 'B': [], 'C': []}
                    for index in range(0, len(randIndexList) / 2):
                        firstHalf['A'].append(data['A'][randIndexList[index]])
                        firstHalf['B'].append(data['B'][randIndexList[index]])
                        firstHalf['C'].append(data['C'][randIndexList[index]])
                    for index in range(len(randIndexList) / 2, len(randIndexList)):
                        secondHalf['A'].append(data['A'][randIndexList[index]])
                        secondHalf['B'].append(data['B'][randIndexList[index]])
                        secondHalf['C'].append(data['C'][randIndexList[index]])
                    firstHalfExact, firstHalfAssumed = getEmpericalProbabilityDifference(firstHalf, A, B, C)
                    secondHalfExact, secondHalfAssumed = getEmpericalProbabilityDifference(secondHalf, A, B, C)

                    exactProbVariationMean += abs(firstHalfExact - secondHalfExact)
                    assumedIndepVariationMean += abs(firstHalfAssumed - secondHalfAssumed)

                print("Average exact probability variation (%d,%d,%d): "%(A,B,C) + str(exactProbVariationMean / 30.0))
                print("Average assumed independence probability variation (%d,%d,%d): "%(A,B,C) + str(assumedIndepVariationMean / 30.0))


'''
This method sums up the difference in the actual conditional probability
and independence assumed conditional probabilities over all settings
of A, B, and C.
'''
def getEmpiricalTotalConditionalProbabilityDifference(data):
    totalDifference = 0
    for A in [0, 1]:
        for B in [0, 1]:
            for C in [0, 1]:
                exactProb, assumedIndepProb = getEmpericalProbabilityDifference(data, A, B, C)
                totalDifference += abs(exactProb - assumedIndepProb)
    return totalDifference


'''
    Method computes the difference in the true conditional probability
    and independence assumed conditional probabilities for ONE setting
    of A, B, and C.

    @:param data Dictionary with 'A', 'B', and 'C' as keys, and arrays as values.
    @:param A value of A to use for calculation (0, or 1)
    @:param B value of B to use for calculation (0, or 1)
    @:param C value of C to use for calculation (0, or 1)
'''
def getEmpericalProbabilityDifference(data, A, B, C):
    #Calculate Pr(A, B, C)
    entryCount = 0
    for i in range(0, len(data['A'])):
        if A == data['A'][i] and B == data['B'][i] and C == data['C'][i]:
            entryCount += 1.0
    totalCount = len(data['A'])
    prA_B_C =entryCount / totalCount

    #Calculate Pr(B)
    entryCount = len(filter(lambda item: item==B, data['B']))
    prB = entryCount / float(totalCount)

    #cProb1 = Pr(A,C|B) = Pr(A,B,C) / Pr(B)
    cProb1 = prA_B_C / prB

    #Calculate Pr(A|B) = Pr(A,B) / Pr(B)
    entryCount = 0
    for i in range(0, len(data['A'])):
        if A == data['A'][i] and B == data['B'][i]:
            entryCount += 1.0
    prA_B = entryCount / totalCount

    #Calculate Pr(C|B) = Pr(C,B) / Pr(B)
    entryCount = 0
    for i in range(0, len(data['A'])):
        if C == data['C'][i] and B == data['B'][i]:
            entryCount += 1.0
    prB_C = entryCount / totalCount

    #cProb2 = Pr(A|B)*Pr(C|B)
    cProb2 = (prB_C*prA_B) / (prB**2)

    #If |cProb1 - cProb2| within experimental variation bound
    return cProb1, cProb2



if __name__ == "__main__":
    main()