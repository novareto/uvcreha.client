from typing import NamedTuple
from horseman.prototyping import Environ
from horseman.response import redirect


class BackendUser(NamedTuple):
    loginname: str


class Auth:

    unprotected = {'/login'}

    def __init__(self, config):
        self.config = config

    def from_credentials(self, credentials: dict):
        if credentials == {'loginname': 'admin', 'password': 'admin'}:
            return BackendUser(loginname='admin')

    def identify(self, environ: Environ):
        if (user := environ.get(self.config.user)) is not None:
            return user
        session = environ[self.config.session]
        if (user_key := session.get(self.config.user, None)) is not None:
            user = environ[self.config.user] = BackendUser(
                loginname=user_key)
            return user
        return None

    def remember(self, environ: Environ, user):
        session = environ[self.config.session]
        session[self.config.user] = user.loginname
        environ[self.config.user] = user
        session.save()

    def __call__(self, app):

        def auth_application_wrapper(environ, start_response):
            user = self.identify(environ)

            if environ['PATH_INFO'] not in self.unprotected:
                # App results need protection checks now.
                if user is None:
                    # Protected access and no user. Go login.
                    return redirect(environ['SCRIPT_NAME'] + '/login')(
                        environ, start_response)
            return app(environ, start_response)

        return auth_application_wrapper
