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

    def _get_default_session(self, cr, uid, context=None):
        return context and \
            context.get('active_model') == 'openacademy.session' and \
            context.get('active_id') or False

    _defaults = {
        'session': _get_default_session,
    }


    def action_subscribe(self, cr, uid, ids, context=None):
        # we know that ids is a list with one element only
        wizard = self.browse(cr, uid, ids[0], context)
        # write on the session record to add attendees
        session_model = self.pool.get('openacademy.session')
        values = {
            'attendees': [(4, partner.id) for partner in wizard.attendees],
        }
        session_model.write(cr, uid, [wizard.session.id], values, context=context)
        # return {} to close the window
        return {}
        