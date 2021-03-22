from collections import defaultdict, Counter
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
class UserIndex(View):
    template = TEMPLATES['user_lp']
    listing = TEMPLATES['listing']

    def update(self):
        self.uid = self.params['uid']
        self.context = models.UserBrain.create(
            self.request.database(models.User).fetch(self.uid), self.request)

    def GET(self):
        files = [
            models.FileBrain.create(file, self.request)
            for file in
            self.request.database(models.File).find(uid=self.uid)
        ]
        docs = defaultdict(list)
        counters = defaultdict(Counter)
        for doc in self.request.database(models.Document).find(uid=self.uid):
            brain = models.DocBrain.create(doc, self.request)
            docs[doc.az].append(brain)
            counters[doc.az].update([brain.state.value])
        return {
            'files': files,
            'docs': docs,
            'counters': counters
        }


@backend.route("/users/{uid}/edit", name="user.edit")
class EditUserForm(EditForm):
    title = "Benutzer anlegen"
    model = models.User
    readonly = ('uid',)

    def get_fields(self):
        return self.fields(
            only=("uid", "loginname", "password", "email")
        )
