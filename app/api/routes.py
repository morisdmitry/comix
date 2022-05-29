import json
import werkzeug
from app.api import api

from flask import make_response, request
from flask_restx import Resource, reqparse
from app import db
from app.api.utils import ImageHandler, response_bad, response_ok, response_error
from app.database.models import Autor, Comix, ComixPages
from app.api.api_models import (
    comix_page_model,
    comix_page_model_full,
    autor_model,
    comix_model,
    error_message_model,
)

autor_ns = api.namespace("autor", description="autor crud")
comix_ns = api.namespace("comix", description="comix crud")
comix_pages_ns = api.namespace("comix_page", description="comix pages crud")
upload_image_ns = api.namespace(
    "upload_image", description="upload image to local storage"
)


@autor_ns.route("/")
class AutorCRUD(Resource):
    @api.response(200, "OK")
    def get(self):
        try:
            autors = Autor.query.all()
            if not autors:
                return make_response(response_error("autors not found", 404))
            result = {
                "autors": [
                    {
                        "id": autor.id,
                        "first_name": autor.first_name,
                    }
                    for autor in autors
                ]
            }

            response = make_response(response_ok(result, 200))

        except Exception as e:
            response = make_response(response_bad(e, 500))

        return response

    @api.response(200, "OK")
    @api.doc(body=autor_model)
    def post(self):
        body = request.get_json()
        try:
            autor = Autor(first_name=body["first_name"], last_name=body["last_name"])
            if not autor:
                return make_response(json.dumps({"error": "autor not created"}))
            db.session.add(autor)
            db.session.commit()

            result = {
                "autor created": {
                    "id": autor.id,
                    "first_name": autor.first_name,
                    "last_name": autor.last_name,
                }
            }

            response = make_response(response_ok(result, 200))
        except Exception as e:
            response = make_response(response_bad(e, 500))

        return response


@comix_ns.route("/")
@api.response(500, "Error", error_message_model)
class ComixCRUD(Resource):
    @api.response(200, "OK")
    def get(self):
        try:
            comixes = Comix.query.all()
            if not comixes:
                return make_response(response_error("comixes not found", 404))
            result = {
                "comixes": [
                    {
                        "id": comix.id,
                        "created_at": str(comix.datetime),
                        "autor_id": comix.autor_id,
                        "description": comix.description,
                    }
                    for comix in comixes
                ]
            }

            response = make_response(response_ok(result, 200))
        except Exception as e:
            response = make_response(response_bad(e, 500))

        return response

    @api.response(200, "OK")
    @api.doc(body=comix_model)
    def post(self):
        body = request.get_json()
        try:

            comix = Comix(description=body["description"], autor_id=body["autor_id"])
            if not comix:
                return make_response(json.dumps({"error": "comix not created"}))
            db.session.add(comix)
            db.session.commit()

            result = {
                "comix": {
                    "id": comix.id,
                    "autor": comix.autor_id,
                    "datetime": str(comix.datetime),
                    "description": comix.description,
                }
            }
            response = make_response(response_ok(result, 200))
        except Exception as e:
            response = make_response(response_bad(e, 500))

        return response


@comix_pages_ns.route("/<int:comix_id>")
class ComixPageCRUDId(Resource):
    @api.response(200, "OK")
    def get(self, comix_id):
        try:
            comix_pages = ComixPages.query.filter(
                ComixPages.comix_id == comix_id
            ).first()
            if not comix_pages:
                return make_response(response_error("comix pages not found", 404))
            result = {
                "comix page": {
                    "id": comix_pages.id,
                    "params": comix_pages.params,
                    "elements": comix_pages.elements,
                    "comix_id": comix_pages.comix_id,
                }
            }

            response = make_response(response_ok(result, 200))
        except Exception as e:
            response = make_response(response_bad(e, 500))
        return response


@comix_pages_ns.route("/")
class ComixPageCRUD(Resource):
    @api.response(200, "OK", comix_page_model_full)
    @api.doc(body=comix_page_model)
    @api.expect(body=comix_page_model)
    def post(self):
        body = request.get_json()
        try:

            comix_page = ComixPages.query.filter(
                ComixPages.comix_id == body["comix_id"]
            ).first()
            if comix_page:
                return make_response(response_error("comix pages already exixts", 409))

            comix_page = ComixPages(
                elements=body["elements"],
                comix_id=body["comix_id"],
            )

            if not comix_page:
                return make_response(response_error("bad save comix page", 400))
            db.session.add(comix_page)
            db.session.commit()

            result = {
                "comix_page": {
                    "id": comix_page.id,
                    "comix_id": comix_page.comix_id,
                    "elements": comix_page.elements,
                }
            }

            response = make_response(response_ok(result, 200))
        except Exception as e:
            response = make_response(response_bad(e, 500))

        return response


@upload_image_ns.route("/")
class UploadImage(Resource):

    file_upload = reqparse.RequestParser()
    file_upload.add_argument(
        "file",
        type=werkzeug.datastructures.FileStorage,
        location="files",
    )
    file_upload.add_argument("page_id", type=int, required=True)

    @api.response(200, "OK")
    @api.doc(file_upload)
    @api.expect(file_upload)
    def post(self):
        try:
            file = request.files.get("file", None)
            page_id = request.args.get("page_id")
            if not file or not page_id:
                return make_response(response_error("bad file upload", 400))

            image = ImageHandler(file)
            filename = image.generate_filename()
            if not filename:
                return make_response(response_error("bad creating filename", 400))

            error = image.save_file(filename)
            if error:
                return make_response(response_error(error, 400))

            result = {"filename": filename}
            response = make_response(response_ok(result, 200))
        except Exception as e:
            response = make_response(response_bad(e, 500))
        return response
