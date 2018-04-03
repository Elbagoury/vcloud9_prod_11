# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    project_type = fields.Selection(
        string = 'Project Type',
        selection = [('template','Template'),('subscription','Subscription'),('job','Job')],
    )

