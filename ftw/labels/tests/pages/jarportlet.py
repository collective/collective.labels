from asserts import assert_true
from ftw.testbrowser import browser


def portlet():
    return browser.css('.labelJarPortlet').first_or_none


def labels():
    assert_true(portlet())
    return dict((label.text, label_color(label))
                for label in portlet().css('.labelJarPortletListingItem'))


def label_color(label_li):
    span = label_li.css('.labelJarPortletListingItem').first
    style = span.attrib.get('style', '')
    color = style.split(':')[1]
    return color
