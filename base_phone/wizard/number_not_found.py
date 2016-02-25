# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Phone module for Odoo
#    Copyright (C) 2010-2015 Alexis de Lattre <alexis@via.ecp.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import logging
import phonenumbers

_logger = logging.getLogger(__name__)


class NumberNotFound(models.TransientModel):
    _name = "number.not.found"
    _description = "Number not found"

    caller_name = fields.Char(
        'Caller ID', size=64, readonly=True,
        help="Called ID name obtained from the telephony server")
    calling_number = fields.Char(
        'Calling Number', size=64, readonly=True,
        help="Phone number of calling party that has been obtained "
        "from the telephony server, in the format used by the "
        "telephony server (not E.164).")
    e164_number = fields.Char(
        'E.164 Number', size=64,
        help="E.164 equivalent of the calling number.")
    number_type = fields.Selection(
        [('phone', 'Fixed'), ('mobile', 'Mobile')],
        'Fixed/Mobile', required=True)
    to_update_partner_id = fields.Many2one(
        'res.partner', 'Partner to Update',
        help="Partner on which the phone number will be written")
    current_partner_phone = fields.Char(
        related='to_update_partner_id.phone', string='Current Phone',
        readonly=True)
    current_partner_mobile = fields.Char(
        related='to_update_partner_id.mobile', string='Current Mobile',
        readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super(NumberNotFound, self).default_get(fields_list) or {}
        if res.get('calling_number'):
            convert = self.env['res.partner']._generic_reformat_phonenumbers(
                {'phone': res.get('calling_number')})
            parsed_num = phonenumbers.parse(convert.get('phone'))
            res['e164_number'] = phonenumbers.format_number(
                parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            number_type = phonenumbers.number_type(parsed_num)
            if number_type == 1:
                res['number_type'] = 'mobile'
            else:
                res['number_type'] = 'phone'
        return res

    @api.multi
    def create_partner(self):
        '''Function called by the related button of the wizard'''
        self.ensure_one()
        parsed_num = phonenumbers.parse(self.e164_number, None)
        phonenumbers.number_type(parsed_num)

        action = {
            'name': _('Create New Partner'),
            'view_mode': 'form,tree,kanban',
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'nodestroy': False,
            'target': 'current',
            'context': {'default_%s' % self.number_type: self.e164_number,
                        'default_name': self.caller_name,},
        }
        return action

    @api.multi
    def update_partner(self):
        self.ensure_one()
        if not self.to_update_partner_id:
            raise ValidationError(_("Select the Partner to Update."))
        self.to_update_partner_id.write({self.number_type: self.e164_number})
        action = {
            'name': _('Partner: %s') % self.to_update_partner_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form,tree,kanban',
            'nodestroy': False,
            'target': 'current',
            'res_id': self.to_update_partner_id.id,
            'context': self.env.context,
        }
        return action

    @api.model
    def onchange_to_update_partner(self, ids, to_update_partner_id):
        res = {'value': {}}
        if to_update_partner_id:
            to_update_partner = self.env['res.partner'].browse(to_update_partner_id)
            res['value'].update({
                'current_partner_phone': to_update_partner.phone,
                'current_partner_mobile': to_update_partner.mobile,
                })
        else:
            res['value'].update({
                'current_partner_phone': False,
                'current_partner_mobile': False,
                })
        return res
