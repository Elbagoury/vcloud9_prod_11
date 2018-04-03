# -*- coding: utf-8 -*-

from odoo import models, fields, api

class JobPrevailingWage(models.Model):

    _description='Job Prevailing Wages'
    _name = 'job.prevailing.wage'
    _order = 'county_id, job_class_id'


    county_id = fields.Many2one(
        comodel_name = 'res.state.county',
        required = True,
    )

    job_class_id = fields.Many2one(
        comodel_name = 'job.class',
        required= True,
    )

    start_date = fields.Date(
        string = 'Starts'
    )

    end_date = fields.Date(
        string = 'Finishes'
    )

    wage = fields.Float(
        string = 'Wage',
        required = True,
    )

    benefit = fields.Float(
        string = 'Benefit',
        required = True,
    )

    pw_total = fields.Float(
        string = 'Total',
        compute='_update_total'
    )


    @api.multi
    def _update_total(self):
        for rec in self:
            rec.pw_total = rec.wage + rec.benefit

    @api.one
    @api.constrains('county_id','job_class_id','start_date','end_date')
    def _check_overlap(self):
        existing_entries = 1
        if existing_entries == 0:
            raise ValidationError("There is already an entry for this Job Class during these dates:")
            #show the line

