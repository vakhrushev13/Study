#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Artem"
from collections import Counter
from functools import partial
from multiprocessing import Pool, cpu_count
from optparse import OptionParser
import sys
from time import time

reload(sys)
sys.setdefaultencoding('utf-8')

def maping(block):
    return Counter([word for word in unicode(block).lower().split() if word.isalpha()])


def parse_options():
    parser = OptionParser(usage=(
        "usage: %prog [options] text or < path/to/file"))
    parser.add_option("-p", "--processes", dest="count", default=cpu_count(),
                      type=int,
                      help=("the number of processes to use (1..20)"
                            "[default %default]"))
    parser.add_option("-r", "--result", dest="result", default=0,
                      type=int,
                      help=("the number of words in result"
                            "[default all(0)]"))
    parser.add_option("-d", "--debug", dest="debug", default=False,
                      action="store_true")
    opts, args = parser.parse_args()
    if len(args) > 0:
        parser.error("%prog doesn't required args")
    if not (1 <= opts.count <= 20):
        parser.error("process count must be 1..20")
    if opts.result < 0:
        parser.error("the number of words in result must be positive")
    return opts


def main():
    opts = parse_options()
    result = Counter()
    start_time = time()
    pool = Pool(opts.count)
    read_block = partial(lambda x: sys.stdin.read(x) + sys.stdin.readline(), 8000000)
    chunks = pool.imap(maping, iter(read_block, ""))
    for chunk in chunks:
        result.update(chunk)
    pool.close()
    pool.join()
    pool.terminate()
    for word, tf in result.most_common(opts.result if opts.result else None):
        print("{0} - {1}".format(word, tf))
    if opts.debug:
        print("all time: ", time() - start_time)


if __name__ == '__main__':
    main()
