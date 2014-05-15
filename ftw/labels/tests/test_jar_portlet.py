from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from glue.suiscms.testing import LABELS_FUNCTIONAL_TESTING
from unittest2 import TestCase


class LabelJarPortletFunctionalTest(TestCase):

    layer = LABELS_FUNCTIONAL_TESTING

    @browsing
    def test_portlet_is_disabled_per_default(self, browser):
        browser.visit()

        self.assertTrue(browser.css('labelJarPortlet'))

    @browsing
    def test_protlet_is_enabled_if_ILabelRoot_is_provided(self, browser):
        folder = create(Builder('label root'))
        browser.visit(folder)

        self.assertTrue(browser.css('labelJarPortlet'))

    @browsing
    def test_list_all_labels_in_the_jar(self, browser):
        folder = create(Builder('label root')
                        .with_labels(('Label 1', ''), ('Label 2', '')))

        browser.visit(folder)
        self.assertEqual(2, len(browser.css('.labelJarPortletListingItem')))

    @browsing
    def test_do_not_show_listing_if_no_labels_are_available(self, browser):
        folder = create(Builder('label root'))

        browser.visit(folder)
        self.assertFalse(browser.css('.labelJarPortletListing'))

    @browsing
    def test_add_color_to_each_listing_item(self, browser):
        folder = create(Builder('label root')
                        .with_labels(('James', 'red'), ('Lara', '#001122')))

        browser.visit(folder)
        import pdb; pdb.set_trace()
        self.assertEqual(
            ['red', '#001122'],
            [label.attrib.get('style') for label in browser.css(
                '.labelJarPortletListingItem')])
