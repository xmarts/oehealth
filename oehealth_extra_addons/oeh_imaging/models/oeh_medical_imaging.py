##############################################################################
#    Copyright (C) 2018 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions

# Odoo Proprietary License v1.0
#
# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, oeHealth.in, openerpestore.com, or if you have received a written
# agreement from the authors of the Software.
#
# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time
import datetime

# Imaging Test Department
class OeHealthImagingTestDepartment(models.Model):
    _name = 'oeh.medical.imagingtest.department'
    _description = 'Imaging Test Departments'

    name = fields.Char(string='Name', size=128, required=True)

# Imaging Test Type Management

class OeHealthImagingTestType(models.Model):
    _name = 'oeh.medical.imaging.test.type'
    _description = 'Imaging Test Type Configuration'

    name = fields.Char(string='Name', size=128, required=True)
    code = fields.Char(string='Code', size=25, required=True)
    test_charge = fields.Float(string='Test Charge', required=True, default=lambda *a: 0.0)
    imaging_department = fields.Many2one('oeh.medical.imagingtest.department', string='Department')

    _sql_constraints = [('name_uniq', 'unique(name)', 'The Imaging test type name must be unique')]


# Imaging Test Management

class OeHealthImagingTypeManagement(models.Model):
    _name = 'oeh.medical.imaging'
    _description = 'Imaging Test Management'

    IMAGING_STATE = [
        ('Draft', 'Draft'),
        ('Test In Progress', 'Test In Progress'),
        ('Completed', 'Completed'),
        ('Invoiced', 'Invoiced'),
    ]

    name = fields.Char(string='Test #', size=16, required=True, readonly=True, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    imaging_department = fields.Many2one('oeh.medical.imagingtest.department', string='Department', readonly=True, states={'Draft': [('readonly', False)]})
    test_type = fields.Many2one('oeh.medical.imaging.test.type', string='Test Type', domain="[('imaging_department', '=', imaging_department)]", required=True, readonly=True, states={'Draft': [('readonly', False)]}, help="Imaging Test type")
    requestor = fields.Many2one('oeh.medical.physician', string='Doctor who requested the test', domain=[('is_pharmacist','=',False)], help="Doctor who requested the test", readonly=True, states={'Draft': [('readonly', False)]})
    analysis = fields.Text(string='Analysis', readonly=True, states={'Test In Progress': [('readonly', False)]})
    conclusion = fields.Text(string='Conclusion', readonly=True, states={'Test In Progress': [('readonly', False)]})
    date_requested = fields.Datetime(string='Date requested', readonly=True, states={'Draft': [('readonly', False)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    date_analysis = fields.Datetime(string='Date of the Analysis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    state = fields.Selection(IMAGING_STATE, string='State',readonly=True, default=lambda *a: 'Draft')
    image1 = fields.Binary(string="Image 1", readonly=True, states={'Test In Progress': [('readonly', False)]})
    image2 = fields.Binary(string="Image 2", readonly=True, states={'Test In Progress': [('readonly', False)]})
    image3 = fields.Binary(string="Image 3", readonly=True, states={'Test In Progress': [('readonly', False)]})
    image4 = fields.Binary(string="Image 4", readonly=True, states={'Test In Progress': [('readonly', False)]})
    image5 = fields.Binary(string="Image 5", readonly=True, states={'Test In Progress': [('readonly', False)]})
    image6 = fields.Binary(string="Image 6", readonly=True, states={'Test In Progress': [('readonly', False)]})

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.imaging')
        vals['name'] = sequence
        return super(OeHealthImagingTypeManagement, self).create(vals)

    @api.multi
    def print_patient_imaging(self):
        return self.env.ref('oehealth_extra_addons.action_report_patient_imaging').report_action(self)


    @api.multi
    # Preventing deletion of a imaging details which is not in draft state
    def unlink(self):
        for imaging in self.filtered(lambda imaging: imaging.state not in ['Draft']):
            raise UserError(_('You can not delete imaging information which is not in "Draft" state !!'))
        return super(OeHealthImagingTypeManagement, self).unlink()

    @api.multi
    def set_to_test_start(self):
        return self.write({'state': 'Test In Progress','date_analysis': datetime.datetime.now()})

    @api.multi
    def set_to_test_complete(self):
        return self.write({'state': 'Completed'})

    @api.multi
    def _default_account(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        return journal.default_credit_account_id.id

    @api.multi
    def action_imaging_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        inv_ids = []
        inv_line_ids = []

        for imaging in self:
            # Create Invoice
            if imaging.patient:
                curr_invoice = {
                    'partner_id': imaging.patient.partner_id.id,
                    'account_id': imaging.patient.partner_id.property_account_receivable_id.id,
                    'patient': imaging.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice': datetime.datetime.now(),
                    'origin': "Imaging Test# : " + imaging.name,
                    'target': 'new',
                }

                inv_ids = invoice_obj.create(curr_invoice)

                if inv_ids:
                    inv_id = inv_ids.id
                    prd_account_id = self._default_account()
                    if imaging.test_type:

                        # Create Invoice line
                        curr_invoice_line = {
                            'name': "Charge for " + str(imaging.test_type.name) + " Imaging test",
                            'price_unit': imaging.test_type.test_charge or 0,
                            'quantity': 1.0,
                            'account_id': prd_account_id,
                            'invoice_id': inv_id,
                        }

                        inv_line_ids = invoice_line_obj.create(curr_invoice_line)

                self.write({'state': 'Invoiced'})

        return {
                'domain': "[('id','=', " + str(inv_id) + ")]",
                'name': 'Imaging Test Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }