# -*- coding: utf-8 -*-
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def _get_is_apply(self):
#         commission_based_on = self.env['ir.values'].get_default('sale.config.settings', 'commission_based_on')
        commission_based_on = self.env['ir.config_parameter'].sudo().get_param('sales_commission_external_user.commission_based_on') #odoo11
#         when_to_pay = self.env['ir.values'].get_default('sale.config.settings', 'when_to_pay')
        when_to_pay = self.env['ir.config_parameter'].sudo().get_param('sales_commission_external_user.when_to_pay') #odoo11
        if commission_based_on == 'sales_team' and when_to_pay == 'invoice_payment':
            return True

    @api.multi
    @api.depends('partner_type')
    def _check_partner_type(self):
        for rec in self:
            if rec.partner_type == 'customer':
                rec.sales_commission_apply = True
        
    sales_team_id = fields.Many2one(
        'crm.team',
        string='Sales Team',
        required=False,
    )
#     sales_user_id = fields.Many2one(
#         'res.users',
#         string='Salesperson',
#     )
#     commission_manager_id = fields.Many2one(
#         'sales.commission.line',
#         string='Sales Commission for Manager'
#     )
#     commission_person_id = fields.Many2one(
#         'sales.commission.line',
#         string='Sales Commission for Member'
#     )
    sales_commission_apply = fields.Boolean(
        string='Sales Commission Apply',
        compute='_check_partner_type',
        store=True,
    )
    sale_commission_user_ids = fields.One2many(
        'sale.commission.level.users',
        'payment_id',
        string="Sale Commission User"
    )
    sale_commission_percentage_ids = fields.One2many(
        'sale.commission.level.percentage',
        'account_payment_id',
        string="Sale Commission Level Percentage"
    )
    is_apply = fields.Boolean(
        string='Is Apply ?',
        compute='_compute_is_apply',
        default=_get_is_apply
    )

    @api.multi
    @api.depends()
    def _compute_is_apply(self):
#         commission_based_on = self.env['ir.values'].get_default('sale.config.settings', 'commission_based_on')
        commission_based_on = self.env['ir.config_parameter'].sudo().get_param('sales_commission_external_user.commission_based_on') #odoo11
#         when_to_pay = self.env['ir.values'].get_default('sale.config.settings', 'when_to_pay')
        when_to_pay = self.env['ir.config_parameter'].sudo().get_param('sales_commission_external_user.when_to_pay') #odoo11
        for rec in self:
            if commission_based_on == 'sales_team' and when_to_pay == 'invoice_payment':
                rec.is_apply = True

    @api.multi
    @api.onchange('sales_team_id')
    def sales_team_id_change(self):
        for rec in self:
            sale_commission_percentage = []
            for level in rec.sales_team_id.sale_commission_percentage_ids:
                sale_commission_percentage.append((0,0,{'level_id': level.level_id.id,
                                        'percentage': level.percentage,
                                        'account_payment_id':rec.id}))
            rec.sale_commission_percentage_ids = sale_commission_percentage

    @api.model
    def default_get(self, fields):
        rec = super(AccountPayment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            rec['sales_team_id'] = invoice['team_id'] and invoice['team_id'][0] or False
        return rec

    @api.multi
    @api.onchange('partner_id')
    def partner_id_change(self):
        for rec in self:
            if rec.partner_id:
                sale_commission = []
                for level in rec.partner_id.sale_commission_user_ids:
                    sale_commission.append((0, 0, {'level_id': level.level_id.id,
                                            'user_id': level.user_id.id,
                                            'payment_id':rec.id}))
                rec.sale_commission_user_ids = sale_commission

    @api.multi
    def get_teamwise_commission(self):
        for rec in self:
            if not rec.sales_team_id:
                raise Warning(_('Please select Sales Team.'))
#             if not rec.sales_user_id:
#                 raise Warning(_('Please select Sales User.'))
            
            commission = {}
            for commission_id in rec.sale_commission_percentage_ids:
                for partner in rec.sale_commission_user_ids:
                    if partner.level_id == commission_id.level_id:
                        amount = (rec.amount * commission_id.percentage)/100
                        if partner.user_id not in commission:
                            commission[partner.user_id] = 0.0
                        commission[partner.user_id] += amount
        return commission

    @api.multi
    def create_commission(self, user_commission,commission):
        commission_obj = self.env['sales.commission.line']
        product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
        for user in user_commission:
            for payment in self:
                if user_commission:
                    for sale_commission in commission.commission_user_id:
                        if user.id == sale_commission.id:
                            commission_value = {
                                'commission_user_id': user.id,
                                'amount': user_commission[user],
                                'origin': payment.name,
                                'user_id': user.id,
                                'product_id': product.id,
                                'date' : payment.payment_date,
                                'src_payment_id': payment.id,
                                'sales_commission_id':commission.id,
                            }
                            commission_id = commission_obj.sudo().create(commission_value)
                            payment.commission_person_id = commission_id.id
        return True

    @api.multi
    def create_base_commission(self, user):
        commission_obj = self.env['sales.commission']
        product = self.env['product.product'].search([('is_commission_product','=',1)],limit=1)
        if user:
            for order in self:
                today = date.today()
                first_day = today.replace(day=1)
                last_day = datetime.datetime(today.year,today.month,1)+relativedelta(months=1,days=-1)
                commission_value = {
                        'start_date' : first_day,
                        'end_date': last_day,
                        'product_id':product.id,
                        'commission_user_id': user.id,
                    }
                commission_id = commission_obj.sudo().create(commission_value)
            return commission_id
    
    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
        if self.env.context.get('skip'): #odoo11 skip real_estate_property_app
            return res
#         when_to_pay = self.env['ir.values'].get_default('sale.config.settings', 'when_to_pay')
        when_to_pay = self.env['ir.config_parameter'].sudo().get_param('sales_commission_external_user.when_to_pay') #odoo11
        if  when_to_pay == 'invoice_payment':
            for payment in self:
                if payment.sales_commission_apply:
#                     commission_based_on = self.env['ir.values'].get_default('sale.config.settings', 'commission_based_on')
                    commission_based_on = self.env['ir.config_parameter'].sudo().get_param('sales_commission_external_user.commission_based_on') #odoo11
                    if commission_based_on == 'sales_team':
                        user_commission = payment.get_teamwise_commission()
                    for user in user_commission:
                        commission = self.env['sales.commission'].search([
                            ('commission_user_id', '=', user.id),
                            ('start_date', '<', payment.payment_date),
                            ('end_date', '>', payment.payment_date),
                            ('state','=','draft')],limit=1)
                        if not commission:
                            commission = payment.create_base_commission(user)
                        if  commission:
                            payment.create_commission(user_commission, commission)
        return res

    @api.multi
    def cancel(self):
        res = super(AccountPayment, self).cancel()
        for rec in self:
            lines = commission_obj.sudo().search([('src_payment_id', '=', rec.id)])
            for line in lines:
                if line.state == 'draft' or line.state == 'cancel':
                    line.state = 'exception'
                elif line.state in ('paid', 'invoice'):
                    raise UserError(_('You can not cancel this invoice because sales commission is invoiced/paid. Please cancel related commission lines and try again.'))
            #if rec.commission_manager_id:
             #   rec.commission_manager_id.state = 'exception'
            #if rec.commission_person_id:
             #   rec.commission_person_id.state = 'exception'
        return res
