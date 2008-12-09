"""
Inspired by 
    http://effbot.org/zone/wide-finder.htm
    http://blog.modp.com/2008/09/sorting-python-dictionary-by-value-take.html
"""

import re
from optparse import OptionParser
from operator import itemgetter

"""
"GET /feeds/series/two-faced-django/ HTTP/1.0" 200 720 "-" "Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; 6 subscribers; feed-id=9590656098396809912)"

"NewsGatorOnline/2.0 (http://www.newsgator.com; 39 subscribers)"
"Netvibes (http://www.netvibes.com/; 5 subscribers; feedId: 5404723)"

127.0.0.1 - - [02/Dec/2008:09:11:06 -0600] "GET /feeds/flow/code/ HTTP/1.0" 200 66736 "-" "CFNetwork/129.22"
"""

def restrict(lst, cutoff, count):
    'Restrict the list by minimum value or count.'
    if cutoff:
        lst = (x for x in lst if x[1] > cutoff)
    if count:
        lst = lst[:count]
    return lst

def parse(filename):
    'Return tuple of dictionaries containing file data.'
    def make_entry(x):
        return { 
            'uri':x.group('uri'),
            'time':x.group('time'),
            }
    # log_re = '"GET (?P<uri>.*?) HTTP/1.\d"'   HTTP/1.0" 200 66736 "-" "CFNetwork/129.22"'
    log_re = '(?P<ip>[.\d]+) - - \[(?P<time>.*?)\] "GET (?P<uri>.*?)"'
    search = re.compile(log_re).search
    matches = (search(line) for line in file(filename))
    return (make_entry(x) for x in matches if x)

def count_value(lst, key):
    d = {}
    for obj in lst:
        val = obj[key]
        if val in d:
            d[val] = d[val] + 1
        else:
            d[val] = 1
    return d.iteritems()

def print_results(lst):
    for item in lst:
        print "%s => %s" % (item[0], item[1])


def generic_report_for_key(key, filename, cutoff, quantity):
    entries = parse(filename)
    lst = count_value(entries, key)
    lst = sorted(lst, key=itemgetter(1), reverse=True)
    lst =  restrict(lst, cutoff, quantity)
    print_results(lst)

def main():
    p = OptionParser("usage: parser.py file uri|time|subscribers")
    p.add_option('-c','--cutoff',dest='cutoff',
                 help="CUTOFF for minimum hits",
                 metavar="CUTOFF")
    p.add_option('-q','--quantity',dest='quantity',
                 help="QUANTITY of results to return",
                 metavar="QUANTITY")
    (options, args) = p.parse_args()
    if len(args) < 1:
        p.error("must specify a file to parse")
    if len(args) < 2:
        p.error("must specify report type to generate")


    filename = args[0]
    report_type = args[1]
    cutoff = int(options.cutoff) if options.cutoff else None
    qty = int(options.quantity) if options.quantity else None
    
    if report_type == 'subscribers':
        subscribers(filename, cutoff=cutoff, quantity=qty)
    elif report_type in ['uri','time']:
        generic_report_for_key(report_type, filename, cutoff, qty)
    else:
        p.error("specified an invalid report type")

if __name__ == '__main__':
    main()

