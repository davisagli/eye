Overview
========

Eye provides a browser-based UI to browse the contents of a ZODB database.

It can also be used as a generic Python object browser.

Installation
============

At this point Eye has been tested on Python 2.6.

Eye has a few dependencies including the Pyramid web framework. Therefore it's
recommended to install it in a virtualenv or buildout to keep it isolated from
other software on your system.

Assuming you have virtualenv installed, the following commands will install Eye::

  $ virtualenv --no-site-packages eye
  $ cd eye
  $ bin/pip install eye

This creates a new virtualenv in the ``eye`` directory, and installs the ``eye``
console script into the ``bin`` subdirectory.

Basic usage
-----------

Inspect a ZODB filestorage
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ bin/eye [path to Data.fs]

Then open your browser to http://localhost:8080/

.. image:: https://github.com/davisagli/eye/raw/master/screenshot.png

Inspect an arbitrary object
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  >>> from datetime import datetime
  >>> foo = datetime.now()
  >>> import eye; eye.eye(foo)


Similar tools
=============

* `zope2.zodbbrowser`_: Runs in Zope 2; provides a bit more app-specific info.
* `zodbbrowser`_: Based on the Zope 3.4.0 KGS; displays historical object revisions.
* `z3c.zodbbrowser`_: An apparently unfinished GSOC project; based on wxPython.

.. _`zope2.zodbbrowser`: http://code.google.com/p/zodbbrowser/
.. _`zodbbrowser`: http://pypi.python.org/pypi/zodbbrowser
.. _`z3c.zodbbrowser`: http://svn.zope.org/z3c.zodbbrowser/trunk

Credits
=======

Thanks to:

* Roberto Allende and menttes. The initial inspiration and code is from their zope2.zodbbrowser.
* Elizabeth Leddy
* Jim Fulton for creating the ZODB.
* The creators of the Pyramid web framework.
* The creators of the JQuery, JQuery UI, and Dynatree libraries.