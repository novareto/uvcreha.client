from uvcreha import models
from uvcreha.browser.crud import AddForm
from reha.client.app import backend


@backend.route("/users/{uid}/add_file")
class AddFile(AddForm):
    title = "Benutzer anlegen"
    model = models.File
    readonly = ('uid',)
