from datetime import datetime
import json

from sqlalchemy import and_
from app.api import api

from flask import make_response, request
from flask_restx import Resource
from app import db
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


@autor_ns.route("/")
class AutorCRUD(Resource):
    @api.response(200, "OK")
    def get(self):
        try:
            autors = Autor.query.all()
            if not autors:
                return make_response(
                    json.dumps({"error": "autors not exist"}),
                    404,
                    {"Content-Type": "application/"},
                )
            result = [
                {
                    "id": autor.id,
                    "first_name": autor.first_name,
                }
                for autor in autors
            ]

            response = make_response(
                json.dumps({"data": result}), 200, {"Content-Type": "application/json"}
            )
        except Exception as e:
            response = make_response(
                json.dumps({"error": getattr(e, "message", str(e))}),
                500,
                {"Content-Type": "application/"},
            )

        return response

    @api.response(200, "OK")
    @api.doc(body=autor_model)
    def post(self):
        body = request.get_json()
        try:
            autor = Autor(first_name=body["first_name"], last_name=body["last_name"])
            db.session.add(autor)
            db.session.commit()

            response_data = {
                "id": autor.id,
                "first_name": autor.first_name,
                "last_name": autor.last_name,
            }

            response = make_response(
                json.dumps({"created": response_data}),
                200,
                {"Content-Type": "application/json"},
            )
        except Exception as e:
            response = make_response(
                json.dumps({"error": getattr(e, "message", str(e))}),
                500,
                {"Content-Type": "application/"},
            )

        return response


@comix_ns.route("/")
@api.response(500, "Error", error_message_model)
class ComixCRUD(Resource):
    @api.response(200, "OK")
    def get(self):
        try:
            comixes = Comix.query.all()
            result = [
                {
                    "id": comix.id,
                    "first_name": comix.first_name,
                }
                for comix in comixes
            ]

            response = make_response(
                json.dumps({"data": result}), 200, {"Content-Type": "application/json"}
            )
        except Exception as e:
            response = make_response(
                json.dumps({"error": getattr(e, "message", str(e))}),
                500,
                {"Content-Type": "application/"},
            )

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

            response_data = {
                "autor": comix.autor_id,
                "datetime": str(comix.datetime),
                "description": comix.description,
            }
            response = make_response(
                json.dumps({"created": response_data}),
                200,
                {"Content-Type": "application/json"},
            )
        except Exception as e:
            response = make_response(
                json.dumps({"error": getattr(e, "message", str(e))}),
                500,
                {"Content-Type": "application/"},
            )

        return response


@comix_pages_ns.route("/<int:comix_id>")
class ComixCRUDId(Resource):
    @api.response(200, "OK")
    def get(self, comix_id):
        comix_pages = ComixPages.query.filter(ComixPages.comix_id == comix_id).first()
        if not comix_pages:
            return make_response(
                json.dumps({"error": "comix pages not found"}),
                404,
                {"Content-Type": "application/"},
            )
        response = {
            "id": comix_pages.id,
            "description": comix_pages.description,
            "elements": comix_pages.elements,
            "comix_id": comix_pages.comix_id,
        }
        return make_response(
            {"created": response}, 200, {"Content-Type": "application/json"}
        )


@comix_pages_ns.route("/")
class ComixCRUD(Resource):
    @api.response(200, "OK", comix_page_model_full)
    @api.doc(body=comix_page_model)
    @api.expect(body=comix_page_model)
    def post(self):
        body = request.get_json()
        try:

            comix_page = ComixPages(
                description=body["description"],
                elements=body["elements"],
                comix_id=body["comix_id"],
            )
            db.session.add(comix_page)
            db.session.commit()

            response_data = {
                "id": comix_page.id,
                "description": comix_page.description,
                "elements": comix_page.elements,
            }

            response = make_response(
                json.dumps({"created": response_data}),
                200,
                {"Content-Type": "application/json"},
            )
        except Exception as e:
            response = make_response(
                json.dumps({"error": getattr(e, "message", str(e))}),
                500,
                {"Content-Type": "application/"},
            )

        return response
