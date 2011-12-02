Dynamic models framework
========================

This package provides a module to create dynamic models in django and use it in view and admin interface.

Thx to `Will Hardy`_ for this fantastic paper `Runtime Dynamic Models Documentation`_

Quick start
===========

Clone and install::

    git clone git://github.com/z4r/django-dynamite.git
    cd django-dynamite
    python setup.py install

Take a look to ``example`` project, try it and enjoy::

    cd example
    python manage.py test
    python manage.py syncdb
    python manage.py runserver

Building / Installing
=====================

You can just use ``setup.py`` to build and install ``django-dynamite``::

   $ python setup.py bdist_egg

Once built, you can use easy_install on the python egg.

Documentation
=============

You can generate your own local copy using
`Sphinx`_ trough the setup.py::

   $ python setup.py build_sphinx

Or simply click `Dynamite Documentation`_

.. _Will Hardy: https://github.com/willhardy
.. _Runtime Dynamic Models Documentation: http://2011.djangocon.eu/media/slides/RuntimeDynamicModels.pdf
.. _Sphinx: http://sphinx.pocoo.org
.. _Dynamite Documentation: http://z4r.github.com/django-dynamite/