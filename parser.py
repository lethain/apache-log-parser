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
            'server_ip':x.group('ip'),
            'uri':x.group('uri'),
            'time':x.group('time'),
            'status_code':x.group('status_code'),
            'agent':x.group('agent'),
            }
    log_re = '(?P<ip>[.\d]+) - - \[(?P<time>.*?)\] "GET (?P<uri>.*?) HTTP/1.\d" (?P<status_code>\d+) \d+ ".*?" "(?P<agent>.*?)"'
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
        print "%50s %10s" % (item[0], item[1])


def generic_report_for_key(key, filename, cutoff, quantity):
    'Handles creating generic reports.'
    entries = parse(filename)
    lst = count_value(entries, key)
    lst = sorted(lst, key=itemgetter(1), reverse=True)
    lst =  restrict(lst, cutoff, quantity)
    print_results(lst)

def subscriptions(filename, cutoff, quantity):
    'Creates a custom report for determining number of subscribers per feed.'
    entries = parse(filename)
    entries = (x for x in entries if 'ubscriber' in x['agent'])

    feeds = {}
    for obj in entries:
        uri = obj['uri']
        agent = obj['agent']
        if uri in feeds:
            feeds[uri].append(agent)
        else:
            feeds[uri] = [agent]

    """
Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; 3 subscribers; feed-id=7675226481817637975)
Netvibes (http://www.netvibes.com/; 5 subscribers; feedId: 5404723)


Bloglines/3.1 (http://www.bloglines.com; 1 subscriber)
NewsGatorOnline/2.0 (http://www.newsgator.com; 1 subscribers)
Zhuaxia.com 1 Subscribers
AideRSS/1.0 (aiderss.com); 2 subscribers
xianguo-rssbot/0.1 (http://www.xianguo.com/; 1 subscribers)
Fastladder FeedFetcher/0.01 (http://fastladder.com/; 1 subscriber)
HanRSS/1.1 (http://www.hanrss.com; 1 subscriber)
livedoor FeedFetcher/0.01 (http://reader.livedoor.com/; 1 subscriber)
    """


    feed_re = '(?P<name>.*?) \(.*?; (?P<count>\d+) subscribers?(; .*?)?\)'
    search = re.compile(feed_re).search
    for key, readers in feeds.iteritems():
        sources = {}
        for reader in readers:
            m = search(reader)
            if not m:
                print "did not match: %s" % reader
            else:
                pass
                #print "match: %s %s" % (m.group('name'), m.group('count'))
            #print reader


    #print feeds['/']
    #lst = restrict(lst, cutoff, quantity)
    #print_results(lst)
    

def main():
    p = OptionParser("usage: parser.py file uri|time|status_code|agent|subscriptions")
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
    
    if report_type == 'subscriptions':
        subscriptions(filename, cutoff=cutoff, quantity=qty)
    elif report_type in ['uri','time','status_code','agent']:
        generic_report_for_key(report_type, filename, cutoff, qty)
    else:
        p.error("specified an invalid report type")

if __name__ == '__main__':
    main()

