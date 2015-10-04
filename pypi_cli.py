#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    pypi_cli
    ~~~~~~~~

    A command line interface to the Python Package Index.

    :copyright: (c) 2014 by Steven Loria.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import division, print_function
import re
import sys
import time
import textwrap
import math
from collections import OrderedDict
PY2 = int(sys.version[0]) == 2
if PY2:
    from xmlrpclib import ServerProxy
    from urllib import quote as urlquote
else:
    from xmlrpc.client import ServerProxy
    from urllib.parse import quote as urlquote

import requests
from dateutil.parser import parse as dateparse
import click
from click import echo, style, echo_via_pager
from click.termui import get_terminal_size

__version__ = '0.4.1'
__author__ = 'Steven Loria'
__license__ = 'MIT'

DATE_FORMAT = "%y/%m/%d"
MARGIN = 3
DEFAULT_SEARCH_RESULTS = 100

TICK = '*'
DEFAULT_PYPI = 'https://pypi.python.org/pypi'
PYPI_RE = re.compile('''^(?:(?P<pypi>https?://[^/]+/pypi)/)?
                        (?P<name>[-A-Za-z0-9_.]+)
                        (?:/(?P<version>[-A-Za-z0-9.]+))?$''', re.X)
SEARCH_URL = 'https://pypi.python.org/pypi?%3Aaction=search&term={query}'

# Number of characters added by bold formatting
_BOLD_LEN = 8
# Number of characters added by color formatting
_COLOR_LEN = 9


def echof(s, *args, **kwargs):
    echo(style(s, *args, **kwargs))


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '--version', '-v', message='%(version)s')
def cli():
    """The pypi CLI.

    \b
    Examples:
        \b
        pypi stat Django
        pypi browse Flask

    To get help with a subcommand, add the --help option after the command.

    \b
        pypi stat --help
    """
    pass


def abort_not_found(name):
    raise click.ClickException(u'No versions of "{0}" were found. Please try '
        'your search again. NOTE: Case matters.'.format(name))

def echo_header(text):
    echo(style(text, bold=True))
    echo(style('=' * len(text), bold=True))


def get_package(name_or_url, client=None):
    m = PYPI_RE.match(name_or_url)
    if not m:
        return None
    pypi_url = m.group('pypi') or DEFAULT_PYPI
    name = m.group('name')
    return Package(name, pypi_url=pypi_url, client=client)


@cli.command()
@click.option('--graph/--no-graph', '-g/-q', default=True,
    help="Output a graph of download counts.")
@click.argument('package', nargs=-1, required=True)
def stat(package, graph):
    """Print download statistics for a package.

    \b
    Example:

        pypi stat requests
    """
    client = requests.Session()
    for name_or_url in package:
        package = get_package(name_or_url, client)
        if not package:
            echo(style(
                u'Invalid name or URL: "{name}"'.format(name=name_or_url), fg='red'),
                file=sys.stderr)
            continue
        try:
            version_downloads = package.version_downloads
        except NotFoundError:
            echo(style(u'No versions found for "{0}". Skipping. . .'.format(package.name),
                fg='red'), file=sys.stderr)
            continue
        echo(u"Fetching statistics for '{url}'. . .".format(url=package.package_url))
        min_ver, min_downloads = package.min_version
        max_ver, max_downloads = package.max_version
        if min_ver is None or max_ver is None:
            raise click.ClickException('Package has no releases')
        avg_downloads = package.average_downloads
        total = package.downloads
        echo()
        header = u'Download statistics for {name}'.format(name=package.name)
        echo_header(header)
        if graph:
            echo()
            echo('Downloads by version')
            echo(package.chart())
        echo()
        echo("Min downloads:   {min_downloads:12,} ({min_ver})".format(**locals()))
        echo("Max downloads:   {max_downloads:12,} ({max_ver})".format(**locals()))
        echo("Avg downloads:   {avg_downloads:12,}".format(**locals()))
        echo("Total downloads: {total:12,}".format(**locals()))
        echo()
        echo_download_summary(package)
        echo()

