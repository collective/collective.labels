from ftw.labels.portlets.interfaces import ILabelJarPortlet
from ftw.labels.portlets.interfaces import ILabelingPortlet
from plone.app.portlets.portlets.base import Assignment
from zope.interface import implementer


@implementer(ILabelJarPortlet)
class LabelJarAssignment(Assignment):

    @property
    def title(self):
        return 'ftw.labels: Label Jar Portlet'


@implementer(ILabelingPortlet)
class LabelingAssignment(Assignment):

    @property
    def title(self):
        return 'ftw.labels: Labeling Portlet'
