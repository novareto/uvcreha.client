import pathlib
from typing import NamedTuple, Callable
from fanstatic import Library, Resource
from reiter.arango.connector import Connector
from reiter.view.meta import View
from reiter.application.browser import TemplateLoader
from uvcreha import models
from uvcreha.app import Browser, fanstatic_middleware, session_middleware
from uvcreha.browser.login import LoginForm
from reha.client.auth import Auth
from chameleon import PageTemplate
from ukh.reha.app import UKHRequest


TEMPLATES = TemplateLoader("./templates")
library = Library("reha.client", "static")
htmx = Resource(library, 'htmx.js', bottom=True)


class AdminRequest(UKHRequest):
    pass


class Backend(Browser):

    def check_permissions(self, route, environ):
        # backend specific security check.
        pass

    def configure(self, config):
        self.config.update(config.app)
        self.connector = Connector(**config.arango)
        self.request_factory = AdminRequest

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


class UserRepresentation(NamedTuple):
    user: models.User
    path: Callable

    @property
    def uid(self):
        return self.user.uid

    @property
    def state(self):
        return self.user.state # fixme : use workflow to get name

    @property
    def loginname(self):
        return self.user.loginname

    @property
    def view(self):
        return self.path('user.view', uid=self.user.uid)

    @property
    def edit(self):
        return self.path('user.view', uid=self.user.uid)

    @property
    def new_file(self):
        return self.path('user.new_file', uid=self.user.uid)


@backend.route("/")
class Index(View):
    template = TEMPLATES["index.pt"]
    search = TEMPLATES["users.pt"]

    def update(self):
        htmx.need()
        self.base = self.request.environ['SCRIPT_NAME']

    def get_users(self):
        return [
            UserRepresentation(user, self.request.route_path)
            for user in self.request.database(models.User).find()
        ]

    def GET(self):
        users = self.get_users()
        return {'users': users}

    def POST(self):
        data = self.request.extract()
        query = data.form.get('search')
        users = [x for x in self.get_users()
                 if x.loginname.startswith(query)]
        return self.search(macros=self.template.macros, users=users)


backend.route("/login")(LoginForm)


@backend.ui.register_slot(request=AdminRequest, name="sitecap")
def sitecap(request, name):
    return 'Some header'


@backend.ui.register_slot(request=AdminRequest, name="footer")
def footer(request, name):
    return 'Some footer'
