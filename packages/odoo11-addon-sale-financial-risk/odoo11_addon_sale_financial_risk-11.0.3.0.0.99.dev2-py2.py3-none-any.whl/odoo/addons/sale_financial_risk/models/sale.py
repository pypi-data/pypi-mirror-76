# Copyright 2016-2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo import _, api, fields, models
from odoo.tools import float_round
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        if not self.env.context.get('bypass_risk', False):
            partner = self.partner_id.commercial_partner_id
            exception_msg = ""
            risk_amount = self.currency_id.with_context(
                date=self.confirmation_date and
                datetime.strptime(
                    self.confirmation_date,
                    DEFAULT_SERVER_DATETIME_FORMAT).date()
                or fields.Date.context_today(self)).compute(
                self.amount_total,
                partner.risk_currency_id, round=False,
            )
            if partner.risk_exception:
                exception_msg = _("Financial risk exceeded.\n")
            elif partner.risk_sale_order_limit and (
                    (partner.risk_sale_order + risk_amount) >
                    partner.risk_sale_order_limit):
                exception_msg = _(
                    "This sale order exceeds the sales orders risk.\n")
            elif partner.risk_sale_order_include and (
                    (partner.risk_total + risk_amount) >
                    partner.credit_limit):
                exception_msg = _(
                    "This sale order exceeds the financial risk.\n")
            if exception_msg:
                return self.env['partner.risk.exceeded.wiz'].create({
                    'exception_msg': exception_msg,
                    'partner_id': partner.id,
                    'origin_reference': '%s,%s' % ('sale.order', self.id),
                    'continue_method': 'action_confirm',
                }).action_show()
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='company_id.currency_id',
        string="Company Currency",
        readonly=True,
    )
    risk_amount = fields.Monetary(
        string="Risk amount",
        compute='_compute_risk_amount',
        compute_sudo=True,
        currency_field="company_currency_id",
        store=True
    )
    # TODO: Analyze performance vs order_id.partner_id.commercial_partner_id
    commercial_partner_id = fields.Many2one(
        related='order_partner_id.commercial_partner_id',
        string='Commercial Entity',
        store=True,
        index=True,
        readonly=True,
    )

    @api.depends('state',
                 'price_reduce_taxinc',
                 'qty_delivered',
                 'product_uom_qty',
                 'qty_invoiced')
    def _compute_risk_amount(self):
        for line in self:
            if line.state != 'sale':
                continue
            qty = line.product_uom_qty
            if line.product_id.invoice_policy == 'delivery':
                qty = max(qty, line.qty_delivered)
            risk_qty = float_round(
                qty - line.qty_invoiced,
                precision_rounding=line.product_uom.rounding)
            # There is no risk if the line hasn't stock moves to deliver
            # Added hasattr condition because fails in post-migration compute
            if risk_qty and hasattr(line, 'move_ids'):
                if not line.move_ids.filtered(
                        lambda move: move.state not in ('done', 'cancel')):
                    risk_qty = line.qty_to_invoice
            if risk_qty == 0.0:
                continue
            if line.product_uom_qty:
                # This method has more precision that using price_reduce_taxinc
                risk_amount = line.price_total * (
                    risk_qty / line.product_uom_qty)
            else:
                risk_amount = line.price_reduce_taxinc * risk_qty
            line.risk_amount = line.order_id.currency_id.with_context(
                date=line.order_id.confirmation_date and
                datetime.strptime(
                    line.order_id.confirmation_date,
                    DEFAULT_SERVER_DATETIME_FORMAT).date()
                or fields.Date.context_today(self)).compute(
                risk_amount, line.company_id.currency_id, round=False)
