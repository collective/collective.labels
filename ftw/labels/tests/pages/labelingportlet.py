from ftw.testbrowser import browser


def portlet():
    return browser.css('.labeling-portlet').first_or_none
