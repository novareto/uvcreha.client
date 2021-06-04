from typing import NamedTuple
from horseman.types import Environ
from horseman.response import redirect
from uvcreha.auth import Auth


class BackendUser(NamedTuple):
    title: str


class AdminAuth(Auth):

    def from_credentials(self, credentials: dict):
        if credentials == {'loginname': 'admin', 'password': 'admin'}:
            return BackendUser(title='admin')

    def identify(self, environ: Environ):
        if (user := environ.get(self.user_key)) is not None:
            return user
        session = environ[self.session_key]
        if (user_key := session.get(self.user_key, None)) is not None:
            user = environ[self.user_key] = BackendUser(title=user_key)
            return user
        return None

    def remember(self, environ: Environ, user):
        session = environ[self.session_key]
        session[self.user_key] = user.title
        environ[self.user_key] = user
        session.save()
