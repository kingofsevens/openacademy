# -*- coding: utf-8 -*-
#
# Module Open Academy for OpenERP
#

{
    'name': 'Open Academy for OpenERP',
    'description': """
This module is aimed at managing training sessions:
 - training courses,
 - course sessions,
 - attendee subscription.
""",
    'version': '1.0',
    'author': '7Gates Interactive Technologies',
    'website': 'http://7gates.co',
    'depends': ['base'],
    'data': [
        'data/partner.xml',
        'view/menu.xml',
        'view/course.xml',
        'view/session.xml',
        'view/partner.xml',
    ],
}