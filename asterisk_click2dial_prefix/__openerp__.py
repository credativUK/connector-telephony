# -*- encoding: utf-8 -*-
##############################################################################
#
#    Asterisk Click2dial module for Odoo 9
#    Copyright (C) 2016 Ondřej Kuzník <ondrej.kuznik@credativ.co.uk>
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

{
    'name': 'Asterisk Click2dial with prefix',
    'version': '9.0.0.1.0',
    'category': 'Phone',
    'license': 'AGPL-3',
    'summary': 'Choose prefix when dialling out',
    'author': 'credativ ltd.',
    'website': 'http://www.credativ.co.uk/',
    'depends': ['asterisk_click2dial'],
    'data': [
        'views/asterisk_dialout_prefix_view.xml',
        'views/asterisk_dialout_prefix_wizard_view.xml',
        'views/web_asterisk_click2dial_prefix.xml',
        'security/ir.model.access.csv',
    ],
    'js': ['static/src/js/*.js'],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'active': False,
}
