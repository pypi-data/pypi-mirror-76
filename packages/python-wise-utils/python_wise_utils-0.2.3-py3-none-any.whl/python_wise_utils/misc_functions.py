from itertools import zip_longest
from pprint import pprint


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def pager(iterable, length=20):
    for i in grouper(iterable, length):
        pprint([x for x in i if x])
        if input(':'):
            break

