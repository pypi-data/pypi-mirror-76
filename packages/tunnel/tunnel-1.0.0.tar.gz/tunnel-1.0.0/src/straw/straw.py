def streamify(l):
    return grammify(l)


def grammify(l):
    for elem in l:
        yield elem
