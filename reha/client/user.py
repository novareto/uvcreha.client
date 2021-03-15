from typing import NamedTuple, Callable
from uvcreha import models
from uvcreha.browser.crud import AddForm, DefaultView, EditForm
from reha.client.app import backend, AdminRequest, TEMPLATES


class FileRepresentation(NamedTuple):
    file: models.File
    path: Callable

    @property
    def uid(self):
        return self.file.uid

    @property
    def az(self):
        return self.file.az

    @property
    def state(self):
        return self.file.state # fixme : use workflow to get name

    @property
    def view(self):
        return self.path(
            'file.view',
            az=self.file.az,
            uid=self.file.uid
        )


@backend.route("/user.add", name="user.add")
class AddUserForm(AddForm):
    title = "Benutzer anlegen"
    model = models.User

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )


@backend.route("/users/{uid}", name="user.view")
class UserFormIndex(DefaultView):
    title = "User"
    model = models.User

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "email")
        )


@backend.route("/users/{uid}/edit", name="user.update")
class EditUserForm(EditForm):
    title = "Benutzer anlegen"
    model = models.User
    readonly = ('uid',)

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )


@backend.ui.register_slot(
    request=AdminRequest, view=UserFormIndex, name="below-content")
def UserFilesList(request, name, view):
    files = (
        FileRepresentation(file=file, path=request.route_path)
        for file in request.database(
                models.File).find(uid=view.context.uid))
    return TEMPLATES["user_files_list.pt"].render(
        request=request, files=files)
