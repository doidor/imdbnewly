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

Requirements
---
Paste from requirements.txt
    1. Python 2.7+
    2. Jinja2 2.7.3
    3. MarkupSafe 0.23
    4. argparse 1.2.1
    5. distribute 0.6.24
    6. imdbpie 1.4.4
    7. prettytable 0.7.2
    8. requests 2.3.0
    9. wsgiref 0.1.2