from uvcreha import models
from uvcreha.browser.crud import AddForm
from reha.client.app import backend


@backend.route("/users/{uid}/files/{az}/add_document", name="file.new_doc")
class AddDocument(AddForm):
    title = "Benutzer anlegen"
    model = models.Document
    readonly = ('az', 'uid')

    def get_initial_data(self):
        return self.params

    def get_fields(self):
        return self.fields(
            exclude=(
                'key', 'id', 'rev',  # arango fields
                'creation_date', # auto-added value
                'state', # workflow state
                'item', # content_type based
            )
        )
