********
pypi-cli
********

.. image:: https://badge.fury.io/py/pypi-cli.png
    :target: http://badge.fury.io/py/pypi-cli
    :alt: Latest version

.. image:: https://travis-ci.org/sloria/pypi-cli.png?branch=master
    :target: https://travis-ci.org/sloria/pypi-cli
    :alt: Travis-CI

A command-line interface to the Python Package Index (PyPI). Get package info, download statistics, and more.

.. image:: https://dl.dropboxusercontent.com/u/1693233/github/pypi-cli.png
    :alt: Screenshot
    :target: http://konch.readthedocs.org

Get it now
==========
::

    $ pip install pypi-cli


Requirements
============

- Python >= 2.7 or >= 3.3

Examples
========

Get Package Info
----------------

Use the ``pypi info`` command to get summary information for a package.

.. code-block:: bash

    $ pypi info matplotlib

::

    matplotlib
    ==========
    Python plotting package

    Latest release:   1.3.1

    Last day:           2,015
    Last week:         16,744
    Last month:        59,989

    Author:   John D. Hunter, Michael Droettboom
    Author email: mdroe@stsci.edu

    PyPI URL:  http://pypi.python.org/pypi/matplotlib
    Home Page: http://matplotlib.org

    License: BSD


Get Download Statistics
-----------------------

Use the ``pypi stat`` command to get download statistics for a package.

.. code-block:: bash

    $ pypi stat numpy

::

    Fetching statistics for 'http://pypi.python.org/pypi/numpy'. . .

    Download statistics for numpy
    =============================

    Downloads by version
    1.0     06/12/02 [ 1,904     ] *
    1.3.0   09/04/06 [ 34,900    ] **
    1.4.1   10/04/24 [ 17,977    ] *
    1.5.0   10/09/15 [ 23,462    ] **
    1.5.1   10/11/18 [ 49,311    ] ***
    1.6.0   11/05/14 [ 39,431    ] **
    1.6.1   11/07/24 [ 168,287   ] ********
    1.6.2   12/05/20 [ 374,288   ] ******************
    1.7.0   13/02/12 [ 147,759   ] *******
    1.7.1   13/04/07 [ 1,006,008 ] **********************************************
    1.8.0   13/10/30 [ 513,208   ] ************************
    1.7.2   13/12/31 [ 2,974     ] *
    1.8.1   14/03/26 [ 356,674   ] *****************

    Min downloads:          1,904 (1.0)
    Max downloads:      1,006,008 (1.7.1)
    Avg downloads:        210,475
    Total downloads:    2,736,183

    Last day:           3,901
    Last week:         44,842
    Last month:       182,480

Browse to a Package's PyPI or homepage
--------------------------------------

Use ``pypi browse`` to open a package's PyPI url in your browser.

.. code-block:: bash

    $ pypi browse textblob

You can also go to a package's homepage.

.. code-block:: bash

    $ pypi browse textblob --homepage

Search For Packages
-------------------

Use ``pypi search`` to search for PyPI packages.

.. code-block:: bash

    $ pypi search 'requests oauth'

::

    Search results for "requests oauth"
    suds_requests
    oauth
    requests
    requests-oauthlib
    requests-foauth
    requests-oauth
    requests-oauth2
    wsgioauth
    pmr2.oauth
    django-oauth-plus


More
====

To get help or list available commands:

.. code-block:: bash

    $ pypi --help

You can also get help with subcommands:

.. code-block:: bash

    $ pypi stat --help


License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/pypi-cli/blob/master/LICENSE>`_ file for more details.
