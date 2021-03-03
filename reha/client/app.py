import pathlib
from fanstatic import Library
from reiter.view.meta import View
from reiter.application.browser import TemplateLoader
from uvcreha import models
from uvcreha.app import backend


TEMPLATES = TemplateLoader(
    str((pathlib.Path(__file__).parent / "templates").resolve()), ".pt"
)

library = Library("reha.client", "static")


@backend.route("/")
class Index(View):
    template = TEMPLATES["index.pt"]

    def GET(self):
        users = self.request.database(models.User).find()
        return dict(request=self.request, users=users)
