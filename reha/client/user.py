from collections import defaultdict, Counter
from reiter.view.meta import View
from uvcreha.browser.form import Form
from uvcreha.browser.crud import AddForm, DefaultView, EditForm
from uvcreha import contenttypes
from uvcreha.workflow import user_workflow
from reha.client.app import backend, AdminRequest, TEMPLATES


@backend.route("/user.add", name="user.add")
class AddUserForm(AddForm):
    title = "Benutzer anlegen"

    def update(self):
        self.content_type = contenttypes.registry['user']

    def create(self, data):
        binding = self.content_type.bind(self.request.database)
        data = data.form.dict()
        obj, response = binding.create(**{
            **self.params,
            **data,
            '_key': data['uid'],
            'state': user_workflow.states.pending.name
        })
        self.request.app.notify(
            "user_created",
            request=self.request, uid=obj['uid'], user=obj)
        return obj

    def get_form(self):
        return Form.from_schema(
            self.content_type.schema,
            include=("uid", "loginname", "password", "email")
        )


@backend.route("/users/{uid}", name="user.view")
class UserIndex(View):
    template = TEMPLATES['user_lp']
    listing = TEMPLATES['listing']

    def update(self):
        self.uid = self.params['uid']
        self.content_type = contenttypes.registry['user']
        self.context = self.content_type.bind(
            self.request.database).fetch(self.uid)

    def GET(self):
        ct = contenttypes.registry['file']
        files = ct.bind(self.request.database).find(uid=self.uid)
        docs = defaultdict(list)
        counters = defaultdict(Counter)
        ct = contenttypes.registry['document']
        for doc in ct.bind(self.request.database).find(uid=self.uid):
            docs[doc['az']].append(doc)
            counters[doc['az']].update([doc.state.value])
        return {
            'files': files,
            'docs': docs,
            'counters': counters
        }


@backend.route("/users/{uid}/edit", name="user.edit")
class EditUserForm(EditForm):
    title = "Benutzer anlegen"
    readonly = ('uid',)

    def update(self):
        self.uid = self.params['uid']
        self.content_type = contenttypes.registry['user']
        self.context = self.content_type.bind(
            self.request.database).fetch(self.uid)

    def get_initial_data(self):
        return self.context

    def apply(self, data):
        formdata = data.form.dict()
        return self.content_type.bind(
            self.request.database).update(formdata['uid'], **formdata)

    def remove(self, id):
        return self.content_type.bind(self.request.database).delete(id)

    def get_form(self):
        return Form.from_schema(
            self.content_type.schema, include=(
                "uid", "loginname", "password", "email"
            )
        )
