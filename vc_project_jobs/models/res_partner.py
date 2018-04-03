# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):

    _inherit = 'res.partner'

    county_id = fields.Many2one(
        string = 'County',
        comodel_name = 'res.state.county',
        required = False,
        help = 'County, Borough, Census Area or Parish',
    )

    type = fields.Selection(selection_add=[('job', 'Job Site Address')])

