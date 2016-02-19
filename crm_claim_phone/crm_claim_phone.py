# -*- encoding: utf-8 -*-
##############################################################################
#
#    CRM Claim Phone module for Odoo/OpenERP
#    Copyright (c) 2012-2014 Akretion (http://www.akretion.com)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import models, api


class CrmClaim(models.Model):
    _name = 'crm.claim'
    _inherit = ['crm.claim', 'phone.common']
    _phone_fields = ['partner_phone']
    _country_field = None
    _partner_field = 'partner_id'

    @api.model
    def create(self, vals):
        vals_reformatted = self._generic_reformat_phonenumbers(vals)
        return super(CrmClaim, self).create(vals_reformatted)

    @api.multi
    def write(self, vals):
        vals_reformatted = self._generic_reformat_phonenumbers(vals)
        return super(CrmClaim, self).write(vals_reformatted)
