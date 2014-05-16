from ftw.labels.config import COLORS
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from plone.app.portlets.portlets.base import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Renderer(Renderer):
    render = ViewPageTemplateFile('labeljar.pt')

    @property
    def available(self):
        return ILabelRoot.providedBy(self.context)

    @property
    def labels(self):
        return ILabelJar(self.context).list()

    @property
    def colors(self):
        return [dict(
            normal=color,
            light='{0}-light'.format(color)
            ) for color in COLORS]
