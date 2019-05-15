#!/usr/bin/python

from random import Random
import copy

def completed_number(prefix, length, generator):
    ccnumber = prefix
    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)
    sum = 0
    pos = 0
    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()
    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9
        sum += odd
        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])
        pos += 2
    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append(str(int(checkdigit)))
    return ''.join(ccnumber)


def credit_card_number():
    mastercardPrefixList = [['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]
    generator = Random()
    generator.seed()
    ccnumber = copy.copy(generator.choice(mastercardPrefixList))
    return completed_number(ccnumber, 16, generator)



