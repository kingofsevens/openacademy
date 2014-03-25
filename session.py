# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

from datetime import datetime, timedelta

from openerp.osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

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

    def _get_end_date(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for session in self.browse(cr, uid, ids, context):
            if session.start_date:
                dt = datetime.strptime(session.start_date, DATE_FORMAT)
                if session.duration > 0:
                    dt += timedelta(days=session.duration, seconds=-1)
                res[session.id] = dt.strftime(DATE_FORMAT)
            else:
                res[session.id] = False
        return res

    def _set_end_date(self, cr, uid, id, field, value, arg, context=None):
        session = self.browse(cr, uid, id, context)
        if session.start_date and value:
            dt0 = datetime.strptime(session.start_date, DATE_FORMAT)
            dt1 = datetime.strptime(value[:10], DATE_FORMAT)
            duration = (dt1 - dt0).days + 1
        else:
            duration = 0
        self.write(cr, uid, [id], {'duration': duration}, context=context)

    def _get_attendee_count(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for session in self.browse(cr, uid, ids, context):
            res[session.id] = len(session.attendees)
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
        'active': fields.boolean('Active'),
        'color': fields.integer('Color'),
        'state': fields.selection(
            [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')],
            string='State', required=True, readonly=True),
        
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
        'end_date': fields.function(_get_end_date, fnct_inv=_set_end_date,
                        type='date', string='End Date'),
        'attendee_count': fields.function(_get_attendee_count, type='integer',
                        string='Number of Attendees', store=True),
        }
        
    _defaults = {
        'active': True,
        'start_date': fields.date.today,
        'state': 'draft',
    }
        
    def _check_instructor(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context):
            if session.instructor in session.attendees:
                return False
        return True

    _constraints = [
        (_check_instructor, 'Instructors cannot attend their own session.',
            ['instructor', 'attendees']),
    ]

