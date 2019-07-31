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

from odoo import fields, api, models, _
from odoo.exceptions import UserError
import datetime

class OeHealthAppointmentWalkin(models.Model):
    _name = "oeh.medical.appointment.register.walkin"

    MARITAL_STATUS = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated'),
    ]

    SEX = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    BLOOD_TYPE = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    RH = [
        ('+','+'),
        ('-','-'),
    ]

    WALKIN_STATUS = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Invoiced', 'Invoiced'),
    ]

    @api.multi
    def _get_physician(self):
        """Return default physician value"""
        therapist_obj = self.env['oeh.medical.physician']
        domain = [('oeh_user_id', '=', self.env.uid)]
        user_ids = therapist_obj.search(domain)
        if user_ids:
            return user_ids.id or False
        else:
            return False


    name = fields.Char(string='Queue #', size=128, required=True, readonly=True, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True, readonly=True, states={'Scheduled': [('readonly', False)]})
    dob = fields.Date(string='Date of Birth', readonly=True, states={'Scheduled': [('readonly', False)]})
    sex = fields.Selection(SEX, string='Sex', index=True, readonly=True, states={'Scheduled': [('readonly', False)]})
    marital_status = fields.Selection(MARITAL_STATUS, string='Marital Status', readonly=True, states={'Scheduled': [('readonly', False)]})
    blood_type = fields.Selection(BLOOD_TYPE, string='Blood Type', readonly=True, states={'Scheduled': [('readonly', False)]})
    rh = fields.Selection(RH, string='Rh', readonly=True, states={'Scheduled': [('readonly', False)]})
    doctor = fields.Many2one('oeh.medical.physician', string='Responsible Physician', readonly=True, states={'Scheduled': [('readonly', False)]}, default=_get_physician)
    state = fields.Selection(WALKIN_STATUS, string='State', readonly=True, states={'Scheduled': [('readonly', False)]}, default=lambda *a: 'Scheduled')
    comments = fields.Text(string='Comments', readonly=True, states={'Scheduled': [('readonly', False)]})
    date = fields.Datetime(string='Date', required=True, readonly=True, states={'Scheduled': [('readonly', False)]}, default=lambda *a: datetime.datetime.now())
    evaluation_ids = fields.One2many('oeh.medical.evaluation', 'walkin', string='Evaluation', readonly=True, states={'Scheduled': [('readonly', False)]})
    prescription_ids = fields.One2many('oeh.medical.prescription','walkin', string='Prescriptions', readonly=True, states={'Scheduled': [('readonly', False)]})
    lab_test_ids = fields.One2many('oeh.medical.lab.test', 'walkin', string='Lab Tests', readonly=True, states={'Scheduled': [('readonly', False)]})
    inpatient_ids = fields.One2many('oeh.medical.inpatient', 'walkin', string='Inpatient Admissions', readonly=True, states={'Scheduled': [('readonly', False)]})
    vaccine_ids = fields.One2many('oeh.medical.vaccines', 'walkin', string='Vaccines', readonly=True, states={'Scheduled': [('readonly', False)]})

    _sql_constraints = [
        ('full_name_uniq', 'unique (name)', 'The Queue Number must be unique')
    ]


    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.appointment.register.walkin')
        vals['name'] = sequence
        return super(OeHealthAppointmentWalkin, self).create(vals)

    @api.onchange(patient)
    def onchange_patient(self):
        if self.patient:
            self.dob = self.patient.dob
            self.sex = self.patient.sex
            self.marital_status = self.patient.marital_status
            self.blood_type = self.patient.blood_type
            self.rh = self.patient.rh

    @api.multi
    def _default_account(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        return journal.default_credit_account_id.id

    @api.multi
    def action_walkin_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        inv_ids = []

        for acc in self:
            # Create Invoice
            if acc.doctor:
                curr_invoice = {
                    'partner_id': acc.patient.partner_id.id,
                    'account_id': acc.patient.partner_id.property_account_receivable_id.id,
                    'patient': acc.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice': acc.date,
                    'origin': "Walkin # : " + acc.name,
                }

                inv_ids = invoice_obj.create(curr_invoice)

                if inv_ids:
                    inv_id = inv_ids.id
                    prd_account_id = self._default_account()

                    # Create Invoice line
                    curr_invoice_line = {
                        'name':"Consultancy invoice for " + acc.name,
                        'price_unit': acc.doctor.consultancy_price,
                        'quantity': 1,
                        'account_id': prd_account_id,
                        'invoice_id': inv_id,
                    }

                    inv_line_ids = invoice_line_obj.create(curr_invoice_line)
                self.write({'state': 'Invoiced'})

            else:
                raise UserError(_('Configuration error!\nCould not find any physician to create the invoice !'))

        return {
                'domain': "[('id','=', " + str(inv_id) + ")]",
                'name': 'Walkin Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }

    @api.multi
    def set_to_completed(self):
        return self.write({'state': 'Completed'})

# Physician schedule management for Walkins

class OeHealthPhysicianWalkinSchedule(models.Model):
    _name = "oeh.medical.physician.walkin.schedule"
    _description = "Information about walkin schedule"

    name = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    physician_id = fields.Many2one('oeh.medical.physician', string='Physician', index=True, ondelete='cascade')

    _order = 'name desc'


# Inheriting Physician screen to add walkin schedule lines

class OeHealthPhysician(models.Model):
    _inherit = "oeh.medical.physician"
    walkin_schedule_lines = fields.One2many('oeh.medical.physician.walkin.schedule', 'physician_id', string='Walkin Schedule')

# Inheriting Inpatient module to add "Walkin" screen reference
class OeHealthInpatient(models.Model):
    _inherit = 'oeh.medical.inpatient'
    walkin = fields.Many2one('oeh.medical.appointment.register.walkin', string='Queue #', readonly=True, states={'Draft': [('readonly', False)]})


# Inheriting Prescription module to add "Walkin" screen reference
class OeHealthPrescription(models.Model):
    _inherit = 'oeh.medical.prescription'
    walkin = fields.Many2one('oeh.medical.appointment.register.walkin', string='Queue #', readonly=True, states={'Draft': [('readonly', False)]})


# Inheriting Evaluation module to add "Walkin" screen reference
class OeHealthPatientEvaluation(models.Model):
    _inherit = 'oeh.medical.evaluation'
    walkin = fields.Many2one('oeh.medical.appointment.register.walkin', string='Queue #')


# Inheriting Evaluation module to add "Walkin" screen reference
class OeHealthLabTests(models.Model):
    _inherit = 'oeh.medical.lab.test'
    walkin = fields.Many2one('oeh.medical.appointment.register.walkin', string='Queue #', readonly=True, states={'Draft': [('readonly', False)]})


# Inheriting Evaluation module to add "Walkin" screen reference
class OeHealthVaccines(models.Model):
    _inherit = 'oeh.medical.vaccines'
    walkin = fields.Many2one('oeh.medical.appointment.register.walkin', string='Queue #')