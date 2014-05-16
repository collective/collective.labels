from asserts import assert_true
from ftw.testbrowser import browser


def portlet():
    return browser.css('.labeling-portlet').first_or_none


def active_labels():
    assert_true(portlet(), 'labeling portlet is not visible')
    return portlet().css('.active-labels .label').text
