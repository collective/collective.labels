from collective.labels.portlets.interfaces import ILabelJarPortlet
from collective.labels.portlets.interfaces import ILabelingPortlet
from plone.app.portlets.portlets.base import Assignment
from zope.interface import implementer


@implementer(ILabelJarPortlet)
class LabelJarAssignment(Assignment):

    @property
    def title(self):
        return 'collective.labels: Label Jar Portlet'


@implementer(ILabelingPortlet)
class LabelingAssignment(Assignment):

    @property
    def title(self):
        return 'collective.labels: Labeling Portlet'
