from typing import NamedTuple, Callable
from uvcreha import models
from uvcreha.browser.crud import EditForm, AddForm, DefaultView
from reha.client.app import backend, AdminRequest, TEMPLATES


@backend.route("/users/{uid}/add_file", name="user.new_file")
class AddFile(AddForm):
    title = "Benutzer anlegen"
    model = models.File
    readonly = ('uid',)

    def get_fields(self):
        return self.fields(
            only=("az", "uid", "mnr", "vid")
        )


@backend.route("/users/{uid}/file/{az}", name="file.view")
class FileIndex(DefaultView):
    title = "File"
    model = models.File

    def get_fields(self):
        return self.fields(
            only=("uid", "az", "mnr", "vid")
        )


@backend.route("/users/{uid}/file/{az}/edit", name="file.edit")
class FileEdit(EditForm):
    title = "File"
    model = models.File
    readonly = ('uid', 'az')

    def get_fields(self):
        return self.fields(
            only=("uid", "az", "mnr", "vid")
        )


@backend.ui.register_slot(
    request=AdminRequest, view=FileIndex, name="below-content")
def FileDocumentsList(request, name, view):
    docs = [
        models.DocBrain.create(doc, request) for doc in request.database(
            models.Document).find(uid=view.context.uid, az=view.context.az)
    ]
    return TEMPLATES["listing.pt"].render(
        brains=docs, listing_title="Documents")
