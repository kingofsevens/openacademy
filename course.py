# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

from openerp.osv import osv, fields

class Course(osv.Model):
    _name = 'openacademy.course'
    _description = 'Courses'

    _columns = {
        'name': fields.char(string='Title', required=True),
        'description': fields.text(string='Description'),
        
        # relational fields
        'responsible': fields.many2one('res.users', 
            # ’set null’ will reset responsible_id to
            # undefined if responsible was deleted
            ondelete='set null', string='Responsible'),
        # A one2many is the inverse link of a many2one    
        'sessions': fields.one2many('openacademy.session', 'course', string='Sessions'),
    }
