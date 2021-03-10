from uvcreha import models
from uvcreha.browser.crud import AddForm
from reha.client.app import backend


@backend.route("/users/add")
class AddUserForm(AddForm):
    title = "Benutzer anlegen"
    model = models.User

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )
