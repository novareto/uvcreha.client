from uvcreha import models
from uvcreha.browser.crud import AddForm, DefaultView, EditForm
from .app import clientapp


@clientapp.route("/users/add")
class AddUserForm(AddForm):
    title = "Benutzer anlegen"
    model = models.User

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )


@clientapp.route("/users/{loginname}")
class UserFormIndex(DefaultView):
    title = "User"
    model = models.User

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )


@clientapp.route("/users/{loginname}/edit")
class EditUserForm(EditForm):
    title = "Benutzer anlegen"
    model = models.User
    readonly = ('uid',)

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )
