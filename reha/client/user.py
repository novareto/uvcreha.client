from uvcreha import models
from reiter.view.meta import View
from uvcreha.workflow import user_workflow
from uvcreha.browser.crud import AddForm, DefaultView, EditForm
from reha.client.app import backend, AdminRequest, TEMPLATES


@backend.route("/user.add", name="user.add")
class AddUserForm(AddForm):
    title = "Benutzer anlegen"
    model = models.User

    def hook(self, obj):
        user = self.request.database(models.User)
        user.update(obj.uid, state=user_workflow.states.pending.name)
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


@backend.route("/users/{uid}/lp", name="user.viewlp")
class UserFormIndexLP(View):
    template = TEMPLATES['user_lp.pt']

    def get_docs(self, az):
        uid = self.request.route.params['uid']
        return [
            models.DocBrain.create(doc, self.request) for doc in self.request.database(
                models.Document).find(uid=uid, az=az)
        ]

    def GET(self):
        files = [models.FileBrain.create(file, self.request)
                for file in self.request.database(models.File).find(uid=self.request.route.params['uid'])]
        user = self.request.database(models.User)

        return dict(request=self.request, files=files)


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
