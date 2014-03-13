# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

from openerp.osv import osv, fields

class Partner(osv.Model):
    _inherit = 'res.partner'

    _columns = {
        'instructor': fields.boolean('Instructor'),
    }

    _defaults = {
        # By default, no partner is an instructor ’instructor’ : False,
        'instructor': False,
    }