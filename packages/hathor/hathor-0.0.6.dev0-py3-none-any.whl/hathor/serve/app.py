import dataclasses
import logging
import os
from typing import Tuple

from flask import Flask, request, abort
from flask_restx import Api, fields, Resource

import hathor.serve.client as hathor_client
from hathor.project.information.project import Project
from hathor.serve import project_builder
from hathor.serve.client import Client
from hathor.serve.models import ChangeListEntry
from hathor.serve.watch_files import watch_files

LOG = logging.getLogger(__name__)

app = Flask("Hathor")

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
        "content": fields.String(),
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
        if client := hathor_client.by_id(client_id):
            return client

    abort(403)


def doc_auth_token(ns):
    def deco(*args):
        return ns.param("Authorization", "Client ID", _in="header")(*args)

    return deco


@Namespaces.announce.route("")
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


@Namespaces.changelist.route("")
class ChangeList(Resource):
    @doc_auth_token(Namespaces.changelist)
    @Namespaces.changelist.marshal_list_with(Models.changelist_entry)
    def get(self):
        client = find_client()

        def change_to_dict(change: ChangeListEntry):
            return {
                "id": change.id,
                "kind": change.kind,
                "path": change.path,
                "isDirectory": change.isDirectory,
                "isFile": change.isFile
            }

        return list(map(change_to_dict, client.changes))

    @doc_auth_token(Namespaces.changelist)
    @Namespaces.changelist.expect(Models.change_delete_request)
    def delete(self):
        client = find_client()
        client.delete_changes(request.json["changes"])

        return "OK"


@Namespaces.package.route("")
class Packages(Resource):
    @Namespaces.package.param("id", description="The package ID to retrieve")
    @doc_auth_token(Namespaces.package)
    # @Namespaces.package.marshal_with(Models.package_takeout)
    def get(self):
        client = find_client()

        takeout = dataclasses.asdict(client.create_takeout(request.args["id"]))

        return takeout

    @doc_auth_token(Namespaces.package)
    @Namespaces.package.expect(Models.create_package_request)
    @Namespaces.package.marshal_with(Models.package)
    def post(self):
        client = find_client()
        package = client.create_package(request.json["changes"])

        return {
            "id": package.id
        }

    @doc_auth_token(Namespaces.package)
    @Namespaces.package.expect(Models.delete_package_request)
    def delete(self):
        client = find_client()
        client.delete_package(request.json["packageId"])


def get_tcp_bind(project: Project) -> Tuple[str, int]:
    host = project.serve_config.get("host", "127.0.0.1")
    port = str(project.serve_config.get("port", 8080))
    assert port.isnumeric(), f"The provided port {port} is not numerical"
    port = int(port)

    return host, port


def run(project: Project):
    host, port = get_tcp_bind(project)
    debug = int(os.environ.get("DEBUG", "0").strip()) > 0

    watch_files(project)

    preferred_profile = project.serve_config.get("build_profile", "default")
    project.active_profile = preferred_profile
    build_profile = project.build_profile()

    project_builder.configure(
        project,
        build_profile.builder,
        5
    )

    try:
        app.run(debug=debug, host=host, port=port)

    finally:
        project_builder.stop()
