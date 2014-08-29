IMDbNewly
=========

IMDbNewly is a simple python script which fetches the newly added movies into IMDb's top 250 list.

Usage
---

Paste from ```python imdbnewly.py -h```
```
usage: imdbnewly.py [-h] [-f] [-a] [-ht] [-b]

Find the newly added movies to imdb's top 250.

optional arguments:
  -h, --help   show this help message and exit
  -f, --fetch  fetch imdb's current top 250 list
  -a, --ascii  print the newly added items in ascii format
  -ht, --html  print the newly added items in html format
  -b, --both   print both the ascii and the html formats
```

I run this as a cronjob, like this:
```
# re-fetch the top 250 list every 3 months
1 0 1 */3 * /usr/bin/python imdbnewly.py -f >/dev/null 2>&1
# generate the newly added movies list every day at 1 am
1 0 * * * /usr/bin/python imdbnewly.py -b >/dev/null 2>&1
```

Requirements
---

Paste from requirements.txt

1. Python 2.7+
1. Jinja2 2.7.3
1. MarkupSafe 0.23
1. argparse 1.2.1
1. distribute 0.6.24
1. imdbpie 1.4.4
1. prettytable 0.7.2
1. requests 2.3.0
1. wsgiref 0.1.2