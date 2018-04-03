# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class Project(models.Model):

    _inherit = 'project.project'

    # for top level projects
    subscription_project_id = fields.Many2one('project.project', string='Subscription Project', index=True)
    job_project_ids = fields.One2many('project.project', 'subscription_project_id', string='Job Projects', domain=[('active', '=', True)])

    # for job projects
    date_from = fields.Date('Scheduled Start')

    date_to = fields.Date('Scheduled Finish')

    hotel_name = fields.Many2one(
        string = 'Hotel Name',
        comodel_name = 'res.partner',
        domain = [('supplier','=',True)]
    )

    foreman_id = fields.Many2one(
        string = 'Foreman',
        comodel_name = 'hr.employee',
    )

    crew_id = fields.Many2one(
        comodel_name = 'job.crew',
        string = 'Job Crew',
    )

    crew_employees = fields.Many2many(
        comodel_name = 'hr.employee',
        string = 'Crew Members',
        related = 'crew_id.employee_ids',
    )

    job_instructions = fields.Text(
        string = 'Instructions',
    )

    daily_report_ids = fields.One2many('job.daily.report','project_id',string='Daily Reports')
    site_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Site',
        domain = "[('type','=','job')]"
    )

    job_count = fields.Integer(compute='_get_job_count', string="Jobs")

    def _get_job_count(self):
        for project in self:
            project.job_count = len(project.job_project_ids)

    daily_report_count = fields.Integer(compute='_get_daily_report_count', string="Daily Reports")

    def _get_daily_report_count(self):
        for project in self:
            project.daily_report_count = len(project.daily_report_ids)

    @api.multi
    def write(self, vals):

        for project in self:
            # if partner is blank and we have a suscription project as the parent, set the customer to match
            if not project.partner_id and project.subscription_project_id:
                parent_project = self.search([('id','=',project.subscription_project_id.id)])
                vals['partner_id'] = parent_project[0].partner_id.id

        res = super(Project, self).write(vals)

        return res

