import pathlib
from typing import NamedTuple, Callable, Dict
from chameleon import PageTemplate
from fanstatic import Library, Resource
from reiter.application.browser import TemplateLoader
from reiter.view.meta import View
from uvcreha import models
from uvcreha.app import Browser
from uvcreha.plugins import fanstatic_middleware, session_middleware
from uvcreha.browser.login import LoginForm
from uvcreha import contenttypes
from uvcreha.database import Connector
from uvcreha.emailer import SecureMailer
from uvcreha.request import Request
from reha.client.auth import Auth


TEMPLATES = TemplateLoader("./templates")
library = Library("reha.client", "static")
htmx = Resource(library, 'htmx.js', bottom=True)
css = Resource(library, 'admin.css')


class AdminRequest(Request):

    def __init__(self, app, environ, route):
        super(AdminRequest, self).__init__(app, environ, route)
        css.need()


class Backend(Browser):

    def check_permissions(self, route, environ):
        # backend specific security check.
        pass

    def configure(self, config):
        self.config.update(config.app)
        self.connector = Connector.from_config(**config.arango)
        self.request_factory = AdminRequest

        # utilities
        db = self.connector.get_database()
        auth = Auth(self.config.env)
        self.utilities.register(auth, name="authentication")

        if config.emailer:
            emailer = SecureMailer(config.emailer)
            self.utilities.register(emailer, name="emailer")

        # middlewares
        self.register_middleware(
            fanstatic_middleware(self.config.assets), order=0)

        middleware = session_middleware(self.config)
        middleware.manager.cookie_name += ".admin"
        self.register_middleware(middleware, order=1)

        self.register_middleware(auth, order=2)


backend = Backend(name='Backend Application')


@backend.route("/")
class Index(View):
    template = TEMPLATES['index']
    listing = TEMPLATES['listing']

    def update(self):
        htmx.need()
        self.base = self.request.environ['SCRIPT_NAME']

    def get_users(self, query: str=''):
        binding = contenttypes.registry['user'].bind(self.request.database)
        users = binding.find()
        if not query:
            return users
        return [user for user in users if user.title.startswith(query)]

    def GET(self):
        users = self.get_users()
        return {'brains': users, "listing_title": "Users"}

    def POST(self):
        data = self.request.extract()
        query = data.form.get('search')
        users = self.get_users(query)
        return self.listing.render(
            brains=users,
            listing_title=query and f"Users (search for {query})" or "Users"
        )


backend.route("/login")(LoginForm)


@backend.ui.register_slot(request=AdminRequest, name="sitecap")
def sitecap(request, name, view):
    return ''


@backend.ui.register_slot(request=AdminRequest, name="footer")
def footer(request, name, view):
    return TEMPLATES["footer.pt"].render(request=request)
