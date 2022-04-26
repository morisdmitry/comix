from datetime import datetime

from sqlalchemy import and_
from app.api import api

from flask import make_response, request
from flask_restx import Resource
from app import db
from app.database.models import Comix, ComixPages
from app.api.api_models import comix_page_model, comix_page_model_full

comix_ns = api.namespace('comix', description='comix crud')
comix_pages_ns = api.namespace('comix_page', description='comix pages crud')

@comix_ns.route('/')
class ComixCRUD(Resource):

    @api.response(200, 'OK')
    def get(self):
        comix = Comix.query.first()
        print('comix', comix)
        return comix.id

    @api.response(200, 'OK')
    def post(self):
        comix = Comix(datetime=datetime.now(), description='desc_hi', autor='autor test')
        db.session.add(comix)
        db.session.commit()

        response_data = {
            'autor': comix.autor,
            'datetime': comix.datetime,

        }

        return make_response({'created': response_data}, 200, {'Content-Type': 'application/json'})

@comix_pages_ns.route('/')
class ComixCRUD(Resource):

    @api.response(200, 'OK')
    def get(self):
        # comix_page = ComixPages.query.order_by(ComixPages.id.desc()).first()
        first = 1
        last = 3
        comix_pages = ComixPages.query.filter(and_(
            ComixPages.id >= first,
            ComixPages.id <= last
        )).all()
        print('comix_pages', comix_pages)

        test = {
            '1':{
                'element_1': {
                    'type': 'text',
                    'coordinates': '192.168',
                    'params': {
                        'width': 30,
                        'heigh': 80,
                    },
                    'data': 'hi, how are you?'
                },
                'element_2': {
                    'type': 'text',
                    'coordinates': '152.100',
                    'params': {
                        'width': 30,
                        'heigh': 80,
                    },
                    'data': 'uuid  of img'
                },
            }
        }


        res = [{i.id: i.description} for i in comix_pages]
        response_data = res
        return make_response({'created': response_data}, 200, {'Content-Type': 'application/json'})

    @api.response(200, 'OK', comix_page_model_full)
    @api.doc(body=comix_page_model)
    @api.expect(body=comix_page_model)
    def post(self):

        data = request.get_json()
        desc = data['description']
        els = data['elements']

        comix_page = ComixPages(description=desc, elements=els)
        db.session.add(comix_page)
        db.session.commit()

        response_data = {
            'id': comix_page.id,
            'description': comix_page.description,
            'elements': comix_page.elements,

        }

        return make_response({'created': response_data}, 200, {'Content-Type': 'application/json'})