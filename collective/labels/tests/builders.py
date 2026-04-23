from collective.labels.interfaces import ILabeling
from collective.labels.interfaces import ILabelJar
from collective.labels.interfaces import ILabelJarChild
from collective.labels.interfaces import ILabelRoot
from collective.labels.interfaces import ILabelSupport
from zope.interface import alsoProvides

import plone.api
import transaction


_registry = {}


def Builder(name):
    cls = _registry.get(name)
    if cls is None:
        raise KeyError(f"No builder registered for '{name}'")
    return cls()


def create(builder):
    return builder.create()


class BaseBuilder:

    portal_type = None
    _extra_interfaces = ()

    def __init__(self):
        self._container = None
        self._title = None
        self._interfaces = list(self._extra_interfaces)

    def within(self, container):
        self._container = container
        return self

    def titled(self, title):
        self._title = title
        return self

    def providing(self, *interfaces):
        self._interfaces.extend(interfaces)
        return self

    def _get_container(self):
        if self._container is not None:
            return self._container
        return plone.api.portal.get()

    def create(self):
        obj = plone.api.content.create(
            container=self._get_container(),
            type=self.portal_type,
            title=self._title or self.portal_type,
        )
        for iface in self._interfaces:
            alsoProvides(obj, iface)
        self._after_create(obj)
        transaction.commit()
        return obj

    def _after_create(self, obj):
        pass


class LabelRootBuilder(BaseBuilder):

    portal_type = 'Folder'
    _extra_interfaces = (ILabelRoot,)

    def __init__(self):
        super().__init__()
        self._labels = []

    def with_labels(self, *labels):
        self._labels.extend(labels)
        return self

    def _after_create(self, obj):
        jar = ILabelJar(obj)
        for title, color, by_user in self._labels:
            jar.add(title, color, by_user)


_registry['label root'] = LabelRootBuilder


class LabelDisplayBuilder(BaseBuilder):

    portal_type = 'Folder'
    _extra_interfaces = (ILabelJarChild,)


_registry['label display'] = LabelDisplayBuilder


class LabelledPageBuilder(BaseBuilder):

    portal_type = 'Document'
    _extra_interfaces = (ILabelSupport,)

    def __init__(self):
        super().__init__()
        self._activated_label_ids = []
        self._personal_label_ids = []

    def with_labels(self, *label_ids):
        self._activated_label_ids = list(label_ids)
        return self

    def with_pers_labels(self, *label_ids):
        self._personal_label_ids = list(label_ids)
        return self

    def _after_create(self, obj):
        ILabeling(obj).update(self._activated_label_ids)
        ILabeling(obj).pers_update(self._personal_label_ids, True)


_registry['labelled page'] = LabelledPageBuilder


class FolderBuilder(BaseBuilder):

    portal_type = 'Folder'


_registry['folder'] = FolderBuilder


_user_counter = 0


class UserBuilder:

    def __init__(self):
        self._roles = []
        self._password = 'secret123'

    def with_roles(self, *roles):
        self._roles.extend(roles)
        return self

    def within(self, container):
        return self

    def create(self):
        global _user_counter
        _user_counter += 1
        username = f'test_user_{_user_counter}'
        email = f'{username}@example.com'
        user = plone.api.user.create(
            email=email,
            username=username,
            password=self._password,
        )
        if self._roles:
            plone.api.user.grant_roles(username=username, roles=list(self._roles))
        transaction.commit()
        return user


_registry['user'] = UserBuilder
