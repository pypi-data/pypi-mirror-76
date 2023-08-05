Regression test
===============

.. Caution::

    This was copied from ``zope.app.catalog`` as it reproduces the behaviour
    which is fixed by this package.



Catalogs are simple tools used to supppot searching.  A catalog
manages a collection of indexes, and aranges for objects to indexed
with it's contained indexes.

TODO: Filters
      Catalogs should provide the option to filter the objects the
      catalog. This would facilitate the use of separate catalogs for
      separate purposes.  It should be possible to specify a a
      collection of types (interfaces) to be cataloged and a filtering
      expression.  Perhaps another option would be to be the ability
      to specify a names filter adapter.

Catalogs use a unique-id tool to assign short (integer) ids to
objects.  Before creating a catalog, you must create a intid tool:

  >>> print(http(r"""
  ... POST /++etc++site/default/@@+/action.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Length: 78
  ... Content-Type: application/x-www-form-urlencoded
  ... Referer: http://localhost:8081/++etc++site/default/@@+
  ...
  ... type_name=BrowserAdd__zope.intid.IntIds&id=&add=+Add+""",
  ... handle_errors=False))
  HTTP/1.1 303 ...

And register it:

  >>> print(http(r"""
  ... POST /++etc++site/default/IntIds/addRegistration.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Referer: http://localhost:8081/++etc++site/default/IntIds/
  ... Content-Type: multipart/form-data; boundary=----------CedQTrEQIEPbgfYhvcITAhQi2aJdgu3tYfJ0WYQmkpLQTt6OTOpd5GJ
  ...
  ... ------------CedQTrEQIEPbgfYhvcITAhQi2aJdgu3tYfJ0WYQmkpLQTt6OTOpd5GJ
  ... Content-Disposition: form-data; name="field.name"
  ...
  ...
  ... ------------CedQTrEQIEPbgfYhvcITAhQi2aJdgu3tYfJ0WYQmkpLQTt6OTOpd5GJ
  ... Content-Disposition: form-data; name="field.provided"
  ...
  ... zope.intid.interfaces.IIntIds
  ... ------------CedQTrEQIEPbgfYhvcITAhQi2aJdgu3tYfJ0WYQmkpLQTt6OTOpd5GJ
  ... Content-Disposition: form-data; name="field.provided-empty-marker"
  ...
  ... 1
  ... ------------CedQTrEQIEPbgfYhvcITAhQi2aJdgu3tYfJ0WYQmkpLQTt6OTOpd5GJ
  ... Content-Disposition: form-data; name="field.comment"
  ...
  ...
  ... ------------CedQTrEQIEPbgfYhvcITAhQi2aJdgu3tYfJ0WYQmkpLQTt6OTOpd5GJ
  ... Content-Disposition: form-data; name="field.actions.register"
  ...
  ... Register
  ... ------------CedQTrEQIEPbgfYhvcITAhQi2aJdgu3tYfJ0WYQmkpLQTt6OTOpd5GJ--
  ... """, handle_errors=False))
  HTTP/1.1 303 ...
  ...


Moving short-id management outside of catalogs make it possible to
join searches accross multiple catalogs and indexing tools
(e.g. relationship indexes).

TODO: Filters?
      Maybe unique-id tools should be filtered as well, however, this
      would limit the value of unique id tools for providing
      cross-catalog/cross-index merging.  At least the domain for a
      unique id tool would be broader than the domain of a catalog.
      The value of filtering in the unique id tool is that it limits
      the amount of work that needs to be done by catalogs.
      One obvious aplication is to provide separate domains for
      ordinary and meta content. If we did this, then we'd need to be
      able to select, and, perhaps, alter, the unique-id tool used by
      a catalog.

Once we have a unique-id tool, you can add a catalog:

  >>> print(http(r"""
  ... POST /++etc++site/default/@@+/action.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Length: 77
  ... Content-Type: application/x-www-form-urlencoded
  ... Referer: http://localhost:8081/++etc++site/default/@@+
  ...
  ... type_name=BrowserAdd__zope.catalog.catalog.Catalog&id=&add=+Add+"""))
  HTTP/1.1 303 ...

and register it:

  >>> print(http(r"""
  ... POST /++etc++site/default/Catalog/addRegistration.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Referer: http://localhost:8081/++etc++site/default/Catalog/
  ... Content-Type: multipart/form-data; boundary=----------61t9UJyoacebBevQVdNrlvXP6T9Ik3Xo4RyXkwJJWvuhao65RTuAPRa
  ...
  ... ------------61t9UJyoacebBevQVdNrlvXP6T9Ik3Xo4RyXkwJJWvuhao65RTuAPRa
  ... Content-Disposition: form-data; name="field.name"
  ...
  ...
  ... ------------61t9UJyoacebBevQVdNrlvXP6T9Ik3Xo4RyXkwJJWvuhao65RTuAPRa
  ... Content-Disposition: form-data; name="field.provided"
  ...
  ... zope.catalog.interfaces.ICatalog
  ... ------------61t9UJyoacebBevQVdNrlvXP6T9Ik3Xo4RyXkwJJWvuhao65RTuAPRa
  ... Content-Disposition: form-data; name="field.provided-empty-marker"
  ...
  ... 1
  ... ------------61t9UJyoacebBevQVdNrlvXP6T9Ik3Xo4RyXkwJJWvuhao65RTuAPRa
  ... Content-Disposition: form-data; name="field.comment"
  ...
  ...
  ... ------------61t9UJyoacebBevQVdNrlvXP6T9Ik3Xo4RyXkwJJWvuhao65RTuAPRa
  ... Content-Disposition: form-data; name="field.actions.register"
  ...
  ... Register
  ... ------------61t9UJyoacebBevQVdNrlvXP6T9Ik3Xo4RyXkwJJWvuhao65RTuAPRa--
  ... """))
  HTTP/1.1 303 ...


Once we have a catalog, we can add indexes to it.  Before we add an
index, let's add a templated page.  When adding indexes, existing
objects are indexed, so the document we add now will appear in the
index:

  >>> print(http(r"""
  ... POST /+/zope.app.zptpage.ZPTPage%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Length: 780
  ... Content-Type: multipart/form-data; boundary=---------------------------1425445234777458421417366789
  ... Referer: http://localhost:8081/+/zope.app.zptpage.ZPTPage=
  ...
  ... -----------------------------1425445234777458421417366789
  ... Content-Disposition: form-data; name="field.source"
  ...
  ... <html>
  ... <body>
  ... Now is the time, for all good dudes to come to the aid of their country.
  ... </body>
  ... </html>
  ... -----------------------------1425445234777458421417366789
  ... Content-Disposition: form-data; name="field.expand.used"
  ...
  ...
  ... -----------------------------1425445234777458421417366789
  ... Content-Disposition: form-data; name="field.evaluateInlineCode.used"
  ...
  ...
  ... -----------------------------1425445234777458421417366789
  ... Content-Disposition: form-data; name="UPDATE_SUBMIT"
  ...
  ... Add
  ... -----------------------------1425445234777458421417366789
  ... Content-Disposition: form-data; name="add_input_name"
  ...
  ... dudes
  ... -----------------------------1425445234777458421417366789--
  ... """))
  HTTP/1.1 303 ...

