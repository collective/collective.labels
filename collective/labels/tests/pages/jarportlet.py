from collective.labels.tests.browser import get_current_browser


def portlet():
    return get_current_browser().css('.labelJarPortlet').first_or_none


def labels():
    assert portlet(), 'labelJarPortlet is not visible'
    return dict(
        (label.text, label_color(label))
        for label in portlet().css('.labelListing .labelColor .labelTitle')
    )


def label_color(label_node):
    return label_node.parent().css('.labelColor').first.attrib.get('data-color')