def echo_download_summary(package):
    echo('Last day:    {daily:12,}'.format(daily=package.downloads_last_day))
    echo('Last week:   {weekly:12,}'.format(weekly=package.downloads_last_week))
    echo('Last month:  {monthly:12,}'.format(monthly=package.downloads_last_month))


@cli.command()
@click.option('--homepage', is_flag=True, default=False)
@click.argument('package', required=True)
def browse(package, homepage):
    """Browse to a package's PyPI or project homepage."""
    p = Package(package)
    try:
        if homepage:
            echof(u'Opening homepage for "{0}"...'.format(package), bold=True)
            url = p.home_page
        else:
            echof(u'Opening PyPI page for "{0}"...'.format(package), bold=True)
            url = p.package_url
    except NotFoundError:
        abort_not_found(package)
    click.launch(url)

def format_result(result, name_column_width=25):
    name = result['name']
    summary_wrapped = textwrap.wrap(
        result['summary'] or name,
        width=click.get_terminal_size()[0] - name_column_width - MARGIN
    )
    padding = ' ' * (name_column_width + 3)
    summary = ('\n' + padding).join(summary_wrapped)
    return u'{0} - {1}'.format(
        style(name.ljust(name_column_width), fg='cyan', bold=True),
        summary
    )

@cli.command()
@click.option('--web', '-w', is_flag=True, default=False,
    help='Open search results in your web browser.')
@click.option('--n-results', '-n', default=DEFAULT_SEARCH_RESULTS,
    help='Max number of results to show.')
@click.argument('query', required=True, type=str)
def search(query, n_results, web):
    """Search for a pypi package.

    \b
    Examples:
        \b
        pypi search requests
        pypi search 'requests oauth'
        pypi search requests -n 20
        pypi search 'requests toolbelt' --web

    """
    if web:
        echof(u'Opening search page for "{0}"...'.format(query), bold=True)
        url = SEARCH_URL.format(query=urlquote(query))
        click.launch(url)
    else:
        searcher = Searcher()
        results = searcher.search(query, n=n_results)
        first_line = style(u'Search results for "{0}"\n'.format(query), bold=True)
        echo_via_pager(
            first_line +
            '\n'.join([format_result(result) for result in results])
        )


@cli.command()
@click.option('--license/--no-license',
    is_flag=True, default=True, help='Show license.')
@click.option('--classifiers', '-c',
    is_flag=True, default=False, help='Show classifiers.')
@click.option('--long-description', '-L',
    is_flag=True, default=False, help='Show long description.')
@click.argument('package', nargs=-1, required=True)
def info(package, long_description, classifiers, license):
    """Get info about a package or packages.
    """
    client = requests.Session()
    for name_or_url in package:
        package = get_package(name_or_url, client)
        if not package:
            echo(style(
                u'Invalid name or URL: "{name}"'.format(name=name_or_url), fg='red'),
                file=sys.stderr)
            continue

        # Name and summary
        try:
            info = package.data['info']
        except NotFoundError:
            echo(style(u'No versions found for "{0}". Skipping. . .'.format(package.name),
                fg='red'), file=sys.stderr)
            continue
        echo_header(name_or_url)
        if package.summary:
            echo(package.summary)

        # Version info
        echo()
        echo('Latest release:   {version:12}'.format(version=info['version']))

        # Long description
        if long_description:
            echo()
            echo(package.description)

        # Download info
        echo()
        echo_download_summary(package)

        # Author info
        echo()
        author, author_email = package.author, package.author_email
        if author:
            echo(u'Author:   {author:12}'.format(**locals()))
        if author_email:
            echo(u'Author email: {author_email:12}'.format(**locals()))

        # Maintainer info
        maintainer, maintainer_email = package.maintainer, package.maintainer_email
        if maintainer or maintainer_email:
            echo()
        if maintainer:
            echo(u'Maintainer:   {maintainer:12}'.format(**locals()))
        if maintainer_email:
            echo(u'Maintainer email: {maintainer_email:12}'.format(**locals()))

        # URLS
        echo()
        echo(u'PyPI URL:  {pypi_url:12}'.format(pypi_url=package.package_url))
        if package.home_page:
            echo(u'Home Page: {home_page:12}'.format(home_page=package.home_page))
        if package.docs_url:
            echo(u'Documentation: {docs_url:12}'.format(docs_url=package.docs_url))


        # Classifiers
        if classifiers:
            echo()
            echo(u'Classifiers: ')
            for each in info.get('classifiers', []):
                echo('\t' + each)

        if license and package.license:
            echo()
            echo(u'License: ', nl=False)
            # license may be just a name, e.g. 'BSD' or the full license text
            # If a new line is found in the text, print a new line
            if package.license.find('\n') >= 0 or len(package.license) > 80:
                echo()
            echo(package.license)
        echo()


