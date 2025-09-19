from collective.testing.genericsetup import GenericSetupUninstallMixin
from collective.testing.genericsetup import apply_generic_setup_layer
from unittest import TestCase


@apply_generic_setup_layer
class TestGenericSetupUninstall(TestCase, GenericSetupUninstallMixin):

    package = 'collective.labels'
