import pathlib
import horseman

from docmanager.request import Request
from fanstatic import Library
from reiter.application.app import Blueprint
from docmanager.browser.layout import template
from docmanager.browser import TemplateLoader
from docmanager.browser.form import FormView, Form
from horseman.http import Multidict
from reiter.form import trigger

from docmanager import models


TEMPLATES = TemplateLoader(
    str((pathlib.Path(__file__).parent / "templates").resolve()), ".pt"
)

library = Library("uvcreha.client", "static")


clientadmin = Blueprint("ClientAdmin")


@clientadmin.route("/client")
@template(TEMPLATES["index.pt"], layout_name="default", raw=False)
def index(request: Request):
    users = request.database(models.User).find()
    return dict(request=request, users=users)


@clientadmin.route("/add_user")
class AddUserForm(FormView):
    title = "Benutzer anlegen"
    action = "add_user"
    model = models.User

    def setupForm(self, data={}, formdata=Multidict()):
        form = Form.from_model(self.model, only=("username", "password", "email"))
        form.process(data=data, formdata=formdata)
        return form

    @trigger("speichern", "Speichern", css="btn btn-primary")
    def speichern(self, request, data):
        form = self.setupForm(formdata=data.form)
        if not form.validate():
            return {
                "form": form,
                "view": self,
                "error": None,
                "path": request.route.path,
            }
        user, response = request.database(models.User).create(**data.form.dict())
        return horseman.response.Response.create(302, headers={"Location": "/client"})


@clientadmin.route("/client/{username}")
@template(TEMPLATES["index_user.pt"], layout_name="default", raw=False)
def index_user(request: Request, **kwargs):
    user = request.database(models.User).fetch(key=kwargs['username'])
    files = request.database(models.File).find(username=kwargs['username'])
    return dict(request=request, user=user, files=files)


