# crawler_asyncio
A web crawler made using python3.5 with asyncio.

## Running the Crawler
Make sure both pip and python correspond to a python of version >= 3.5

First, install the requirements in a `virtualenv` or globally: `pip install -r requirements.txt`.

In the project, simply run `python crawler <args> > <name_of_map>.json` where `<args>` are:

You can optionally run `pip install .` and then you can use `crawl ...`


```
Usage:
crawl (--domain=<dom> | --local --basedir=<dir>)
crawl -h | --help
crawl --version

Options:
-h --help             Show this screen.
--version             Show version.
-d --domain=<dom>     Domain of website.
-l --local            Use local or http [default: false].
-b --basedir=<dir>    Root directory of website.
```

NOTE: the domain must have the host in it (e.g. http://www.samcoope.com)

For example, `map_of_blomfield.json` contains the sitemap of www.tomblomfield.com, the result of running: `python crawler -d http://tomblomfield.com > map_of_blomfield.json`


## Tests
To run the tests, simply run `pytest test`
