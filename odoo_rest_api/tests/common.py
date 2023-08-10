from odoo.tests import common


class TestSaleCommonBase(common.TransactionCase):
    ''' Setup with sale test configuration. '''

    @classmethod
    def setUpClass(cls):
        """
        master data
        """
        super(TestSaleCommonBase, cls).setUpClass()
        product_data = cls.detail_product()
        ids = [cls.data_product(cls, line) for line in product_data]
        cls.product_ids = cls.prepare_product(cls, ids)
        
    
    def data_product(cls, data):
        return cls.env.ref(data).id
    
    def detail_product():
        data = [
            'sale.product_product_4e', 
            'sale.product_product_4f', 
            'product.product_product_5', 
            'product.product_product_6',
            'product.product_product_7',
        ]
        return data

    def prepare_product(cls, ids):
        domain = [('id', 'in', ids)]
        res = []
        for rec in cls.env['product.product'].search(domain):
            res.append(cls.set_data(rec))
        return res
        
    def set_data(data):
        res = {
            'name':data.name,
            'id': data.id
        }
        return res
        
