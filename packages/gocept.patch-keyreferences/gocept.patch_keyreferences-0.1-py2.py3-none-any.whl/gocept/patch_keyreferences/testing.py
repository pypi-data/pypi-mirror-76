from zope.app.wsgi.testlayer import BrowserLayer

import gocept.patch_keyreferences

PatchedAppCatalogLayer = BrowserLayer(
    gocept.patch_keyreferences,
    allowTearDown=True)
