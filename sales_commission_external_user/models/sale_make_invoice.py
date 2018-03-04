# -*- coding: utf-8 -*-
from openerp import models, fields, api

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order=order,
                                                                     so_line=so_line,
                                                                     amount=amount)
        if invoice:
            if order.sale_commission_user_ids:
                sale_commission_user_lines = []
                for commission in order.sale_commission_user_ids:
                    sale_commission_user_lines.append((0, 0, {
                        'level_id': commission.level_id.id,
                        'user_id': commission.user_id and commission.user_id.id or False}))
                invoice.write({'sale_commission_user_ids': sale_commission_user_lines})
    
            if order.sale_commission_percentage_ids:
                sale_commission_lines = []
                for commission in order.sale_commission_percentage_ids:
                    sale_commission_lines.append((0, 0, {
                        'level_id': commission.level_id.id,
                        'percentage': commission.percentage}))
                invoice.write({'sale_commission_percentage_ids': sale_commission_lines})
            for line in invoice.invoice_line_ids:
                line._onchange_product_id()
        return invoice
