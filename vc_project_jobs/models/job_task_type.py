# -*- coding: utf-8 -*-

from odoo import models, fields, api

class JobTaskType(models.Model):

    _name = 'job.task.type'
    _description = 'Job Task Types'

    name = fields.Char(
        string = 'Name',
        required = True,
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This Task Type is already in the system! - Please check the Type and try again.')
    ]

