MARK1 = 10
MARK2 = 7
MARK3 = 5
MARK4 = 3
MARK5 = 0


def Q1(marks):
    if marks in ("More_than_90%", "Between_80%_90%"):
        return MARK1 * 0.8
    elif marks in ("Between_70%_80%", "Between_70%_90%"):
        return MARK2 * 0.8
    elif marks == "Between_60%_70%":
        return MARK3 * 0.8
    else:
        return MARK4 * 0.8


def Q7_9(x):
    if x in ("sports", "singing", "media", "creative", "yes"):
        return MARK1 * 0.3
    else:
        return MARK5


def Q13(a):
    if a == "reading":
        return MARK3 * 0.5
    elif a == "writing" or a == "group" or a == "family" or a == "any":
        return MARK2 * 0.5
    else:
        return MARK1 * 0.5


def Q15(c):
    if c == "1hr":
        return MARK4 * 0.5
    elif c == "2hr_3hr":
        return MARK3 * 0.5
    elif c == "4hr":
        return MARK2 * 0.5
    else:
        return MARK1 * 0.5


def Q16(b):
    if b == "1hr":
        return MARK1 * 0.5
    elif b == "2hr_3hr":
        return MARK2 * 0.5
    elif b == "4hr":
        return MARK3 * 0.5
    else:
        return MARK4 * 0.5


def Q19(g):
    if g == "1":
        return MARK1 * 0.3
    else:
        return MARK3 * 0.3


def Q22(g):
    if g == "no":
        return MARK1 * 0.3
    else:
        return MARK5


def Q27(i):
    if i == "More_than_10":
        return MARK1
    elif i == "Less_than_10":
        return MARK2
    elif i == "Less_than_5":
        return MARK3
    else:
        return MARK4


def Q28(y):
    if y == "yes":
        return MARK1
    elif y == "no":
        return MARK5
    else:
        return MARK3
