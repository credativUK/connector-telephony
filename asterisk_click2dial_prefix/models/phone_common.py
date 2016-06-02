# -*- coding: utf-8 -*-
# (c) 2016 credativ ltd. - Ondřej Kuzník
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class PhoneCommon(models.AbstractModel):
    _inherit = 'phone.common'

    @api.model
    def _transform_number(self, ast_server, ast_number):
        ast_number = super(PhoneCommon, self)._transform_number(ast_server, ast_number)
        prefix = self.env.context.get('asterisk_dialout_prefix')
        if prefix:
            ast_number = "%s%s" % (prefix.prefix, ast_number)
        return ast_number
