import pathlib
from fanstatic import Library
from reiter.arango.connector import Connector
from reiter.view.meta import View
from reiter.application.browser import TemplateLoader
from uvcreha import models
from uvcreha.app import Browser, fanstatic_middleware, session_middleware
from uvcreha.browser.login import LoginForm
from reha.client.auth import Auth


TEMPLATES = TemplateLoader("./templates")
library = Library("reha.client", "static")


class Backend(Browser):

    def check_permissions(self, route, environ):
        # backend specific security check.
        pass

    def configure(self, config):
        self.config.update(config.app)
        self.connector = Connector(**config.arango)
        self.request = config.app.factories.request

        # utilities
        db = self.connector.get_database()
        auth = Auth(self.config.env)
        self.utilities.register(auth, name="authentication")

        # middlewares
        self.register_middleware(
            fanstatic_middleware(self.config.assets), order=0)

        self.register_middleware(
            session_middleware(self.config), order=1)

        self.register_middleware(auth, order=2)


backend = Backend('Backend Application')


@backend.route("/")
class Index(View):
    template = TEMPLATES["index.pt"]

    def GET(self):
        users = self.request.database(models.User).find()
        return {'users': users}


backend.route("/login")(LoginForm)
