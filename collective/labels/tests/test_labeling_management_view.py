from Products.CMFCore.utils import getToolByName
from collective.builder import Builder
from collective.builder import create
from collective.labels.interfaces import ILabeling
from collective.labels.testing import LABELS_FUNCTIONAL_TESTING
from collective.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest import TestCase


class TestLabelingView(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    @browsing
    def test_activate_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple', False),
                                   ('Bug', 'red', False),
                                   ('Feature', 'blue', True)))
        page = create(Builder('labelled page').within(root))
        self.assertFalse(self.indexed_labels_for(page))

        browser.login().open(page,
                             view='labeling/update',
                             data={'activate_labels': ['question', 'bug']})

        self.assertCountEqual(
            [{'label_id': 'question',
              'title': 'Question',
              'color': 'purple',
              'by_user': False},
             {'label_id': 'bug',
              'title': 'Bug',
              'color': 'red',
              'by_user': False}],
            ILabeling(page).active_labels())

        self.assertCountEqual(['bug', 'question'], self.indexed_labels_for(page))

        browser.login().open(page,
                             view='pers-labeling/pers_update',
                             data={'label_id': 'feature', 'active': 'False'})

        self.assertCountEqual(
            [{'label_id': 'question',
              'title': 'Question',
              'color': 'purple',
              'by_user': False},
             {'label_id': 'bug',
              'title': 'Bug',
              'color': 'red',
              'by_user': False},
             {'label_id': 'feature',
              'title': 'Feature',
              'color': 'blue',
              'by_user': True}],
            ILabeling(page).active_labels())

        self.assertCountEqual(['bug', 'question', 'feature', 'test_user_1_:feature'], self.indexed_labels_for(page))

    @browsing
    def test_deactivate_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple', False),
                                   ('Bug', 'red', False),
                                   ('Feature', 'blue', True)))
        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question', 'bug')
                      .with_pers_labels('feature'))

        browser.login().open(page,
                             view='labeling/update',
                             data={})

        self.assertCountEqual(
            [{'label_id': 'feature',
              'title': 'Feature',
              'color': 'blue',
              'by_user': True}],
            ILabeling(page).active_labels())

        browser.login().open(page,
                             view='pers-labeling/pers_update',
                             data={'label_id': 'feature', 'active': 'True'})

        self.assertCountEqual(
            [],
            ILabeling(page).active_labels())

    @browsing
    def test_mixed_updating_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple', False),
                                   ('Bug', 'red', False),
                                   ('Feature', 'blue', False)))
        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question', 'bug'))

        browser.login().open(page,
                             view='labeling/update',
                             data={'activate_labels': ['question', 'feature']})

        self.assertCountEqual(
            [{'label_id': 'question',
              'title': 'Question',
              'color': 'purple',
              'by_user': False},
             {'label_id': 'feature',
              'title': 'Feature',
              'color': 'blue',
              'by_user': False}],
            ILabeling(page).active_labels())

    @browsing
    def test_updating_is_protected(self, browser):
        root = create(Builder('label root'))
        page = create(Builder('labelled page').within(root))
        browser.login(create(Builder('user').with_roles('Reader')))

        with browser.expect_unauthorized():
            browser.open(page,
                         view='labeling/update',
                         data={'question': 'yes',
                               'feature': 'yes'})

        with browser.expect_unauthorized():
            browser.open(page,
                         view='pers-labeling/pers_update',
                         data={})

    def indexed_labels_for(self, obj):
        catalog = getToolByName(self.portal, 'portal_catalog')
        rid = catalog.getrid('/'.join(obj.getPhysicalPath()))
        return catalog.getIndexDataForRID(rid).get('labels')
