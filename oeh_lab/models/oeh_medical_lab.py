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
import time
import datetime


# Lab Units Management

class OeHealthLabTestUnits(models.Model):
    _name = 'oeh.medical.lab.units'
    _description = 'Lab Test Units'

    name = fields.Char(string='Unit Name', size=25, required=True)
    code = fields.Char(string='Code', size=25, required=True)

    _sql_constraints = [('name_uniq', 'unique(name)', 'The Lab unit name must be unique')]

# Lab Test Department
class OeHealthLabTestDepartment(models.Model):
    _name = 'oeh.medical.labtest.department'
    _description = 'Lab Test Departments'

    name = fields.Char(string='Name', size=128, required=True)

# Lab Test Types Management

class OeHealthLabTestCriteria(models.Model):
    _name = 'oeh.medical.labtest.criteria'
    _description = 'Lab Test Criteria'

    name = fields.Char(string='Tests', size=128, required=True)
    normal_range = fields.Text(string='Normal Range')
    units = fields.Many2one('oeh.medical.lab.units', string='Units')
    sequence = fields.Integer(string='Sequence')
    medical_type_id = fields.Many2one('oeh.medical.labtest.types', string='Lab Test Types')

    _order="sequence"


class OeHealthLabTestMaterial(models.Model):
    _name = 'oeh.medical.labtest.material'
    _description = 'Materiales para prueba de laboratorio'
    name = fields.Many2one('product.product',string='Producto')
    cantidad = fields.Integer(string="Cantidad")
    medical_type_id = fields.Many2one('oeh.medical.labtest.types', string='Lab Test Types')



class OeHealthLabTestTypes(models.Model):
    _name = 'oeh.medical.labtest.types'
    _description = 'Lab Test Types'

    name = fields.Char(string='Lab Test Name', size=128, required=True, help="Test type, eg X-Ray, Hemogram, Biopsy...")
    code = fields.Char(string='Code', size=128, help="Short code for the test")
    info = fields.Text(string='Description')
    test_charge = fields.Float(string='Test Charge', default=lambda *a: 0.0)
    lab_criteria = fields.One2many('oeh.medical.labtest.criteria', 'medical_type_id', string='Lab Test Cases')
    lab_material = fields.One2many('oeh.medical.labtest.material', 'medical_type_id', string='Materiales para prueba de laboratorio')
    lab_department = fields.Many2one('oeh.medical.labtest.department', string='Department')


