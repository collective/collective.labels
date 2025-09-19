from Products.CMFCore.utils import getToolByName
from collective.builder import Builder
from collective.builder import create
from collective.labels.testing import LABELS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest import TestCase


class TestCatalogIndex(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def test_index_is_registered(self):
        self.assertIn('labels', self.catalog.indexes())

    def test_updating_index(self):
        root = create(Builder('label root')
                      .with_labels(('Question', 'blue', False),
                                   ('Bugs', 'red', True),
                                   ('Enhancements', 'green', True)))

        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question')
                      .with_pers_labels('bugs'))

        self.assertFalse(self.index_data_for(page).get('labels'))

        page.reindexObject(idxs=['labels'])

        labels = self.index_data_for(page).get('labels')
        self.assertTrue(labels)
        self.assertCountEqual(['bugs', 'test_user_1_:bugs', 'question'], labels)

    def index_data_for(self, obj):
        rid = self.catalog.getrid('/'.join(obj.getPhysicalPath()))
        return self.catalog.getIndexDataForRID(rid)
