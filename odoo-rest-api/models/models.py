from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang

class MaterialProductLine(models.Model):
    _name = 'material.product.line'
    _description = 'material product line'
    _rec_name = 'product_id'
    
    product_id = fields.Many2one('product.product')
    buy_price = fields.Float(default=101.0)
    suplier_id = fields.Many2one('res.partner')
    material_product_id = fields.Many2one('material.product')
    type = fields.Selection(
        [('Fabric', 'Fabric'), ('Jeans', 'Jeans'), ('Cotton', 'Cotton')],
        compute='onchange_material_product_id', store=True)
    
    _sql_constraints = [
        ('product_material_uniq', 'unique (product_id,material_product_id)', 'Duplicate Product !')
    ]
    
    @api.constrains('buy_price')
    def check_buy_price(self):
        for rec in self:
            if rec.buy_price < 100:
                raise UserError(_('Buy price must be greather than 0'))
            
    @api.onchange('product_id')
    def _campus_onchange(self):
        res = {}
        self.product_id.variant_seller_ids
        ids = [line.name.id for line in self.product_id.variant_seller_ids]
        res['domain']={'suplier_id':[('id', 'in', ids)]}
        return res
        
    @api.depends('material_product_id')
    def onchange_material_product_id(self):
        for rec in self:
            data = ''
            if rec.material_product_id:
                data = rec.material_product_id.type
            rec.type = data
            
    def unlink(self):
        return super(MaterialProductLine, self).unlink()

class MaterialProduct(models.Model):
    _name = 'material.product'
    _description = 'material product'
    
    code = fields.Char(required=True)
    name = fields.Char(required=True)
    type = fields.Selection([('Fabric', 'Fabric'), ('Jeans', 'Jeans'), ('Cotton', 'Cotton')])
    material_line_ids = fields.One2many('material.product.line', 'material_product_id')
    
    def name_get(self):
        data = []
        for rec in self:
            name = rec.name+'('+rec.code+'/'+rec.type+')'
            id = rec.id
            data.append((id, name))
        return data
    
    def write(self, vals):
        res = super(MaterialProduct, self).write(vals)
        for rec in self:
            type = rec.type
            datas = self.env['material.product.line'].search([('material_product_id', '=', rec.id)])
            datas.type=type     
        return res       
    
    def unlink(self):
        ids = self.ids
        datas = self.env['material.product.line'].search([('material_product_id', '=', ids)])
        datas.type=False
        return super(MaterialProduct, self).unlink()
            
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    material_product_id = fields.Many2one('material.product', required=True)
    
    @api.onchange('material_product_id')
    def _campus_onchange(self):
        res = {}
        material_id = self.env['material.product'].search([('id', '=', self.material_product_id.id)])
        ids = [line.product_id.id for line in material_id.material_line_ids]
        res['domain']={'product_id':[('id', 'in', ids), ('sale_ok', '=', True), '|',('company_id', '=', self.company_id), ('company_id', '=', False)]}
        return res
    
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if res != None and 'warning' not in res:
            if self.order_id.pricelist_id and self.order_id.partner_id and self.material_product_id:
                data = self.env['material.product.line'].search([('product_id', '=', self.product_id.id), ('material_product_id', '=', self.material_product_id.id)], limit=1)
                if data:
                    self.update({'price_unit': data.buy_price})
        return res
    
    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            data = self.env['material.product.line'].search([('product_id', '=', self.product_id.id), ('material_product_id', '=', self.material_product_id.id)], limit=1)
            if data:
                self.price_unit = data.buy_price
        return res
    
class productProduct(models.Model):
    _inherit = 'product.product'
    
    def action_material_line(self):
        action = self.env.ref('odoo-rest-api.action_material_product_line').read()[0]
        domain = [('product_id', '=', self.id)]
        action['domain'] = domain
        return action
    
    
    
    
    
    
