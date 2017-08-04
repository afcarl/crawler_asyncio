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
from datetime import datetime

from .finders import InternalLinkFinder, StaticAssetsFinder, ScriptFinder
from .getters import FileGetter, WebGetter
from .keywords import SALESFORCE_KEYWORDS, ZENDESK_KEYWORDS
from .keyword_search import findall


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

    sitemap, findings = loop.run_until_complete(crawl(domain, local_dir, use_local))

    logging.info('DONE')
    # print(json.dumps(sitemap, sort_keys=True, indent=4))
    print(json.dumps(findings, sort_keys=True, indent=4))


async def crawl(domain, local_dir, use_local=False, max_time_secs=30):
    if use_local:
        getter = FileGetter(basedir=local_dir)
    else:
        getter = WebGetter(domain=domain)

    seen_paths = {'', '/'}
    site_map = {}

    link_finder = InternalLinkFinder(domain)
    sa_finder = StaticAssetsFinder()
    script_finder = ScriptFinder()

    def get_links(parsed_html):
        nonlocal link_finder
        return link_finder.find_all(parsed_html)

    def get_static_assets(parsed_html):
        nonlocal sa_finder
        return sa_finder.find_all(parsed_html)

    def get_scripts(parsed_html):
        nonlocal script_finder
        return script_finder.find_all(parsed_html)

    findings = {
        'zendesk': {},
        'salesforce': {}
    }

    site_map, findings = await crawl_recursive(
        getter, '', seen_paths, findings, get_links, get_static_assets, get_scripts,
        start_time=datetime.now(),
        timeout_secs=max_time_secs
    )

    return site_map, findings


async def crawl_recursive(
    getter,
    path,
    seen_paths,
    findings,
    get_links,
    get_static_assets,
    get_scripts,
    start_time,
    timeout_secs
):
    """
    TODO: update this with findings
    returns {
        <path>: {
            links: [<url>...],
            assets: [<url>...]
        },
        ...
    }
    """

    # HACK: along with all of the try/catches
    if (datetime.now() - start_time).seconds > timeout_secs:
        # TODO: find a nice way of notifying why something stopped
        return {}, findings

    try:
        logging.info('Getting: {}'.format(path))
        page_html = await getter.get(path)
        logging.info('Got {}'.format(path))
    except Exception as e:
        logging.info('Unable to get path {}. {}'.format(path, str(e)))
        return {path: 'ERROR GETTING PAGE {}'.format(str(e))}, findings

    parsed_html = BeautifulSoup(page_html, 'html.parser')

    scripts_html = []
    try:
        scripts = get_scripts(parsed_html)

        if len(scripts) > 0:
            scripts_html_futures, _ = await asyncio.wait([
                getter.get(script_uri) for script_uri in scripts
            ])

            for x in scripts_html_futures:
                if not x.exception():
                    scripts_html += [x.result()]
                else:
                    x.cancel()
    except Exception as e:
        pass

    all_page_html = '\n'.join([page_html] + scripts_html).lower()

    zendesk_findings = find_keywords(ZENDESK_KEYWORDS, all_page_html)
    if len(zendesk_findings) > 0:
        findings['zendesk'][path] = zendesk_findings

    salesforce_findings = find_keywords(SALESFORCE_KEYWORDS, all_page_html)
    if len(salesforce_findings) > 0:
        findings['salesforce'][path] = salesforce_findings

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

    if len(unseen_paths) != 0:
        seen_paths.update(unseen_paths)
        # crawl the unseen ones
        other_maps_futures, _ = await asyncio.wait([
            crawl_recursive(
                getter, new_path, seen_paths, findings, get_links, get_static_assets, get_scripts,
                start_time=start_time, timeout_secs=timeout_secs
            )
            for new_path in unseen_paths
        ])

        other_maps = [x.result()[0] for x in other_maps_futures]

        for path_map in other_maps:
            this_path_map.update(path_map)

    return (this_path_map, findings)


def resolve_link_path(path, link):
    if link.startswith('..'):
        # remove the last value in the path so normpath works properly
        path = '/'.join(path.split('/')[:-1])
        return normpath(join_path(path, link.strip('/')))
    else:
        return link.strip('/')


def find_keywords(keywords, text):
    assert all(type(k) == str for k in keywords)
    assert type(text) == str
    findings = []

    for keyword in keywords:
        keyword_locations = [index for index in findall(keyword, text)]
        for location in keyword_locations:
            findings += [{
                'keyword': keyword,
                'message': 'found keyword {} in source:\n`{}`'.format(
                    keyword,
                    text[location - 100: location + 100]
                )
            }]
    return findings
