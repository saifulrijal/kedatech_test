{
    'name': 'Odoo REST API V2',
    'version': '14.0.1.1',
    'description': "",
    'website': '',
    'depends': [
        'sale_management',
        'product',
        'purchase',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/material_product_views.xml',
        'views/material_product_line_views.xml',
        'views/sale_order_views.xml',
        'views/product_product_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['pypeg2']
    }
}
