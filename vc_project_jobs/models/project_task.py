# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectTask(models.Model):

    _inherit = 'project.task'

    task_type = fields.Selection(
        string = 'Task Type',
        selection = [('job_pm','Project Management'),('job_labor','Labor'),('job_expenses','Expenses')],
    )



