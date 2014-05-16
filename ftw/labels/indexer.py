from ftw.labels.interfaces import ILabelSupport
from ftw.labels.interfaces import ILabeling
from operator import itemgetter
from plone.indexer.decorator import indexer


@indexer(ILabelSupport)
def labels(obj):
    labeling = ILabeling(obj)
    return map(itemgetter('title'), labeling.active_labels())
