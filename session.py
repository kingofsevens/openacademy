# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

from openerp.osv import osv, fields

class Session(osv.Model):
    _name = 'openacademy.session'
    _description = 'Sessions'
    _order = 'start_date'

    def _get_completion(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for session in self.browse(cr, uid, ids, context):
            if session.seats:
                res[session.id] = 100.0 * len(session.attendees) / session.seats
            else:
                res[session.id] = 0.0
        return res

    def onchange_seats(self, cr, uid, ids, attendees, seats, context=None):
        if seats:
            dicts = self.resolve_2many_commands(cr, uid, 'attendees', attendees, ['id'])
            completion = 100.0 * len(dicts) / seats
        else:
            completion = 0
        res = {'value': {'completion': completion}}
        if seats < 0:
            res['warning'] = {
                'title': "Warning: bad value",
                'message': "The number of seats should not be negative!"
            }
        return res


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
        'instructor': fields.many2one('res.partner', string='Instructor',
                        domain=['|', ('instructor', '=', True),
                                ('category_id.name', 'like', 'Teacher')]),
        'attendees': fields.many2many('res.partner', string='Attendees'),
        
        # function fields
        'completion': fields.function(_get_completion, type='float',
                        string='Completion', help='Percentage of taken seats.'),
        
        }
