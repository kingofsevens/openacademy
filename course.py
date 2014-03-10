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
    }
