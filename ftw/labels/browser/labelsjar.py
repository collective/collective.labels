from Products.Five.browser import BrowserView
from ftw.labels.interfaces import ILabelJar
from zExceptions import BadRequest


class LabelsJar(BrowserView):

    def create(self):
        """Create a new label.
        """

        title = self.request.form.get('title', None)
        color = self.request.form.get('color', None)
        if not title or not color:
            raise BadRequest(
                '"title" and "color" request arguments are required.')

        jar = ILabelJar(self.context)
        jar.get(jar.add(title, color))
        return self.request.RESPONSE.redirect(self.context.absolute_url())

    def update(self):
        """Update a label.
        """

        label_id = self.request.form.get('label_id', None)
        if not label_id:
            raise BadRequest('The "label_id" request argument is required.')

        jar = ILabelJar(self.context)
        label = jar.get(label_id)

        title = self.request.form.get('title', None)
        if title:
            label['title'] = title

        color = self.request.form.get('color', None)
        if color:
            label['color'] = color

        jar.update(**label)
        return self.request.RESPONSE.redirect(self.context.absolute_url())

    def remove(self):
        """Remove a label.
        """

        label_id = self.request.form.get('label_id', None)
        if not label_id:
            raise BadRequest('The "label_id" request argument is required.')

        ILabelJar(self.context).remove(label_id)
        return self.request.RESPONSE.redirect(self.context.absolute_url())
