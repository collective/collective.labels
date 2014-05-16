from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.labels.interfaces import ILabelSupport
from plone.app.portlets.portlets.base import Renderer


class Renderer(Renderer):
    render = ViewPageTemplateFile('labeling.pt')

    @property
    def available(self):
        return ILabelSupport.providedBy(self.context)
