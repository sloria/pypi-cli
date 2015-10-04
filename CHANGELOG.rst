*********
Changelog
*********

0.4.1 (2015-10-04)
==================

- Use explicit u'' prefix rather than importing unicode_literals from __future__ to avoid warnings from click on Py2.
- Tested on Python 3.5.

0.4.0 (2014-12-22)
==================

- Don't pin to python-dateutil==2.2.
- Echo search results in pager.

0.3.2 (2014-09-09)
==================

- Use HTTPS urls. Thanks Alex Gaynor.
- Fix error in search when a package's summary is ``None``. Thanks Eric Lo.

0.3.1 (2014-06-18)
==================

- Disable pager for displaying search results until click has better support for ANSI styles in the pager. Thanks Arne Neumann for reporting.
- Support newer versions of click. Thanks Juraj Bubniak for reporting.

0.3.0 (2014-06-15)
==================

- Fix bug that caused search to raise a `TypeError` on Python 3. Thanks @barrio for reporting.
- Search command shows package summaries.
- Search command shows all results in the pager.


0.2.1 (2014-06-12)
==================

- Fix bug that caused a crash in search. Thanks Christian Pedersen for reporting.


0.2.0 (2014-06-09)
==================

- Add ``--web`` option to `search` command.
- Fix bug with locating packages with an underscore character.
- Add license, maintainer, and documentation info to the ``info`` command.


0.1.0 (2014-06-08)
==================

- First release.
- Supports ``stat``, ``browse``, and ``search``, and ``info`` commands.
