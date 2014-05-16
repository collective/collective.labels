from Products.Five.browser import BrowserView
from ftw.labels.interfaces import ILabeling


class Labeling(BrowserView):

    def update(self):
        """Update activated labels.
        """
        labeling = ILabeling(self.context)
        form = self.request.form

        deactivate = []
        activate = []

        for label in labeling.available_labels():
            label_id = label['label_id']
            should_be_active = form.get(label_id, False)
            if should_be_active and not label['active']:
                activate.append(label_id)
            if not should_be_active and label['active']:
                deactivate.append(label_id)

        labeling.deactivate(*deactivate)
        labeling.activate(*activate)
        return self.request.RESPONSE.redirect(self.context.absolute_url())
