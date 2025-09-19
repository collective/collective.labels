collective.labels
=================

A Plone addon for labels.

Containers, Folders for example, can be marked as label container.
For each label container a set of labels with colors can be defined.
Items whithin this container which support labelling can then be labelled
with one or more labels.

Fork of ftw.labels that was unmaintained see https://github.com/4teamwork/ftw.labels/issues/67


Screenshots
-----------

Managing labels on the label container (``ILabelJar``):

.. image:: https://raw.github.com/collective/collective.labels/master/docs/label_jar.png


Set label for a content (``ILabelSupport``):

.. image:: https://raw.github.com/collective/collective.labels/master/docs/label_support.png



Installation
------------

- Add ``collective.labels`` to your buildout configuration:

.. code:: rst

    [instance]
    eggs +=
        collective.labels

- Install the generic setup profile of ``collective.labels``.


Usage / Integration
-------------------

Add the ``ILabelJar`` marker interface to any container class you want:

.. code:: xml

    <class class="Products.ATContentTypes.content.folder.ATFolder">
        <implements interface="collective.labels.interfaces.ILabelRoot" />
    </class>

For objects providing ``ILabelJar`` a left-column-portlet is added
on the root of the Plone site which allows to manage labels.


Add the ``ILabelSupport`` marker interface to any item you want to be able to
set labels on:

.. code:: xml

    <class class="plone.app.blob.content.ATBlob">
        <implements interface="collective.labels.interfaces.ILabelSupport" />
    </class>

For objects providing ``ILabelSupport`` a right-column-portlet is added
on the root of the Plone site which allows to manage labels.


Add the ``ILabelJarChild`` marker interface to any container class to
display the labels stored in a parents ``ILabelJar``

.. code:: xml

    <class class="Products.ATContentTypes.content.folder.ATFolder">
        <implements interface="collective.labels.interfaces.ILabelJarChild" />
    </class>

For objects providing ``ILabelJarChild`` you can manage and store the
same labels as defined in the ``ILabelJar`` content without defining
a new ``ILabelRoot``


Uninstall
---------

The package provides an uninstall mechanism.
Use Plone's addon control panel or portal_quickInstaller to uninstall
the package.



Links
-----

- Github: https://github.com/collective/collective.labels
- Issues: https://github.com/collective/collective.labels/issues
- Pypi: http://pypi.python.org/pypi/collective.labels
- Continuous integration: https://jenkins.4teamwork.ch/search?q=collective.labels


Copyright
---------

This package was created by `4teamwork <http://www.4teamwork.ch/>`_.

``collective.labels`` is licensed under GNU General Public License, version 2.
