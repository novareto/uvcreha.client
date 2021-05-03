import enum
from horseman.http import Multidict
from reha.client.app import backend
from uvcreha import models
from uvcreha.browser.crud import AddForm, EditForm, DefaultView
from uvcreha.browser.form import Form
from wtforms.fields import SelectField


def alternatives(**opts):
    alts = [(key, schema.get('title', key))
            for key, schema in models.JSONSchemaRegistry.items()]
    return SelectField(
        'Select your content type', choices=alts)


@backend.route("/users/{uid}/files/{az}/add_document", name="file.new_doc")
class AddDocument(AddForm):
    title = "Benutzer anlegen"
    model = models.Document
    readonly = ('az', 'uid')

    def get_fields(self):
        return self.fields(
            exclude=(
                'key', 'id', 'rev',  # arango fields
                'creation_date',  # auto-added value
                'state',  # workflow state
                'item',  # content_type based
            )
        )

    def setupForm(self, data=None, formdata=Multidict()):
        fields = self.get_fields()
        fields['content_type'].factory = alternatives
        form = Form.from_fields(fields)
        form.process(data=self.params, formdata=formdata)
        if self.readonly is not None:
            form.readonly(self.readonly)
        return form


@backend.route("/users/{uid}/file/{az}/docs/{docid}", name="doc.view")
class DocumentIndex(DefaultView):
    title = "Document"
    model = models.Document

    def get_fields(self):
        return self.fields(
            exclude=(
                'key', 'id', 'rev',  # arango fields
                'creation_date', # auto-added value
                'state', # workflow state
                'item', # content_type based
            )
        )


@backend.route("/users/{uid}/file/{az}/docs/{docid}/edit", name="doc.edit")
class DocumentEdit(EditForm):
    title = "Document"
    model = models.Document
    readonly = ('uid', 'az', 'docid', 'content_type')

    def get_fields(self):
        return self.fields(
            exclude=(
                'key', 'id', 'rev',  # arango fields
                'creation_date', # auto-added value
                'state', # workflow state
                'item', # content_type based
            )
        )

    def setupForm(self, data=None, formdata=Multidict()):
        fields = self.get_fields()
        fields['content_type'].factory = alternatives
        form = Form.from_fields(fields)
        form.process(data=self.params, formdata=formdata)
        if self.readonly is not None:
            form.readonly(self.readonly)
        return form
