=======
piptool
=======

.. image:: https://badge.fury.io/py/piptool.png
    :target: http://badge.fury.io/py/piptool
    :alt: Latest version

.. image:: https://travis-ci.org/sloria/piptool.png?branch=master
    :target: https://travis-ci.org/sloria/piptool
    :alt: Travis-CI

Get download statistics for PyPI packages from the command line.
::

    $ piptool marshmallow
    Fetching statistics for 'marshmallow'. . .

    Download statistics for marshmallow
    ===================================
    Downloads by version
    0.1.0  13/11/11 [ 818 ] *****************************************************
    0.2.0  13/11/12 [ 855 ] ********************************************************
    0.2.1  13/11/12 [ 806 ] ****************************************************
    0.3.0  13/11/14 [ 760 ] *************************************************
    0.3.1  13/11/16 [ 695 ] *********************************************
    0.4.0  13/11/25 [ 641 ] *****************************************
    0.4.1  13/12/02 [ 695 ] *********************************************
    0.5.0  13/12/29 [ 719 ] ***********************************************
    0.5.1  14/02/03 [ 316 ] ********************

    Min downloads:            316 (0.5.1)
    Max downloads:            855 (0.2.0)
    Avg downloads:            700
    Total downloads:        6,305

Get it now
----------
::

    pip install piptool


Requirements
------------

- Python >= 2.7 or >= 3.3

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/piptool/blob/master/LICENSE>`_ file for more details.
