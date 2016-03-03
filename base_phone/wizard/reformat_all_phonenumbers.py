# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Phone module for Odoo
#    Copyright (C) 2012-2015 Alexis de Lattre <alexis@via.ecp.fr>
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

from openerp import api, fields, models, tools
import logging

logger = logging.getLogger(__name__)


class reformat_all_phonenumbers(models.TransientModel):
    _name = "reformat.all.phonenumbers"
    _inherit = "res.config.installer"
    _description = "Reformat all phone numbers"

    phonenumbers_not_reformatted = fields.Text(
        string="Phone numbers that couldn't be reformatted")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             string='State', default='draft')

    @api.multi
    def run_reformat_all_phonenumbers(self):
        self.ensure_one()
        logger.info('Starting to reformat all the phone numbers')
        phonenumbers_not_reformatted = ''
        phoneobjects = self.env['phone.common']._get_phone_fields()
        for objname in phoneobjects:
            processed = updated = 0
            obj = self.env[objname]
            fields = obj._phone_fields
            logger.info(
                'Starting to reformat phone numbers on object %s '
                '(fields = %s)' % (objname, fields))
            # search if this object has an 'active' field
            domain = []
            if obj._fields.get('active'):
                domain += ['|', ('active', '=', True), ('active', '=', False)]
            ids = obj.search(domain)._ids
            try:
                new_cr = self.env.registry.cursor()
                env = api.Environment(new_cr, self.env.uid, self.env.context)
                obj = env[objname]
                while ids:
                    updated_uncommitted = processed_uncommitted = 0
                    current, ids = ids[:100], ids[100:]
                    for entry in obj.browse(current):
                        def strip_displayname(value):
                            """read returns (id, diplay_name) on many2one"""
                            return value[0] if isinstance(value, tuple) else value

                        orig_vals = entry.read()[0]
                        orig_vals = {key: strip_displayname(value)
                                     for key, value in orig_vals.iteritems()}
                        vals = orig_vals.copy()

                        try:
                            entry.with_context(raise_if_phone_parse_fails=True).\
                                _generic_reformat_phonenumbers(vals)
                        except Exception, e:
                            name = entry.name_get()[0][1]
                            logger.exception("Problem on %s '%s'" %
                                (obj._description, name))
                            phonenumbers_not_reformatted += \
                                "Problem on %s '%s'. Error message: %s\n" % (
                                    obj._description, name, tools.ustr(e))
                            continue

                        updates = {field: vals.get(field) for field in fields
                                if orig_vals.get(field) != vals.get(field)}
                        if updates:
                            logger.info(
                                '[%s] Reformating phone number: FROM %s TO %s' % (
                                    obj._description,
                                    tools.ustr({key: orig_vals.get(key) for key in updates}),
                                    tools.ustr(updates)))
                            entry.write(updates)
                            updated_uncommitted += 1
                        processed_uncommitted += 1
                    updated += updated_uncommitted
                    processed += processed_uncommitted
                    logger.info(
                        '[%s] Committing changes: %d/%d records updated, %d remain' % (
                            obj._description, updated_uncommitted, processed_uncommitted, len(ids)))
                    new_cr.commit()
                logger.info(
                    '[%s] Finished: %d records processed, %d records updated' % (
                        obj._description, processed, updated))
            except Exception, e:
                phonenumbers_not_reformatted += "Processing model '%s' failed\n" % objname
                logger.exception("Reformatting on model '%s' failed, processed %d records with %d updates" % (objname, processed, updated))
                new_cr.rollback()
            finally:
                new_cr.close()
        if not phonenumbers_not_reformatted:
            phonenumbers_not_reformatted = \
                'All phone numbers have been reformatted successfully.'
        self.write({
            'phonenumbers_not_reformatted': phonenumbers_not_reformatted,
            'state': 'done'})
        logger.info('End of the phone number reformatting wizard')
        action = self.env['ir.actions.act_window'].for_xml_id(
            'base_phone', 'reformat_all_phonenumbers_action')
        action['res_id'] = self.id
        return action
