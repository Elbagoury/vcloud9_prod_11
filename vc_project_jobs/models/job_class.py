# -*- coding: utf-8 -*-

from odoo import models, fields, api

class JobClass(models.Model):

    _name = 'job.class'
    _description = 'Job Classes'

    name = fields.Char(
        string = 'Class',
        required = True,
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This Job Class is already in the system! - Please check the Class and try again.')
    ]

