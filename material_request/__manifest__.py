{
    'name': 'Material Project',
    'version': '1.0',
    'summary': 'Material Project Manegment',
    'description': """Material Project Customization""",

    # 'category': 'Inventory',

    'depends': ['base','hr','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_request.xml',
        # 'reports/material_report.xml',
        'data/sequence.xml',

    ],

    'assets':{
       'web.assets_backend' : ['material_request/static/src/css/material.css']
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
