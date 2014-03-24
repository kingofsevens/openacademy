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

    _sql_constraints = [
    
        ('name_description_check', 
            'CHECK(name <> description)', 
            'The title of the course should be different of the description'),
            
        ('name_unique', 
            'UNIQUE(name)', 
            'Course titles must be distinct.'),
            
    ]

    def copy(self, cr, uid, id, default, context=None):
        # duplicate the course with the given id
        course = self.browse(cr, uid, id, context)
        new_name = "%s (copy)" % course.name
        # use a different name for the copy, and do not duplicate sessions
        default = dict(default, name=new_name, sessions=[])
        return super(Course, self).copy(cr, uid, id, default, context)

