===========
EEA Aliases
===========
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=Eionet/eea.aliases/develop
  :target: https://ci.eionet.europa.eu/job/Eionet/job/eea.aliases/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=Eionet/eea.aliases/master
  :target: https://ci.eionet.europa.eu/job/Eionet/job/eea.aliases/job/master/display/redirect
  :alt: Master
.. image:: https://img.shields.io/github/v/release/eea/eea.aliases
  :target: https://eggrepo.eea.europa.eu/d/eea.aliases/
  :alt: Release
  
Introduction
============

Add fallback aliases for common missing modules while migrating to Plone 5.2 (Python 3)

See https://community.plone.org/t/zodbverify-porting-plone-with-zopedb-to-python3/8806/13


Contents
========

.. contents::


Install
=======

* Add eea.aliases to your eggs and zcml section in your buildout and re-run buildout::

    [buildout]
    parts +=
      zodbupdate

    eggs +=
      eea.aliases
      zodbverify

    [zodbupdate]
    recipe = zc.recipe.egg
    eggs =
      zodbupdate
      ${buildout:eggs}


Usage
=====

  ::

    $ bin/instance zodbverify
    $ bin/zodbupdate --convert-py3 --file=/data/filestorage/Data.fs --encoding utf8 --encoding-fallback latin1


Source code
===========

Latest source code (Zope 2 compatible):

* `EEA on Github <https://github.com/eea/eea.aliases>`_


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The eea.aliases (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Funding and project management
==============================

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
