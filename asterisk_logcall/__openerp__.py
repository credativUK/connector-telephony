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


{
    'name': 'Asterisk Phone Log-call',
    'version': '9.0.0.1.0',
    'category': 'Phone',
    'license': 'AGPL-3',
    'summary': 'Allow a call to be logged in Odoo',
    'description': """
Asterisk Phone Log-call
=================

When a call has completed within Asterisk a callback can be
added in a hangup handler to call an AGI script which sends
a request to Odoo to log the call.
""",
    'author': "credativ Ltd,Odoo Community Association (OCA)",
    'website': 'http://www.credativ.co.uk/',
    'depends': ['base_phone', 'crm_voip'],
    'data': [
      'views/crm_phonecall_view.xml',
    ],
    'images': [],
    'active': False,
}
