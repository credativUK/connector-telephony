# -*- coding: utf-8 -*-
# (c) 2016 credativ ltd. - Ondřej Kuzník
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields


class AsteriskDialoutPrefixWizard(models.TransientModel):
    _name = 'asterisk.dialout.prefix.wizard'

    prefix = fields.Many2one('asterisk.dialout.prefix')
    phone_number = fields.Char(required=True)
    click2dial_model = fields.Char(required=True)
    click2dial_id = fields.Integer()

    @api.multi
    def click2dial(self):
        self.ensure_one()
        res = self.with_context(asterisk_dialout_prefix=self.prefix)\
            .env['phone.common'].click2dial(self.phone_number)

        if res.get('action_model'):
            return {
                'name': res.get('action_name'),
                'type': 'ir.actions.act_window',
                'res_model': res.get('action_model'),
                'view_mode': 'form',
                'views': [[False, 'form']],
                'target': 'new',
                'context': self.env.context,
            }
