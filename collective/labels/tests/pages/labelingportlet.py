from collective.labels.tests.browser import get_current_browser


def portlet():
    return get_current_browser().css('.labelingPortlet').first_or_none


def active_labels():
    assert portlet(), 'labeling portlet is not visible'
    return portlet().css('.activeLabels .labelItem').text


def form():
    node = portlet().css('.updateLabeling').first_or_none
    assert node, 'The updateLabeling form is missing.'
    return node


def form_checkboxes():
    result = {}
    for input_node in form().inputs:
        if not input_node.label:
            continue  # submit button
        result[input_node.label.text] = bool(input_node.attrib.get('checked'))
    return result
