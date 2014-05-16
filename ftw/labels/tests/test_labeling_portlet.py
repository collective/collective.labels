from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from ftw.labels.tests.pages import labelingportlet
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase


class TestLabelingPortlet(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    @browsing
    def test_labeling_portlet_is_visible_on_labelable_objects(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple')))
        page = create(Builder('labelled page').within(root))
        browser.login().open(page)
        self.assertTrue(labelingportlet.portlet(), 'Portlet should be visible.')

    @browsing
    def test_labeling_portlet_not_visible_other_objects(self, browser):
        root = create(Builder('folder'))
        browser.login().open(root)
        self.assertFalse(labelingportlet.portlet(), 'Portlet should be visible.')

    @browsing
    def test_labeling_portlet_is_visible_if_no_labels_are_available(self, browser):
        root = create(Builder('label root'))
        page = create(Builder('labelled page').within(root))
        browser.login().open(page)
        self.assertFalse(labelingportlet.portlet(), 'Portlet should be visible.')

    @browsing
    def test_labeling_portlet_lists_active_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))
        page = create(Builder('labelled page').within(root)
                      .with_labels('question'))
        browser.login().visit(page)

        self.assertEquals(['Question'], labelingportlet.active_labels())

    @browsing
    def test_form_has_a_list_of_all_available_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))
        page = create(Builder('labelled page').within(root))
        browser.login().visit(page)

        self.assertItemsEqual(
            ['Question', 'Bug'],
            labelingportlet.form().field_labels)

    @browsing
    def test_form_active_label_checkboxes_are_checked(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))
        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question'))
        browser.login().visit(page)

        self.assertEquals(
            {'Question': True,
             'Bug': False},
            labelingportlet.form_checkboxes())

    @browsing
    def test_form_update_activated_labels(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red'),
                                   ('Feature', 'future')))
        page = create(Builder('labelled page')
                      .within(root)
                      .with_labels('question', 'bug'))
        browser.login().visit(page)

        labelingportlet.form().fill({
                'Question': False,
                'Bug': True,
                'Feature': True}).submit()

        self.assertEquals(
            {'Question': False,
             'Bug': True,
             'Feature': True},
            labelingportlet.form_checkboxes())
