from flask import Flask, request, abort
from flask_restx import Api, fields, Resource
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent
from watchdog.observers import Observer

from hathor.project.information.project import Project, find_projects
from hathor.serve.client import Client, CLIENTS

app = Flask("hathor")
app.url_map.strict_slashes = False

api = Api(
    app,
    version="1.0",
    title="Hathor Synchronization API",
    authorizations={
        "client_id": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    }
)


class Namespaces:
    announce = api.namespace("announce", "Client announcements")
    changelist = api.namespace("changelist", "Changelist API")
    package = api.namespace("package", "Synchronization Packages")


class Models:
    announcement = api.model("Announcement", {
        "name": fields.String(description="The name for the new client")
    })

    announcement_response = api.model("AnnouncementResponse", {
        "sessionId": fields.String(description="The session ID for the announced client")
    })

    changelist_entry = api.model("ChangeListEntry", {
        "id": fields.String(description="The unique ID for this change"),
        "kind": fields.String(description="The kind of change"),
        "path": fields.List(fields.String()),
        "isDirectory": fields.Boolean(),
        "isFile": fields.Boolean()
    })

    change_delete_request = api.model("ChangeDeleteRequest", {
        "changes": fields.List(fields.String())
    })

    package_takeout = api.model("PackageTakeout", {
        "content": fields.Arbitrary(),
        "remainingChanges": fields.Integer(),
        "packageSize": fields.Integer()
    })

    create_package_request = api.model("CreatePackageRequest", {
        "changes": fields.List(fields.String())
    })

    package = api.model("Package", {
        "id": fields.String()
    })

    delete_package_request = api.model("DeletePackageRequest", {
        "packageId": fields.String()
    })


def auth_token():
    header = request.headers.get("Authorization")
    if header is None:
        return

    header_spl = header.strip().split(" ")
    assert header_spl[0].strip().lower() == "bearer"

    return header_spl[1]


def find_client() -> Client:
    if client_id := auth_token():
        if client := CLIENTS.get(client_id, None):
            return client

    abort(403)


def doc_auth_token(ns):
    def deco(*args):
        return ns.param("Authorization", "Client ID", _in="header")(*args)

    return deco


@Namespaces.announce.route("/")
class Announcements(Resource):
    @Namespaces.announce.expect(Models.announcement)
    @Namespaces.announce.marshal_with(Models.announcement_response)
    def post(self):
        data = request.json
        client = Client(data["name"])

        return {
            "sessionId": client.id
        }

    @api.doc(security="client_id")
    @doc_auth_token(Namespaces.announce)
    def delete(self):
        client = find_client()
        client.remove()

        return "OK", 200


@Namespaces.changelist.route("/")
class ChangeList(Resource):
    @Namespaces.changelist.marshal_list_with(Models.changelist_entry)
    def get(self):
        return []

    @Namespaces.changelist.expect(Models.change_delete_request)
    def delete(self):
        pass


@Namespaces.package.route("/")
class Packages(Resource):
    @Namespaces.package.param("id", description="The package ID to retrieve")
    @Namespaces.package.marshal_with(Models.package_takeout)
    def get(self):
        pass

    @Namespaces.package.expect(Models.create_package_request)
    @Namespaces.package.marshal_with(Models.package)
    def post(self):
        pass

    @Namespaces.package.expect(Models.delete_package_request)
    def delete(self):
        pass


def watch_files(project: Project):
    projects = find_projects()
    assert len(projects), f"Only one project can be served at a time, found {len(projects)}"

    class ChangeHandler(FileSystemEventHandler):

        def on_created(self, event):
            super().on_created(event)

            if isinstance(event, FileCreatedEvent):
                print("Create", event.src_path)

        def on_deleted(self, event):
            super().on_deleted(event)

            if isinstance(event, FileDeletedEvent):
                print("Delete", event.src_path)

        def on_modified(self, event):
            super().on_modified(event)

            if isinstance(event, FileModifiedEvent):
                print("Modify", event.src_path)

    observer = Observer()
    event_handler = ChangeHandler()

    for path in project.source_directories:
        observer.schedule(event_handler, str(path.absolute()), recursive=True)

    observer.start()


def run(project: Project):
    host = project.serve_config.get("host", "127.0.0.1")
    port = str(project.serve_config.get("port", 8080))
    assert port.isnumeric(), f"The provided port {port} is not numerical"
    port = int(port)

    watch_files(project)

    app.run(debug=True, host=host, port=port)
