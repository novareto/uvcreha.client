from uvcreha import models
from uvcreha.browser.crud import AddForm, DefaultView
from uvcreha.workflow import file_workflow
from reha.client.app import backend


@backend.route("/users/{uid}/add_file", name="user.new_file")
class AddFile(AddForm):
    title = "Benutzer anlegen"
    model = models.File
    readonly = ('uid',)

    def hook(self, obj):
        user = self.request.database(models.User)
        user.update(obj.uid, state=file_workflow.states.created)
        self.request.app.notify(
            "file_created",
            request=self.request, az=obj.az, obj=obj)

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
