from ftw.labels import _
from ftw.labels.interfaces import ILabelRoot
from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.interface import implements


class ILabelJarPortlet(IPortletDataProvider):

    title = schema.TextLine(
        title=_(u'Title'),
        description=u'',
        required=True,
        default=u'')


class Assignment(base.Assignment):
    implements(ILabelJarPortlet)

    def __init__(self, portlet_title=""):
        self.portlet_title = portlet_title

    @property
    def title(self):
        return u'ftw.labels: label jar portlet'


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('labeljar.pt')

    @property
    def available(self):
        return ILabelRoot.providedBy(self.context)


class AddForm(form.AddForm):
    implements(IPortletAddForm)
    label = _(u'Add label jar portlet')
    fields = field.Fields(ILabelJarPortlet)

    def create(self, data):
        return Assignment(title=data.get('title', ''))


class EditForm(form.EditForm):
    implements(IPortletEditForm)
    label = _(u'Edit label jar portlet')
    fields = field.Fields(ILabelJarPortlet)
