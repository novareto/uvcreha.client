from uvcreha import models
from uvcreha.app import backend
from uvcreha.browser.crud import AddForm


@backend.route("/users/{uid}/add_file")
class AddFile(AddForm):
    title = "Benutzer anlegen"
    model = models.File
    readonly = ('uid',)
