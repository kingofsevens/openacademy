# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

from openerp.osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

class Subscribe(osv.TransientModel):
    _name = 'openacademy.subscribe'

    _columns = {
        'session': fields.many2one('openacademy.session', string='Session', required=True),
        'attendees': fields.many2many('res.partner', string='Attendees'),
    }
