from unittest import TestCase
from unittest.mock import MagicMock
from zope.interface import alsoProvides


class MockTestCase(TestCase):

    def providing_stub(self, interfaces):
        if not isinstance(interfaces, (list, tuple)):
            interfaces = [interfaces]
        mock = MagicMock()
        for iface in interfaces:
            alsoProvides(mock, iface)
        return mock

    def stub(self):
        return MagicMock()

    def set_parent(self, obj, parent):
        obj.__parent__ = parent
        return obj
