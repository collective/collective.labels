from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.labels.interfaces import ILabelSupport
from ftw.labels.interfaces import ILabeling
from ftw.labels.portlets.assignments import LabelingAssignment
from plone.app.portlets.portlets.base import NullAddForm
from plone.app.portlets.portlets.base import Renderer


class AddForm(NullAddForm):

    def create(self):
        return LabelingAssignment()


class Renderer(Renderer):
    render = ViewPageTemplateFile('labeling.pt')

    @property
    def available(self):
        if 'portal_factory' in self.context.absolute_url():
            return False
        if not ILabelSupport.providedBy(self.context):
            return False
        if not tuple(self.available_labels):
            return False
        return True

    @property
    def active_labels(self):
        return ILabeling(self.context).active_labels()

    @property
    def available_labels(self):
        return ILabeling(self.context).available_labels()
