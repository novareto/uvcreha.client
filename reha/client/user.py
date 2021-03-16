from reha.client.app import backend
from uvcreha import models
from uvcreha.browser.crud import AddForm, DefaultView, EditForm


@backend.route("/user.add", name="user.add")
class AddUserForm(AddForm):
    title = "Benutzer anlegen"
    model = models.User

    def hook(self, obj):
        self.request.app.notify(
            "user_created",
            request=self.request, uid=obj.uid, user=obj)

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
