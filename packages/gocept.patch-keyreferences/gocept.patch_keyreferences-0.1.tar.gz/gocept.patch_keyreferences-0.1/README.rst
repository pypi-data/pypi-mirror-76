============================
gocept.patch_keyreferences
============================

This package fixes the comparison between keyreferences of
``zope.keyreference`` in Python 3.

Reasoning
=========

In Python 2 ``zope.keyreference`` used to compare items via the ``__cmp__``
method. This was facilitated by the C-implementation of the Zope security
packages, as it allowed the comparison without un-wrapping the security proxy
explicitly. Python 3 used rich comparison and this behaviour stopped working.
For further information see the following `PR`_.

.. _PR: https://github.com/zopefoundation/zope.keyreference/pull/6

This package applies a monkey patch to make the fix usable although it is the
wrong place to fix it in general.

Usage
=====

To use this package include it in the zcml of you application::

    <configure xmlns="http://namespaces.zope.org/zope">

        <include package="gocept.patch_keyreferences" />

    </configure>
