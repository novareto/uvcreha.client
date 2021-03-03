from uvcreha import models
from uvcreha.app import backend
from uvcreha.browser.crud import AddForm


@backend.route("/users/add")
class AddUserForm(AddForm):
    title = "Benutzer anlegen"
    model = models.User

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )
