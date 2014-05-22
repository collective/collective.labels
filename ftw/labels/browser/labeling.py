from Products.Five.browser import BrowserView
from ftw.labels.interfaces import ILabeling


class Labeling(BrowserView):

    def update(self):
        """Update activated labels.
        """
        labeling = ILabeling(self.context)

        activate_labels = self.request.form.get('activate_labels', [])

        deactivate = []
        activate = []

        for label in labeling.available_labels():
            label_id = label['label_id']

            if label_id in activate_labels and not label['active']:
                activate.append(label_id)
            if label_id not in activate_labels and label['active']:
                deactivate.append(label_id)

        labeling.deactivate(*deactivate)
        labeling.activate(*activate)
        self.context.reindexObject(idxs=['labels'])
        return self._redirect()

    def _redirect(self):
        response = self.request.RESPONSE
        referer = self.request.get('HTTP_REFERER')
        if referer and referer is not 'localhost':
            response.redirect(referer)
        else:
            response.redirect(self.context.absolute_url())