# Utilities
# #########

def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated."""
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property

def _style_value(value):
    return style('{:,}'.format(value), fg='yellow')

def bargraph(data, max_key_width=30):
    """Return a bar graph as a string, given a dictionary of data."""
    lines = []
    max_length = min(max(len(key) for key in data.keys()), max_key_width)
    max_val = max(data.values())
    max_val_length = max(
        len(_style_value(val))
        for val in data.values())
    term_width = get_terminal_size()[0]
    max_bar_width = term_width - MARGIN - (max_length + 3 + max_val_length + 3)
    template = u"{key:{key_width}} [ {value:{val_width}} ] {bar}"
    for key, value in data.items():
        try:
            bar = int(math.ceil(max_bar_width * value / max_val)) * TICK
        except ZeroDivisionError:
            bar = ''
        line = template.format(
            key=key[:max_length],
            value=_style_value(value),
            bar=bar,
            key_width=max_length,
            val_width=max_val_length
        )
        lines.append(line)
    return '\n'.join(lines)


class PackageError(Exception):
    pass


class NotFoundError(PackageError):
    pass


# API Wrapper
# ###########

class Package(object):

    def __init__(self, name, client=None, pypi_url=DEFAULT_PYPI):
        self.client = client or requests.Session()
        self.name = name
        self.url = '{pypi_url}/{name}/json'.format(pypi_url=pypi_url, name=name)

    @lazy_property
    def data(self):
        resp = self.client.get(self.url)
        if resp.status_code == 404:
            raise NotFoundError('Package not found')
        return resp.json()

    @lazy_property
    def versions(self):
        """Return a list of versions, sorted by release datae."""
        return [k for k, v in self.release_info]

    @lazy_property
    def version_downloads(self):
        """Return a dictionary of version:download_count pairs."""
        ret = OrderedDict()
        for release, info in self.release_info:
            download_count = sum(file_['downloads'] for file_ in info)
            ret[release] = download_count
        return ret

    @property
    def release_info(self):
        release_info = self.data['releases']
        # filter out any versions that have no releases
        filtered = [(ver, releases) for ver, releases in release_info.items()
                    if len(releases) > 0]
        # sort by first upload date of each release
        return sorted(filtered, key=lambda x: x[1][0]['upload_time'])

    @lazy_property
    def version_dates(self):
        ret = OrderedDict()
        for release, info in self.release_info:
            if info:
                upload_time = dateparse(info[0]['upload_time'])
                ret[release] = upload_time
        return ret

    def chart(self):
        def style_version(version):
            return style(version, fg='cyan', bold=True)

        data = OrderedDict()
        for version, dl_count in self.version_downloads.items():
            date = self.version_dates.get(version)
            date_formatted = ''
            if date:
                date_formatted = time.strftime(DATE_FORMAT,
                    self.version_dates[version].timetuple())
            key = "{0:20} {1}".format(
                style_version(version),
                date_formatted
            )
            data[key] = dl_count
        return bargraph(data, max_key_width=20 + _COLOR_LEN + _BOLD_LEN)

    @lazy_property
    def downloads(self):
        """Total download count.

        :return: A tuple of the form (version, n_downloads)
        """
        return sum(self.version_downloads.values())

    @lazy_property
    def max_version(self):
        """Version with the most downloads.

        :return: A tuple of the form (version, n_downloads)
        """
        data = self.version_downloads
        if not data:
            return None, 0
        return max(data.items(), key=lambda item: item[1])

    @lazy_property
    def min_version(self):
        """Version with the fewest downloads."""
        data = self.version_downloads
        if not data:
            return (None, 0)
        return min(data.items(), key=lambda item: item[1])

    @lazy_property
    def average_downloads(self):
        """Average number of downloads."""
        return int(self.downloads / len(self.versions))

    @property
    def author(self):
        return self.data['info'].get('author')

    @property
    def description(self):
        return self.data['info'].get('description')

    @property
    def summary(self):
        return self.data['info'].get('summary')

    @property
    def author_email(self):
        return self.data['info'].get('author_email')

    @property
    def maintainer(self):
        return self.data['info'].get('maintainer')

    @property
    def maintainer_email(self):
        return self.data['info'].get('maintainer_email')

    @property
    def license(self):
        return self.data['info'].get('license')

    @property
    def downloads_last_day(self):
        return self.data['info']['downloads']['last_day']

    @property
    def downloads_last_week(self):
        return self.data['info']['downloads']['last_week']

    @property
    def downloads_last_month(self):
        return self.data['info']['downloads']['last_month']

    @property
    def package_url(self):
        return self.data['info']['package_url']

    @property
    def home_page(self):
        return self.data['info'].get('home_page')

    @property
    def docs_url(self):
        return self.data['info'].get('docs_url')

    def __repr__(self):
        return '<Package(name={0!r})>'.format(self.name)


class Searcher(object):
    """PyPI package search wrapper that uses the PyPI's XMLRPC API.

    Search algorithm adapted from Supreet Sethi's implementation (MIT Licensed).
    https://github.com/djinn/pypi-json/blob/master/LICENSE.md
    """

    STOP_WORDS = set([
        "a", "and", "are", "as", "at", "be", "but", "by",
        "for", "if", "in", "into", "is", "it",
        "no", "not", "of", "on", "or", "such",
        "that", "the", "their", "then", "there", "these",
        "they", "this", "to", "was", "will",
    ])

    NAME_MATCH_WEIGHT = 16
    CONTAINS_NAME_MULT = 4
    NAME_IN_SUMMARY_MULT = 2

    def __init__(self, pypi_url=DEFAULT_PYPI, client=None):
        self.pypi_url = pypi_url
        self.client = client or ServerProxy(pypi_url)

    def score(self, tokens, record):
        score = 0
        name, summary = record['name'].lower(), record['summary']
        for token in tokens:
            qtf = 0
            if token == name:
                qtf += self.NAME_MATCH_WEIGHT
            else:
                n_name_matches = len(re.compile(token).findall(name))
                qtf += self.CONTAINS_NAME_MULT * n_name_matches
            if record['summary'] is not None:
                summary_matches = re.compile(token).findall(summary.lower())
                qtf += 2 * len(summary_matches)
            score += qtf
        return score

    def search(self, query, n=None):
        tokens = [each.strip() for each in query.strip().lower().split()
                  if each not in self.STOP_WORDS]
        results = self.client.search({'name': tokens}, 'and')
        visited = []
        nd = []
        for result in results:
            name = result['name']
            try:
                visited.index(name)
            except ValueError:
                nd.append(result)
                visited.append(name)
        ranked = [(self.score(tokens, result), result) for result in nd]
        sorted_results = sorted(ranked, reverse=True, key=lambda t: t[0])
        limited_results = sorted_results[:n] if n else sorted_results
        return (result for score, result in limited_results)
