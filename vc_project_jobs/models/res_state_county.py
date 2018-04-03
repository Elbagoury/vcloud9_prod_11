# -*- coding: utf-8 -*-

from odoo import models, fields, api

class County(models.Model):

    _description='State Counties'
    _name = 'res.state.county'

    # Used to store US Counties
    # Data sourced originally on 9/9/2017 from
    # https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt
    # At that time the longest county name in the country was:
    # Prince of Wales-Hyder Census Area (33 Characters)

    name = fields.Char(
        string='County',
        size=45,
        required=True,
        help='County, Borough, Census Area or Parish',
    )

    state_id = fields.Many2one(
        string = 'State',
        comodel_name = 'res.country.state',
        required = True,
        help = 'State, Territory or Commonwealth',
    )

    state_code = fields.Char(
        string = 'State Code',
        help = 'The state code.',
        related = 'state_id.code',
    )


    _order = 'state_code,name'

