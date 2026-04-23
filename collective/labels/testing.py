from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.zca import popGlobalRegistry
from plone.testing.zca import pushGlobalRegistry
from zope.configuration import xmlconfig

import collective.labels.tests.builders  # noqa: registers builders at import time
import logging
import sys


handler = logging.StreamHandler(stream=sys.stderr)
logging.root.addHandler(handler)


class AdaptersZCMLLayer:
    """A layer which only loads the adapters.zcml."""

    __name__ = 'AdaptersZCMLLayer'
    __bases__ = ()

    def setUp(self):
        pushGlobalRegistry()
        import collective.labels
        xmlconfig.file('adapters.zcml', collective.labels)

    def tearDown(self):
        popGlobalRegistry()

    def testSetUp(self):
        pass

    def testTearDown(self):
        pass


ADAPTERS_ZCML_LAYER = AdaptersZCMLLayer()


class LabelsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.labels
        xmlconfig.file('configure.zcml',
                       collective.labels,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.labels:default')
        from collective.labels.setuphandler import add_catalog_indexes
        add_catalog_indexes(portal)


LABELS_FIXTURE = LabelsLayer()
LABELS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LABELS_FIXTURE,),
    name='collective.labels:functional')
