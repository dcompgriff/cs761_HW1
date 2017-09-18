import scipy.io


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

    #Calculate variation of probabilities for data.
    print("Pr(A=1,B=1,C=1): " + str(getEmpericalProbabilityDifference(data, 1, 1, 1)[0]))
    print("Pr(A=1,B=1,C=1): " + str(getEmpericalProbabilityDifference(data, 1, 1, 1)[1]))

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
                totalDifference += getEmpericalProbabilityDifference(data, A, B, C)
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