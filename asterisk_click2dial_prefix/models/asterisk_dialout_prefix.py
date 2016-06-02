# -*- coding: utf-8 -*-
# (c) 2016 credativ ltd. - Ondřej Kuzník
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class AsteriskDialoutPrefix(models.Model):
    _name = 'asterisk.dialout.prefix'

    name = fields.Char(required=True)
    prefix = fields.Char()
    server_id = fields.Many2one('asterisk.server', string='Server')
