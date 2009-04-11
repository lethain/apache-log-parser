# apache_parser.py

This is a Python script and command-line tool,
with no dependencies, that allows parsing data
from Apache log files.

At this time it supports generating supports for:

* **uri** - pageviews for each uri
* **time** - datetime with highest request/second
* **status_code** - hits for each http status code
* **referral** - uris of referring sites
* **agent** - hits for each user agent
* **subscriptions** - the number of feed subscribers per uri.
    This is done by parsing user agents for their subscriber count.

## Usage

Here are some example uses:

    python parser.py access.log subscriptions
    python parser.py access.log uri --quantity 5
    python parser.py access.log agent --cutoff 100

There is help available at the command-line as well.

    python parser.py --help


## User agents successfully parsed for feed subscribers

These are the feeds that have been tested against
the feed subscription system:

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


## Credits

This script draws inspiration and code from:

* http://effbot.org/zone/wide-finder.htm
* http://www.python.org/dev/peps/pep-0265/
