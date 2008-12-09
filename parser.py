"""
Inspired by 
    http://effbot.org/zone/wide-finder.htm
    http://blog.modp.com/2008/09/sorting-python-dictionary-by-value-take.html
"""

import re
from optparse import OptionParser
from operator import itemgetter

def parse(filename, cutoff=None, quantity=None):
    log_re = '"GET (.*?) HTTP/1.\d"'
    search = re.compile(log_re).search

    hist = {}
    matches = (search(line) for line in file(filename))
    uris = (x.group(1) for x in matches if x)
    
    for uri in uris:
        if uri in hist:
            hist[uri] = hist[uri] + 1
        else:
            hist[uri] = 1

    sorted_lst = sorted(hist.iteritems(), key=itemgetter(1), reverse=True)

    if cutoff:
        sorted_lst = (x for x in sorted_lst if x[1] > cutoff)
    if quantity:
        sorted_lst = sorted_lst[:quantity]

    for uri,count in sorted_lst:
        print "%s => %s" % (uri, count)

def main():
    p = OptionParser("usage: parser.py file")
    p.add_option('-c','--cutoff',dest='cutoff',
                 help="CUTOFF for minimum hits",
                 metavar="CUTOFF")
    p.add_option('-q','--quantity',dest='quantity',
                 help="QUANTITY of results to return",
                 metavar="QUANTITY")
    (options, args) = p.parse_args()
    if len(args) < 1:
        p.error("must specify a file to parse")
    cutoff = int(options.cutoff) if options.cutoff else None
    qty = int(options.quantity) if options.quantity else None
    parse(args[0], cutoff=cutoff, quantity=qty)

if __name__ == '__main__':
    main()

