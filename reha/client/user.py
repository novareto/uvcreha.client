from uvcreha import models
from uvcreha.browser.crud import AddForm, DefaultView, EditForm
from reha.client.app import backend, AdminRequest, TEMPLATES



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


@backend.route("/users/{uid}/edit", name="user.edit")
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
    files = [models.FileBrain.create(file, request)
             for file in request.database(
                     models.File).find(uid=view.context.uid)]
    return TEMPLATES["listing.pt"].render(
        brains=files, listing_title="Files")
