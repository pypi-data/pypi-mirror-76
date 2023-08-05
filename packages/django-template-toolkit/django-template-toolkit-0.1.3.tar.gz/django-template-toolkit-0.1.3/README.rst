django-template-toolkit
=======================

.. image:: https://travis-ci.org/ghdpro/django-template-toolkit.svg?branch=master
    :target: https://travis-ci.org/ghdpro/django-template-toolkit
    :alt: Build Status

.. image:: https://codecov.io/gh/ghdpro/django-template-toolkit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ghdpro/django-template-toolkit
    :alt: Test Coverage

.. image:: https://api.codeclimate.com/v1/badges/ffe49f0be8becc46d6d6/maintainability
   :target: https://codeclimate.com/github/ghdpro/django-template-toolkit/maintainability
   :alt: Maintainability

This project is a collection of useful templates & tags for the Django web framework.
I made this mainly for my own projects where I noticed I was copying the same set of
templates and template tags & filters over to each new project, but hopefully it will
be useful for other people as well.

Django >= 2.2 and Python >= 3.6 are supported.

Documentation and examples will follow in the future. For now, to use this package in your
Django project install it with :code:`pip` then add it to your :code:`INSTALLED_APPS` list
in settings. You can then include the templates as :code:`{% include 'toolkit/forms/field.html' %}` (for example)
and the template tags with :code:`{% load toolkit %}`. For now see the source code for which
template tags & filters are available.
