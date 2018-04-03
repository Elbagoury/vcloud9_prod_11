# -*- coding: utf-8 -*-

from odoo import models, fields, api

class JobWeatherType(models.Model):

    _name = 'job.weather.type'
    _description = 'Job Weather Types'

    name = fields.Char(
        string = 'Type',
        required = True,
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This Weather Type is already in the system! - Please check the Type and try again.')
    ]
