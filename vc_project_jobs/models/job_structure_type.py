# -*- coding: utf-8 -*-

from odoo import models, fields, api

class JobStructureType(models.Model):

    _name = 'job.structure.type'
    _description = 'Job Structure Types'

    name = fields.Char(
        string = 'Type',
        required = True,
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This Structure Type is already in the system! - Please check the Type and try again.')
    ]

