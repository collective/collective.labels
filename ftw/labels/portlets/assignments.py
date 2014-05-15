from ftw.labels.portlets.interfaces import ILabelJarPortlet
from plone.app.portlets.portlets.base import Assignment
from zope.interface import implements


class Assignment(Assignment):
    implements(ILabelJarPortlet)

    @property
    def title(self):
        return 'ftw.labels: Label Jar Portlet'
