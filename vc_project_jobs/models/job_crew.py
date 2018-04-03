# -*- coding: utf-8 -*-

from odoo import models, fields, api

class JobCrew(models.Model):
    _name = 'job.crew'
    _description = 'Job Crews'


    name = fields.Char(
        string = 'Crew Name',
        required = True,
    )

    employee_ids = fields.Many2many(
        comodel_name = 'hr.employee',
        string='Employees',
        required=True
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This Crew Name is already in the system! - Please check the Name and try again.')
    ]
