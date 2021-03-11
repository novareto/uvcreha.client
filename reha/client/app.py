import pathlib
from fanstatic import Library, Resource
from reiter.arango.connector import Connector
from reiter.view.meta import View
from reiter.application.browser import TemplateLoader
from uvcreha import models
from uvcreha.app import Browser, fanstatic_middleware, session_middleware
from uvcreha.browser.login import LoginForm
from reha.client.auth import Auth
from chameleon import PageTemplate


TEMPLATES = TemplateLoader("./templates")
library = Library("reha.client", "static")
htmx = Resource(library, 'htmx.js', bottom=True)


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

    def update(self):
        htmx.need()

    def get_users(self):
        return self.request.database(models.User).find()

    def GET(self):
        users = self.get_users()
        return {'users': users}

    def POST(self):
        data = self.request.extract()
        query = data.form.get('search')
        users = [x for x in self.get_users() if x.loginname.startswith(query)]
        ret = '<tr tal:repeat="user users"> <td tal:content="user.uid"/> <td tal:content="user.loginname"/> </tr>'
        template = PageTemplate(ret)
        return template(users=users)

backend.route("/login")(LoginForm)
