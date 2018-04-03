# -*- coding: utf-8 -*-
from odoo import http

# class Scaffold(http.Controller):
#     @http.route('/scaffold/scaffold/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scaffold/scaffold/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('scaffold.listing', {
#             'root': '/scaffold/scaffold',
#             'objects': http.request.env['scaffold.scaffold'].search([]),
#         })

#     @http.route('/scaffold/scaffold/objects/<model("scaffold.scaffold"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scaffold.object', {
#             'object': obj
#         })