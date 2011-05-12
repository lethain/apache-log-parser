import re, operator
from optparse import OptionParser
from operator import itemgetter

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
            'referral':x.group('referral'),
            'agent':x.group('agent'),
            }
    log_re = '(?P<ip>[.:0-9a-fA-F]+) - - \[(?P<time>.*?)\] "GET (?P<uri>.*?) HTTP/1.\d" (?P<status_code>\d+) \d+ "(?P<referral>.*?)" "(?P<agent>.*?)"'
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

    feed_re = '(?P<name>.*?) \(.*?; (?P<count>\d+) subscribers?(; .*?)?\)'
    feed_re2 = '(?P<name>.*?);? (?P<count>\d+) (S|s)ubscribers?'
    search = re.compile(feed_re).search
    search2 = re.compile(feed_re2).search

    # remove duplicate subscriptions to avoid
    # double counting
    results = []
    for key, readers in feeds.iteritems():
        sources = {}
        for reader in readers:
            m = search(reader)
            if not m:
                m = search2(reader)
            if m:
                name = m.group('name')
                count = int(m.group('count'))
                if name in sources:
                    if sources[name] < count:
                        sources[name] = count
                else:
                    sources[name] = count
        
        # sum subscription totals
        vals = ( val for key,val in sources.iteritems())
        sum = reduce(operator.add, vals, 0)

        # there can be false positives with weird user agents,
        # but they won't have any subscribers listed, so we
        # filter them out here
        if sum > 0:
            results.append((key, sum))

    results = sorted(results, key=itemgetter(1), reverse=True)
    results = restrict(results, cutoff, quantity)
    print_results(results)
    
def main():
    p = OptionParser("usage: parser.py file uri|time|status_code|agent|referral|subscriptions")
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
    elif report_type in ['uri','time','status_code','agent','referral']:
        generic_report_for_key(report_type, filename, cutoff, qty)
    else:
        p.error("specified an invalid report type")

if __name__ == '__main__':
    main()
