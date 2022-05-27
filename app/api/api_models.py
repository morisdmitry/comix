from flask_restx import fields
from app.api import api


error_message_model = api.model(
    "ErrorMessageModel",
    {
        "error_message": fields.String(
            required=True, description="Error message", example="error message example"
        ),
    },
)

comix_el_params_model = api.model(
    "ComixElParamsModel",
    {
        "url": fields.String(required=True, example="/src/932/390.png"),
        "size": fields.Integer(required=True, example=20),
        "rotate": fields.String(required=True, example="-80"),
    },
)

comix_element_coords = api.model(
    "ComixElementCoords",
    {
        "axis_x": fields.Integer(required=True, example=192),
        "axis_y": fields.Integer(required=True, example=168),
    },
)

comix_elements_model = api.model(
    "ComixElementsModel",
    {
        "id": fields.Integer(required=True, example=1),
        "type": fields.String(required=True, example="image"),
        "coordinates": fields.Nested(comix_element_coords),
        "params": fields.Nested(comix_el_params_model),
    },
)

comix_page_model = api.model(
    "ComixPageModel",
    {
        "comix_id": fields.Integer(required=False, example=1),
        "elements": fields.Nested(comix_elements_model),
    },
)

comix_page_model_full = api.model(
    "ComixPageModelFull",
    {
        "id": fields.Integer(required=True, example=1),
        "description": fields.String(required=False, example="text of description"),
        "elements": fields.Nested(comix_elements_model),
    },
)


autor_model = api.model(
    "Autor",
    {
        "first_name": fields.String(required=False, example="John"),
        "last_name": fields.String(required=False, example="Doe"),
    },
)

comix_model = api.model(
    "Comix",
    {
        "autor_id": fields.Integer(required=False, example=1),
        "description": fields.String(required=False, example="describe your comix"),
    },
)
