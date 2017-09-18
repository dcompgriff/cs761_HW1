import random

pdf = [
    [0.0267, 0.0697, 0.0775, 0.0313, 0.0101],
    [0.0283, 0.0761, 0.0739, 0.0566, 0.0362],
    [0.0109, 0.0337, 0.0552, 0.0780, 0.0740],
    [0.0014, 0.0093, 0.0309, 0.0750, 0.0698],
    [0.0001, 0.0028, 0.0124, 0.0318, 0.0283]
]


def main():
    parta()
    partb(10)
    #partc1()
    #partc2()
    #partc1Test()
    #partc2Test()



def parta():
    randStudent = random.random() * (8094 - 0 + 0)
    print("Part a: %d" % (randStudent))


def partb(k):
    for i in range(0, k):
        randStudent = random.random() * (8094 - 0 + 0)
        print("Student %d: %d" % (i+1, randStudent))


def partc1():
    x1 = random.random()
    x2 = random.random()

    '''
    Question: We could solve this 2 ways correct?
        1) By summing element wise through the matrix until we find
        the proper bucket.
        2) By finding the marginal dist for x1, x2, and then finding the
        location of x1, and x2 separately.
    '''

    X1X2RandPoint = random.random()
    x1Value = 0;
    x2Value = 0;
    #Method 1)
    pdfSum = 0
    for row in range(0, len(pdf)):
        for col in range(0, len(pdf[0])):
            pdfSum += pdf[row][col]
            if X1X2RandPoint <= pdfSum:
                x1Value = row
                x2Value = col
                #print("x1Value: " + str(x1Value))
                #print("x2Value: " + str(x2Value))
                return x1Value, x2Value

def partc2():
    x1 = random.random()
    x2 = random.random()

    '''
    Question: We could solve this 2 ways correct?
        1) By summing element wise through the matrix until we find
        the proper bucket.
        2) By finding the marginal dist for x1, x2, and then finding the
        location of x1, and x2 separately.
    Answer: No! Empirically, these don't both match. The second procedure
        must assume some sort of independence. Work out the mathematical
        equation that corresponds to this assumption. Empirically, the table
        generated is equivalent to P(x1, x2) = p(x1)*p(x2)
    '''

    #Method 2)
    x1MarginalPdf =[]
    for row in pdf:
        x1MarginalPdf.append(sum(row))
    x2MarginalPdf = []
    for col in range(0, len(pdf[0])):
        mSum = 0
        for row in range(0, len(pdf)):
            mSum += pdf[row][col]
        x2MarginalPdf.append(mSum)
    print("x1 marginal pdf: " + str(x1MarginalPdf))
    print(sum(x1MarginalPdf))
    print("x2 marginal pdf: " + str(x2MarginalPdf))
    print(sum(x2MarginalPdf))
    x1pdfSum = 0
    x1Value = 0
    for row in range(0, len(x1MarginalPdf)):
            x1pdfSum += x1MarginalPdf[row]
            if x1 <= x1pdfSum:
                x1Value = row
                print("x1Value: %d" % (x1Value))
                break

    x2pdfSum = 0
    x2Value = 0
    for col in range(0, len(x2MarginalPdf)):
        x2pdfSum += x2MarginalPdf[col]
        if x2 <= x2pdfSum:
            x2Value = col
            print("x2Value: %d" % (x2Value))
            break
    return x1Value, x2Value


def partc1Test():
    buckets = [ [0 for col in range(0, 5)] for row in range(0, 5)]
    for i in range(0, 100000):
        x1, x2 = partc1()
        buckets[x1][x2] += 1

    for row in range(0, len(buckets)):
        for col in range(0, len(buckets[0])):
            buckets[row][col] /= 100000.0
    for row in range(0, len(buckets)):
        print(buckets[row])

def partc2Test():
    buckets = [[0 for col in range(0, 5)] for row in range(0, 5)]
    for i in range(0, 100000):
        x1, x2 = partc2()
        buckets[x1][x2] += 1

    for row in range(0, len(buckets)):
        for col in range(0, len(buckets[0])):
            buckets[row][col] /= 100000.0
    for row in range(0, len(buckets)):
        print(buckets[row])


if __name__ == "__main__":
    main()





