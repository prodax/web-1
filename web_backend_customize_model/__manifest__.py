# -*- coding: utf-8 -*-
{
    'name': "Backend Theme Customize Model",
    'summary': """
        Customize your backend theme as per your needs""",
    'description': """
        Customize your backend theme as per your needs
    """,
    'author': "Kaushal Prajapati",
    'category': 'web',
    'version': '10.0.1.0.0',
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': ['web'],
    # always loaded
    'data': [
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}