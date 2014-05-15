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
from ftw.labels.interfaces import ILabelJar


class ILabelJarPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=_(u'Title'),
        description=u'',
        required=True,
        default=u'')


class Assignment(base.Assignment):
    implements(ILabelJarPortlet)

    def __init__(self, portlet_title=""):
        self.portlet_title = portlet_title


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('labeljar.pt')

    @property
    def available(self):
        return ILabelRoot.providedBy(self.context)

    @property
    def labels(self):
        return ILabelJar(self.context).list()


class AddForm(form.AddForm):
    implements(IPortletAddForm)
    label = _(u'Add label jar portlet')
    fields = field.Fields(ILabelJarPortlet)

    def create(self, data):
        return Assignment(portlet_title=data.get('portlet_title', ''))


class EditForm(form.EditForm):
    implements(IPortletEditForm)
    label = _(u'Edit label jar portlet')
    fields = field.Fields(ILabelJarPortlet)
