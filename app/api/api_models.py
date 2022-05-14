from flask_restx import fields
from app.api import api


error_message_model = api.model('ErrorMessageModel', {
    'error_message': fields.String(required=True, description='Error message', example="error message example"),
})

comix_el_params_model = api.model('ComixElParamsModel', {
    'width': fields.Integer(required=True, example=30),
    'height': fields.Integer(required=True, example=80),
})

comix_elements_model = api.model('ComixElementsModel', {
    'type': fields.String(required=False, example='text'),
    'coordinates': fields.String(required=False, example='192.168'),
    'params': fields.Nested(comix_el_params_model)
})

comix_page_model = api.model('ComixPageModel', {
    'comix_id': fields.Integer(required=False, example=1),
    'description': fields.String(required=False, example='text of description'),
    'elements': fields.Nested(comix_elements_model),
})

comix_page_model_full = api.model('ComixPageModelFull', {
    'id': fields.Integer(required=True, example=1),
    'description': fields.String(required=False, example='text of description'),
    'elements': fields.Nested(comix_elements_model)
})


autor_model = api.model('Autor', {
    'first_name': fields.String(required=False, example='John'),
    'last_name': fields.String(required=False, example='Doe'),
})

comix_model = api.model('Comix', {
    'autor_id': fields.Integer(required=False, example=1),
    'description': fields.String(required=False, example='describe your comix'),
})