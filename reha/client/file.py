import horseman.response
from horseman.http import Multidict
from reiter.form import trigger
from uvcreha import models
from uvcreha.browser.crud import AddForm, DefaultView, EditForm
from .app import clientapp


@clientapp.route("/users/{uid}/files/add")
class AddFile(AddForm):
    title = "Benutzer anlegen"
    model = models.File
    readonly = ('uid',)


@clientapp.route("/users/{uid}/files/{az}")
class FileIndex(DefaultView):
    model = models.File


@clientapp.route("/users/{uid}/files/{az}/edit")
class FileEdit(EditForm):
    model = models.File
    readonly = ('uid', 'az')