class OeHealthLabTests(models.Model):
    _name = 'oeh.medical.lab.test'
    _description = 'Lab Tests'

    LABTEST_STATE = [
        ('Draft', 'Draft'),
        ('Test In Progress', 'Test In Progress'),
        ('Completed', 'Completed'),
        ('Invoiced', 'Invoiced'),
    ]

    name = fields.Char(string='Lab Test #', size=16, readonly=True, required=True, help="Lab result ID", default=lambda *a: '/')
    lab_department = fields.Many2one('oeh.medical.labtest.department', string='Department', readonly=True, states={'Draft': [('readonly', False)]})
    test_type = fields.Many2one('oeh.medical.labtest.types', string='Test Type', domain="[('lab_department', '=', lab_department)]", required=True, readonly=True, states={'Draft': [('readonly', False)]}, help="Lab test type")
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    pathologist = fields.Many2one('oeh.medical.physician', string='Pathologist', help="Pathologist", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    requestor = fields.Char(string='Doctor who requested the test', help="Doctor who requested the test", readonly=True, states={'Draft': [('readonly', False)]})
    results = fields.Text(string='Results', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    diagnosis = fields.Text(string='Diagnosis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    lab_test_criteria = fields.One2many('oeh.medical.lab.resultcriteria', 'medical_lab_test_id', string='Lab Test Result', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    date_requested = fields.Datetime(string='Date requested', readonly=True, states={'Draft': [('readonly', False)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    date_analysis = fields.Datetime(string='Date of the Analysis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    state = fields.Selection(LABTEST_STATE, string='State', readonly=True, default=lambda *a: 'Draft')


    have_imss = fields.Boolean(string='¿Tiene Seguro?', readonly=True, states={'Draft': [('readonly', False)]})
    discount = fields.Integer(string='Porcentaje de Descuento', readonly=True, states={'Draft': [('readonly', False)]})
    vale = fields.Char(string='N° de Vale', readonly=True, states={'Draft': [('readonly', False)]})
    hospital_estudio = fields.Many2one('oeh.medical.health.center', string='Hospital donde de hará el estudio', help="Medical Center", readonly=True, states={'Draft': [('readonly', False)]})
    lab_test_indications = fields.One2many('oeh.medical.lab.indications.lines', 'medical_lab_test_id', string='Indicaciones', readonly=True, states={'Draft': [('readonly', False)]})





    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.lab.test')
        vals['name'] = sequence or '/'
        return super(OeHealthLabTests, self).create(vals)


    # Fetching lab test types
    @api.onchange('test_type')
    def onchange_test_type_id(self):
        values = self.onchange_test_type_id_values(self.test_type.id if self.test_type else False)
        return values


    @api.multi
    def onchange_test_type_id_values(self, test_type):
        criteria_obj = self.env['oeh.medical.labtest.criteria']
        labtest_ids =[]

        res = {}

         # if no test type present then nothing will process
        if (not test_type):
            return res

        #defaults
        res = {'value':{
                'lab_test_criteria':[],
            }
        }

        # Getting lab test lines values
        query = _("select name, sequence, normal_range, units from oeh_medical_labtest_criteria where medical_type_id=%s") % (str(test_type))
        self.env.cr.execute(query)
        vals = self.env.cr.fetchall()
        if vals:
            for va in vals:
                specs = {
                          'name': va[0],
                          'sequence': va[1],
                          'normal_range': va[2],
                          'units': va[3],
                        }
                labtest_ids += [specs]

        res['value'].update({
            'lab_test_criteria': labtest_ids,
        })
        return res


    # This function prints the lab test
    @api.multi
    def print_patient_labtest(self):
        return self.env.ref('oehealth.action_report_patient_labtest').report_action(self)

    @api.multi
    def set_to_test_inprogress(self):
        for l in self.test_type.lab_material:
            # Toma por defecto la ubicacion "Existencias" - (WH/Existencias)
            stockquant_id = self.env['stock.quant'].search([('location_id.id', '=', 15),('product_id', '=', l.name.id)], limit=1)
            stockquant_id.quantity = (stockquant_id.quantity)-(l.cantidad)
        return self.write({'state': 'Test In Progress', 'date_analysis': datetime.datetime.now()})

    @api.multi
    def set_to_test_complete(self):
        return self.write({'state': 'Completed'})

    @api.multi
    def _default_account(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        return journal.default_credit_account_id.id

    def action_lab_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        desc = 0
        nvale = ''
        for lab in self:
            # Create Invoice
            if lab.patient:
                if self.have_imss == True:
                    desc = self.discount
                    nvale = "\nNo. de Vale: " + self.vale
                curr_invoice = {
                    'partner_id': lab.patient.partner_id.id,
                    'account_id': lab.patient.partner_id.property_account_receivable_id.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice':datetime.datetime.now(),
                    'origin': "Lab Test# : " + lab.name,
                    'target': 'new',
                }

                inv_ids = invoice_obj.create(curr_invoice)
                inv_id = inv_ids.id

                if inv_ids:
                    prd_account_id = self._default_account()
                    if lab.test_type:

                        # Create Invoice line
                        curr_invoice_line = {
                            'name': "Charge for " + str(lab.test_type.name) + " laboratory test" + nvale,
                            'price_unit': (lab.test_type.test_charge - ((lab.test_type.test_charge / 100) * desc)) or 0,
                            'quantity': 1.0,
                            'account_id': prd_account_id,
                            'invoice_id': inv_id,
                        }

                        inv_line_ids = invoice_line_obj.create(curr_invoice_line)

                self.write({'state': 'Invoiced'})

        return {
                'domain': "[('id','=', " + str(inv_id) + ")]",
                'name': 'Lab Test Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }



class OeHealthLabTestsIndications(models.Model):
    _name = 'oeh.medical.lab.indications'
    _description = 'Indicaciones para pruebas de laboratorio'
    name = fields.Char(string='Descripción', required=True)


class OeHealthLabTestsIndicationsLine(models.Model):
    _name = 'oeh.medical.lab.indications.lines'
    _description = 'Indicaciones'
    name = fields.Many2one("oeh.medical.lab.indications",string='Indicaciones', required=True)
    extra_info = fields.Char(string="Datos adicionales")
    medical_lab_test_id = fields.Many2one('oeh.medical.lab.test', string='Lab Tests')


class OeHealthLabTestsResultCriteria(models.Model):
    _name = 'oeh.medical.lab.resultcriteria'
    _description = 'Lab Test Result Criteria'

    name = fields.Char(string='Tests', size=128, required=True)
    result = fields.Text(string='Result')
    normal_range = fields.Text(string='Normal Range')
    units = fields.Many2one('oeh.medical.lab.units', string='Units')
    sequence = fields.Integer(string='Sequence')
    medical_lab_test_id = fields.Many2one('oeh.medical.lab.test', string='Lab Tests')

    _order="sequence"

# Inheriting Patient module to add "Lab" screen reference
class OeHealthPatient(models.Model):
    _inherit='oeh.medical.patient'
    
    @api.multi
    def _labtest_count(self):
        oe_labs = self.env['oeh.medical.lab.test']
        for ls in self:
            domain = [('patient', '=', ls.id)]
            lab_ids = oe_labs.search(domain)
            labs = oe_labs.browse(lab_ids)
            labs_count = 0
            for lab in labs:
                labs_count+=1
            ls.labs_count = labs_count
        return True

    lab_test_ids = fields.One2many('oeh.medical.lab.test', 'patient', string='Lab Tests')
    labs_count = fields.Integer(compute=_labtest_count, string="Lab Tests")