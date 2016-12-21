"""
crawl.

Usage:
crawl (--domain=<dom> | --local --basedir=<dir>)
crawl -h | --help
crawl --version

Options:
-h --help             Show this screen.
--version             Show version.
-d --domain=<dom>     Domain of website.
-l --local            Use local or http [default: false].
-b --basedir=<dir>    Root directory of website
"""
from docopt import docopt
import logging
import asyncio
from os.path import normpath, join as join_path
import json
from bs4 import BeautifulSoup

from .finders import InternalLinkFinder, StaticAssetsFinder
from .getters import FileGetter, WebGetter


def main():
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )

    arguments = docopt(__doc__, version='0.0.1')
    domain = arguments.get('--domain')
    local_dir = arguments.get('--basedir')

    loop = asyncio.get_event_loop()
    use_local = arguments.get('--local')

    sitemap = loop.run_until_complete(crawl(domain, local_dir, use_local))

    logging.info('DONE')
    print(json.dumps(sitemap, sort_keys=True, indent=4))


async def crawl(domain, local_dir, use_local):
    if use_local:
        getter = FileGetter(basedir=local_dir)
    else:
        getter = WebGetter(domain=domain)

    seen_paths = {'', '/'}
    site_map = {}

    link_finder = InternalLinkFinder(domain)
    sa_finder = StaticAssetsFinder()

    def get_links(parsed_html):
        nonlocal link_finder
        return link_finder.find_all(parsed_html)

    def get_static_assets(parsed_html):
        nonlocal sa_finder
        return sa_finder.find_all(parsed_html)

    site_map = await crawl_recursive(getter, '', seen_paths, get_links, get_static_assets)

    return site_map


async def crawl_recursive(getter, path, seen_paths, get_links, get_static_assets):
    """
    returns {
        <path>: {
            links: [<url>...],
            assets: [<url>...]
        },
        ...
    }
    """
    try:
        logging.info('Getting: {}'.format(path))
        page_html = await getter.get(path)
        logging.info('Got {}'.format(path))
    except Exception as e:
        logging.warning('Unable to get path {}. {}'.format(path, str(e)))
        return {path: 'ERROR GETTING PAGE {}'.format(str(e))}

    parsed_html = BeautifulSoup(page_html, 'html.parser')

    links = get_links(parsed_html)
    # resolve relative links using the original path
    links = {resolve_link_path(path, link) for link in links}

    unseen_paths = links - seen_paths

    assets = get_static_assets(parsed_html)
    # leave asset paths relative, this could be done later if needed

    this_path_map = {
        path: {
            'links': sorted(list(links)),
            'assets': sorted(list(assets))
        }
    }

    if unseen_paths:

        seen_paths.update(unseen_paths)
        # crawl the unseen ones
        other_maps_futures, _ = await asyncio.wait([
            crawl_recursive(getter, new_path, seen_paths, get_links, get_static_assets)
            for new_path in unseen_paths
        ])

        other_maps = [x.result() for x in other_maps_futures]

        for path_map in other_maps:
            this_path_map.update(path_map)

    return this_path_map


def resolve_link_path(path, link):
    if link.startswith('..'):
        # remove the last value in the path so normpath works properly
        path = '/'.join(path.split('/')[:-1])
        return normpath(join_path(path, link.strip('/')))
    else:
        return link.strip('/')
