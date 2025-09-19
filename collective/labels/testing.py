from collective.builder.testing import BUILDER_LAYER
from collective.builder.testing import functional_session_factory
from collective.builder.testing import set_builder_session_factory
from collective.testing.layer import ComponentRegistryLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
import collective.labels.tests.builders
import logging
import sys


handler = logging.StreamHandler(stream=sys.stderr)
logging.root.addHandler(handler)


class AdaptersZCMLLayer(ComponentRegistryLayer):
    """A layer which only loads the adapters.zcml.
    """

    def setUp(self):
        super(AdaptersZCMLLayer, self).setUp()
        import collective.labels
        self.load_zcml_file('adapters.zcml', collective.labels)


ADAPTERS_ZCML_LAYER = AdaptersZCMLLayer()


class LabelsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import collective.labels
        xmlconfig.file('configure.zcml',
                       collective.labels,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.labels:default')


LABELS_FIXTURE = LabelsLayer()
LABELS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LABELS_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="collective.labels:functional")
