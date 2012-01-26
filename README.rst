========================
Dynamic models framework
========================

This package provides a module to create dynamic models in django and use it in view and admin interface.
Thx to `Will Hardy`_ for this fantastic paper `Runtime Dynamic Models Documentation`_

.. contents::
    :local:

.. _installation:

Installation
============
Clone and install::

    git clone git://github.com/z4r/django-dynamite.git
    cd django-dynamite
    python setup.py install

Using pip::

   $ pip install django-dynamite

.. _overview:

Quick Start
===========

Take a look to ``example`` project, try it and enjoy::

    cd example
    python manage.py test
    python manage.py syncdb
    python manage.py runserver

.. _license:

License
=======

This software is licensed under the ``Apache License 2.0``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. _documentation:

Documentation
=============

You can generate your own local copy using
`Sphinx`_ trough the setup.py::

   $ python setup.py build_sphinx

Or simply click `Dynamite Documentation`_




.. _Will Hardy: http://github.com/willhardy
.. _Runtime Dynamic Models Documentation: http://2011.djangocon.eu/media/slides/RuntimeDynamicModels.pdf
.. _Sphinx: http://sphinx.pocoo.org
.. _Dynamite Documentation: http://z4r.github.com/django-dynamite/