# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    #make sure the Analytic Account is created as a Project each time a subscription is created
    @api.model
    def create(self, vals):
        vals['use_tasks'] = True
        vals['project_type'] = 'subscription'
        return super(SaleSubscription, self).create(vals)

    project_count = fields.Integer(
        string='Project Count',
        related = 'analytic_account_id.project_count')

    project_ids = fields.One2many(
        comodel_name = 'project.project',
        inverse_name = 'analytic_account_id',
        string = 'Projects',
        related = 'analytic_account_id.project_ids' )


    @api.multi
    def action_subscription_projects(self):
        if len(self.project_ids.ids) == 1:
            return {
                "type": "ir.actions.act_window",
                "res_model": "project.project",
                "res_id": self.project_ids.ids[0],
                "domain": [["id", "in", self.project_ids.ids]],
                "views": [[self.env.ref('project.edit_project').id, "form"]],
                "name": "Projects",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "res_model": "project.project",
                "domain": [["id", "in", self.project_ids.ids]],
                "views": [[self.env.ref('project.view_project').id, "tree"],
                      [self.env.ref('project.edit_project').id, "form"]],
                "name": "Projects",
            }



