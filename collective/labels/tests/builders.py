from collective.builder import builder_registry
from collective.builder.dexterity import DexterityBuilder
from collective.labels.interfaces import ILabelJarChild
from collective.labels.interfaces import ILabeling
from collective.labels.interfaces import ILabelJar
from collective.labels.interfaces import ILabelRoot
from collective.labels.interfaces import ILabelSupport
import transaction


class LabelRootBuilder(DexterityBuilder):

    portal_type = 'Folder'

    def __init__(self, *args, **kwargs):
        super(LabelRootBuilder, self).__init__(*args, **kwargs)
        self.providing(ILabelRoot)
        self.labels = []

    def with_labels(self, *labels):
        self.labels.extend(labels)
        return self

    def after_create(self, obj):
        super(LabelRootBuilder, self).after_create(obj)
        jar = ILabelJar(obj)
        for title, color, by_user in self.labels:
            jar.add(title, color, by_user)

        if self.session.auto_commit:
            transaction.commit()


builder_registry.register('label root', LabelRootBuilder)


class LabelDisplayBuilder(DexterityBuilder):

    portal_type = 'Folder'

    def __init__(self, *args, **kwargs):
        super(LabelDisplayBuilder, self).__init__(*args, **kwargs)
        self.providing(ILabelJarChild)


builder_registry.register('label display', LabelDisplayBuilder)


class LabelledPageBuilder(DexterityBuilder):

    portal_type = 'Document'

    def __init__(self, *args, **kwargs):
        super(LabelledPageBuilder, self).__init__(*args, **kwargs)
        self.providing(ILabelSupport)
        self.activated_label_ids = []
        self.personal_label_ids = []

    def with_labels(self, *label_ids):
        self.activated_label_ids = label_ids
        return self

    def with_pers_labels(self, *label_ids):
        self.personal_label_ids = label_ids
        return self

    def after_create(self, obj):
        super(LabelledPageBuilder, self).after_create(obj)

        ILabeling(obj).update(self.activated_label_ids)
        ILabeling(obj).pers_update(self.personal_label_ids, True)
        if self.session.auto_commit:
            transaction.commit()


builder_registry.register('labelled page', LabelledPageBuilder)
