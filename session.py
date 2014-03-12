# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

from openerp.osv import osv, fields

class Session(osv.Model):
    _name = 'openacademy.session'
    _description = 'Sessions'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'start_date': fields.date(string='Start Date'),
        'duration': fields.float(string='Duration', digits=(6,1),
                                help="Duration in days."),
        'seats': fields.integer(string='Number of Seats'),
        
        # relational fields
        'course': fields.many2one('openacademy.course', string='Course', required=True),
        'instructor': fields.many2one('res.partner', string='Instructor'),
    }
