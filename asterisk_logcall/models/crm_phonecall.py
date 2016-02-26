# -*- coding: utf-8 -*-
##############################################################################
#
#    Asterisk Phone Log-call module for Odoo/OpenERP
#    Copyright (C) 2016 credativ Ltd (<http://credativ.co.uk>).
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

from openerp import _, api, models, fields
from datetime import datetime
from time import mktime
import logging


logger = logging.getLogger(__name__)

class CrmPhonecall(models.Model):
    _inherit = "crm.phonecall"

    recording_id = fields.Many2one('ir.attachment', string='Call Recording', readonly=True,)

class PhoneCommon(models.AbstractModel):
    _inherit = 'phone.common'

    @api.model
    @api.returns('crm.phonecall')
    def log_call_and_recording(self, odoo_type, odoo_src, odoo_dst, odoo_duration, odoo_start, odoo_filename, odoo_uniqueid):
        phonecall_obj = self.env['crm.phonecall']
        users_obj = self.env['res.users']
        attach_obj = self.env['ir.attachment']

        start_date = datetime.strptime(odoo_start, '%Y-%m-%d %H:%M:%S')
        start_time = mktime(start_date.timetuple())

        caller_user, caller_external = odoo_type == 'incoming' and (odoo_dst, odoo_src) or (odoo_src, odoo_dst)

        call_name_prefix = odoo_type == 'incoming' and "Call from %s" or "Call to %s"

        phonecall_data = {
                'partner_phone': caller_external,
                'name': call_name_prefix % (caller_external,),
                'opportunity_id': False,
                'partner_id': False,
                'duration': int(odoo_duration) / 60.0,
                'state': 'done',
                'start_time': start_time,
                'date': odoo_start,
            }

        r = self.get_record_from_phone_number(caller_external)
        if r[0] == 'res.partner':
            phonecall_data['partner_id'] = r[1]
            if r[2]:
                phonecall_data['name'] = call_name_prefix % (r[2],)
        elif r[0] == 'crm.lead':
            phonecall_data['opportunity_id'] = r[1]
            if r[2]:
                phonecall_data['name'] = call_name_prefix % (r[2],)
        record = self.env[r[0]].browse(r[1])

        users = users_obj.search([('internal_number', '=', caller_user)])
        if users:
            phonecall_data['user_id'] = users._ids[0]

        phonecall_id = phonecall_obj.create(phonecall_data)

        if odoo_filename:
            params = self.env['ir.config_parameter']
            base_url = params.get_param('crm.voip.ucp_url', default='')
            if base_url:
                ir_attachment_data = {
                        'res_model': 'crm.phonecall',
                        'res_id': phonecall_id.id,
                        'name': phonecall_data['name'],
                        'type': 'url',
                        'mimetype': 'audio/wav',
                        'url': base_url.format(
                            caller_user=caller_user,
                            odoo_uniqueid=odoo_uniqueid.replace('.', '_'),
                            odoo_filename=odoo_filename),
                        'datas_fname': odoo_filename,
                    }
                attach_id = attach_obj.create(ir_attachment_data)
                phonecall_id.write({'recording_id': attach_id.id})

                message_format = _("Recorded %s call (%%sm)." % odoo_type)
                record.message_post(
                    body=message_format % (int(odoo_duration) / 60,),
                    message_type='comment',
                    attachment_ids=attach_id._ids)

        return phonecall_id
