from uvcreha import models
from uvcreha.browser.crud import AddForm, DefaultView
from reha.client.app import backend


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
