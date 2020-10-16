#!/usr/bin/env python3.7
from collections import Counter as _counter
from math import log2 as _log2


# region Helper Functions
def decimalToVector(i, l):
    """Returns a vector of 'l' bits representing 'i'."""
    # I use map to make an iterable containing
    # the individual bits in integer form.
    return list(map(int, f"{i:0{l}b}"))


def _multiplyVectorByMatrix(vector, matrix):
    """Returns the vector resulting from multiplying a vector by a matrix.
    
    The vector and matrix must only have elements that are binary bits
    """
    result = [
        sum(
            # Each element in the vector is multiplied by the 
            # corresponding value in the current column vector.
            matrix[row][column] * value
            for row, value in enumerate(vector)
            # Can safely ignore elements that are 0 as I am multiplying
            # and so they won't contribute
            if value != 0
        ) % 2
        for column in range(len(matrix[0]))
    ]

    return result

# endregion Helper Functions


# region Functions for repetition codes
def repetitionEncoder(m, n):
    """Returns the element of the 1x1 vector 'm' repeated 'n' times."""
    encoded = [
        m[0]
        for i in range(n)
    ]

    return encoded


def repetitionDecoder(v):
    """Returns the decoded repetition code given by the vector 'v'."""
    # Gives the most commonly occuring element
    # as well as the number of occurences.
    occurrences = _counter(v).most_common(1)[0]

    # Checks if the number of occurences isn't
    # half the length of the vector v.
    if occurrences[1] != len(v)/2:
        code = [occurrences[0]]
    else:
        code = []

    return code

# endregion Functions for repetition codes


# region Functions for Hamming codes
def message(a):
    """Converts 'a' into a message for Hamming Code.

    'a' is a vector of any positive length
    """
    length = len(a)

    # Calculate r    
    part = 0
    r = 1
    while part < length:
        r += 1
        part = 2**r - 2*r - 1

    k = part + r

    # Form the remaing parts of the message and combine them
    binaryLength = decimalToVector(length, r)
    padding = [0 for i in range(k - r - length)]

    code = binaryLength + a + padding

    return code


def hammingEncoder(m):
    """Encodes the message represented by 'm' using Hamming Codes.

    'm' is a vector of length 2^r -r - 1 where r >= 2
    """
    k = len(m)

    # Calculate r
    # This also checks if m is of a valid length
    r = 1
    testValue = 0
    while testValue < k:
        r += 1
        testValue = 2**r - r - 1
        if testValue > k:
            c = []
            break

    else:
        generatorMatrix = hammingGeneratorMatrix(r)

        # Encode m using the generatorMatrix
        c = _multiplyVectorByMatrix(m, generatorMatrix)

    return c


def hammingDecoder(v):
    """Decodes the Hamming Code represented by 'v' using Syndrome decoding.

    'v' is a vector of length 2^r - 1 with r >= 2
    """
    # Calculate r
    r = _log2(len(v) + 1)
    if not r.is_integer():
        return []
    else:
        r = int(r)

    # Construct the parity check matrix.
    # Due to the construction method it is already transposed.
    parityCheckMatrixTranspose = [
        decimalToVector(number, r)
        for number in range(1, 2**r)
    ]

    # Multiplying v by the transpose of the parity check
    # matrix gives the position of the error in binary form.
    errorPosition = _multiplyVectorByMatrix(v, parityCheckMatrixTranspose)

    # Find the index of the error by converting to decimal.
    # Subtract 1 due to 0 index
    errorIndex = int("".join(map(str, errorPosition)), 2) - 1

    v[errorIndex] = (v[errorIndex] + 1)%2

    return v


def messageFromCodeword(c):
    """Extracts the message sent from the codeword represented by 'c'.

    'c' is a vector of length 2^r - 1 with r >= 2
    """
    length = len(c)

    # Calculate r
    # This also checks if c is of a valid length
    r = _log2(length + 1)
    if not r.is_integer():
        return []

    # Message extracted by ignoring all values in positions that
    # correspond to powers of 2 (after adjusting for zero index)
    m = [
        value
        for index, value in enumerate(c)
        if not _log2(index + 1).is_integer()
    ]

    return m


def dataFromMessage(m):
    """Recovers the raw data from the message represented by 'm'.

    'm' is a vector of length 2^r - r - 1 with r >= 2
    """
    k = len(m)

    # Calculate r
    # This also checks if m is of a valid length
    r = 1
    testValue = 0
    while testValue < k:
        r += 1
        testValue = 2**r - r - 1
        if testValue > k:
            a = []
            break
    else:
        # Extract the relevant part of m to get the length
        length = int("".join(map(str, m[:r])), 2)
        # From that we have the end index of the data
        dataEndIndex = r + length

        # Another check if m is valid by
        # checking if the end index is within m
        if dataEndIndex > k:
            a = []
        else:
            a = m[r:dataEndIndex]

    return a

# endregion Functions for Hamming codes


# region Lecturer's Code
#function HammingG
#input: a number r
#output: G, the generator matrix of the (2^r-1,2^r-r-1) Hamming code
def hammingGeneratorMatrix(r):
    n = 2**r-1

    #construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2**(r-i-1))
    for j in range(1,r):
        for k in range(2**j+1,2**(j+1)):
            pi.append(k)

    #construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i+1))

    #construct H'
    H = []
    for i in range(r,n):
        H.append(decimalToVector(pi[i],r))

    #construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n-r):
        GG.append(decimalToVector(2**(n-r-i-1),n-r))

    #apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    #transpose    
    G = [list(i) for i in zip(*G)]

    return G
# endregion Lecturer's Code

