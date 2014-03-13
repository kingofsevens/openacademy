# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

from openerp.osv import osv, fields

class Session(osv.Model):
    _name = 'openacademy.session'
    _description = 'Sessions'
    _order = 'start_date'
    
    _columns = {
        'name': fields.char(string='Name', required=True),
        'start_date': fields.date(string='Start Date'),
        'duration': fields.float(string='Duration', digits=(6,1),
                                help="Duration in days."),
        'seats': fields.integer(string='Number of Seats'),
        
        # relational fields
        'course': fields.many2one('openacademy.course', 
                # ’cascade’ will destroy session if course_id was deleted
                ondelete='cascade', string='Course', required=True),
        'instructor': fields.many2one('res.partner', string='Instructor'),
        'attendees': fields.many2many('res.partner', string='Attendees'),
    }
