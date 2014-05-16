from asserts import assert_true
from ftw.testbrowser import browser


def portlet():
    return browser.css('.labelJarPortlet').first_or_none


def labels():
    assert_true(portlet())
    return dict((label.text, label_color(label))
                for label in portlet().css('.labelItem'))


def label_color(label_li):
    css_class = filter(
        lambda cls: cls.startswith('labelcolor-'), label_li.classes)[0]
    return css_class.replace('labelcolor-', '')
