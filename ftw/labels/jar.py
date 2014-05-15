from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from persistent.mapping import PersistentMapping
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements


ANNOTATION_KEY = 'ftw.labels:jar'


class LabelJar(object):
    implements(ILabelJar)
    adapts(ILabelRoot)

    def __init__(self, context):
        self.context = context

    def add(self, title, color):
        label_id = self._make_id(title)
        self.storage[label_id] = PersistentMapping(
            dict(
                label_id=label_id,
                title=title,
                color=color
            )
        )
        return label_id

    def remove(self, label_id):
        if label_id not in self.storage:
            return False

        del self.storage[label_id]
        return True

    def update(self, label_id, title, color):
        self.storage[label_id].update(
            dict(
                title=title,
                color=color
            )
        )

    def get(self, label_id):
        return dict(self.storage[label_id])

    def list(self):
        return self.storage.values()

    @property
    def storage(self):
        if getattr(self, '_storage', None) is None:
            annotation = IAnnotations(self.context)
            if ANNOTATION_KEY not in annotation:
                annotation[ANNOTATION_KEY] = PersistentMapping()
            self._storage = annotation[ANNOTATION_KEY]
        return self._storage

    def _make_id(self, title):
        normalizer = getUtility(IIDNormalizer)
        label_id = base_id = normalizer.normalize(title)

        counter = 0
        while label_id in self.storage:
            counter += 1
            label_id = '{0}-{1}'.format(base_id, counter)

        return label_id
