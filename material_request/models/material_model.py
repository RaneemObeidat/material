from email.policy import default

from odoo import models, fields, api
# first step  نكتب الكلاس بعدين ال fields بعدين كل ما ندخل قيمة بدخل فيلدز جديد والعلاقات حسب شو بحتاج

class MaterialRequest(models.Model):
    _name = 'material.request'
    _description = '  Material Request'

    ref = fields.Char(default='New', readonly=1,string='Reference')
    request_date = fields.Date(string='Request date', required=False)
    department = fields.Many2one('hr.department',string='Department', required=False)
    vendor_id = fields.Many2one('res.partner',string='Vendor', required=False)
    operation_type = fields.Many2one('stock.picking.type',string='Operation Type', required=False)
    destination = fields.Many2one('stock.location',string='Destination',required=False)
    source_id = fields.Many2one('stock.location',string='Source', required=False)
    material_request_lines = fields.One2many('material.request.lines','material_request_id', string='Material Request Lines')
    # استخدمت selecttion هون حتى اكتب خيارات ال statusbar
    status = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('in progress','In Progress'),
        ('done','Done'),
        ('canceled','Canceled')
    ],
        default='draft')
    active = fields.Boolean(string="Active", default=True)

    # هاد الfields حتى اعرف زر ال check availability
    check_is_available = fields.Boolean(string='Check Availability', default=False)

    # هاد ال function لنكتب اجراء مرتبط بالزر confirm
    def action_confirm(self):
        for record in self:
            if record.status == 'draft':
                record.status = 'pending'
            elif record.status == 'pending':
                record.status = 'in_progress'
            elif record.status == 'in_progress':
                record.status = 'done'
            elif record.status == 'done':
                record.status = 'canceled'
            elif record.status == 'canceled':
                record.status = 'draft'

    # هاد ال function لنكتب اجراء مرتبط بالزر check
    def action_check(self):
        for record in self:
            for line in record.material_request_lines:
                if line.product_id:
                    qty_available = line.product_id.qty_available

                    if line.quantity <= qty_available:
                        line.is_available = True
                    else:
                        line.is_available = False

    def action_canceled(self):
        for record in self:
            record.status = 'canceled'

    def create(self,vals):
        res = super(MaterialRequest,self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('material_seq')
            return res

    # def action(self):
    #     pass

    # def action_open(self):
    #     print('True')

# هاد الكلاس لنكتب فيلدز ال نوت بوك
class MaterialRequestLines(models.Model):
    _name='material.request.lines'
    _description = 'Material Request Lines'

    material_request_id = fields.Many2one('material.request', string='Material Request')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    is_available = fields.Boolean(string='Is Available', readonly=True)
    purchased = fields.Boolean(string='Purchased', readonly=True)
    transferred = fields.Boolean(string='Transferred', readonly=True)
