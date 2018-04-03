# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression

class JobCostCode(models.Model):

    _name = 'job.cost.code'
    _description = 'Job Cost Codes'
    _order = 'code'

    code = fields.Char(
        string = 'Code',
        size=8,
        required = True,
        help = 'Cost Code Reference',
    )

    name = fields.Char(
        string = 'Description',
        required = True,
        help = 'Cost Code Reference',
    )

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        cost_codes = self.search(domain + args, limit=limit)
        return cost_codes.name_get()

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for rec in self:
            name = rec.code + ' - ' + rec.name
            result.append((rec.id, name))
        return result

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'This Cost Code is already in the system! - Please check the Code and try again.')
    ]
