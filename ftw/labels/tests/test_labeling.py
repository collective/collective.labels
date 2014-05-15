from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from ftw.labels.interfaces import ILabelSupport
from ftw.labels.interfaces import ILabeling
from ftw.labels.testing import ADAPTERS_ZCML_LAYER
from ftw.testing import MockTestCase
from zope.annotation import IAttributeAnnotatable
from zope.component import queryAdapter


class TestLabeling(MockTestCase):
    layer = ADAPTERS_ZCML_LAYER

    def setUp(self):
        super(TestLabeling, self).setUp()
        self.root = self.providing_stub([ILabelRoot, IAttributeAnnotatable])
        self.document = self.providing_stub([ILabelSupport, IAttributeAnnotatable])
        self.replay()
        self.jar = ILabelJar(self.root)

    def test_adapter(self):
        self.assertTrue(
            queryAdapter(self.document, ILabeling),
            'The labeling adapter is not registered for ILabeling')

    def test_available_labels(self):
        self.jar.add('Question', '#00FF00')
        labeling = ILabeling(self.document)
        self.assertEqual(
            {'label_id': 'question',
             'title': 'Question',
             'color': '#00FF00',
             'active': False},
            labeling.available_labels())

    def test_activate_label(self):
        self.jar.add('Question', '#00FF00')
        labeling = ILabeling(self.document)

        labeling.activate('Question')
        self.assertEqual(
            {'label_id': 'question',
             'title': 'Question',
             'color': '#00FF00',
             'active': True},
            labeling.available_labels())

    def test_activate_raises_KeyError_when_label_not_in_jar(self):
        self.assertEqual(0, len(self.jar.list()))
        labeling = ILabeling(self.document)
        with self.assertRaises(KeyError) as cm:
            labeling.activate('Something')

        self.assertEqual(
            'Cannot activate label: the label "Something" is not in the label jar.',
            str(cm.exception))

    def test_deactivate_label(self):
        self.jar.add('Question', '')
        labeling = ILabeling(self.document)

        labeling.activate('Question')
        self.assertEqual(1, len(labeling.active_labels()))

        self.assertTrue(labeling.deactivate('Question'))
        self.assertEqual(0, len(labeling.active_labels()))

        self.assertFalse(labeling.deactivate('Question'))

    def test_active_labels(self):
        self.jar.add('Question', '')
        self.jar.add('Bug', '')
        self.jar.add('Duplicate', '')

        labeling = ILabeling(self.document)
        labeling.activate('Bug')
        self.assertEqual(
            {'label_id': 'bug',
             'title': 'Bug',
             'color': ''},
            labeling.active_labels())
