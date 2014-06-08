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


Examples
========

Get Download Statistics
-----------------------

Use the ``pypi stat`` command to get download statistics for a package.

.. code-block:: bash

    $ pypi stat marshmallow

.. code-block:: bash

    Fetching statistics for 'http://pypi.python.org/pypi/marshmallow'. . .

    Download statistics for marshmallow
    ===================================

    Downloads by version
    0.1.0   13/11/11 [ 1,677 ] **********************************
    0.2.0   13/11/12 [ 1,717 ] ***********************************
    0.2.1   13/11/12 [ 1,671 ] **********************************
    0.3.0   13/11/14 [ 1,620 ] *********************************
    0.3.1   13/11/16 [ 1,559 ] ********************************
    0.4.0   13/11/25 [ 1,508 ] *******************************
    0.4.1   13/12/02 [ 1,620 ] *********************************
    0.5.0   13/12/29 [ 1,796 ] *************************************
    0.5.1   14/02/03 [ 1,340 ] ***************************
    0.5.2   14/02/10 [ 2,441 ] *************************************************
    0.5.3   14/03/03 [ 1,634 ] *********************************
    0.5.4   14/04/18 [ 859   ] ******************
    0.5.5   14/05/03 [ 991   ] ********************
    0.6.0   14/06/04 [ 366   ] ********

    Min downloads:            366 (0.6.0)
    Max downloads:          2,441 (0.5.2)
    Avg downloads:          1,485
    Total downloads:       20,799

    Last day:              73
    Last week:          1,464
    Last month:         3,836

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

.. code-block:: bash

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


Get it now
==========
::

    $ pip install pypi-cli



Requirements
============

- Python >= 2.7 or >= 3.3

License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/pypi/blob/master/LICENSE>`_ file for more details.
