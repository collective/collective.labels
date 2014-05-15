from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class AdaptersZCMLLayer(ComponentRegistryLayer):
    """A layer which only loads the adapters.zcml.
    """

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.labels
        self.load_zcml_file('adapters.zcml', ftw.labels)


ADAPTERS_ZCML_LAYER = AdaptersZCMLLayer()


class LabelsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import ftw.labels
        xmlconfig.file('configure.zcml',
                       ftw.labels,
                       context=configurationContext)


LABELS_FIXTURE = LabelsLayer()
LABELS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LABELS_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.labels:functional")
