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

import datetime
from datetime import timedelta
import logging
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

# Family Management

class OeHealthFamily(models.Model):
    _name = 'oeh.medical.patient.family'

    FAMILY_RELATION = [
                ('Father', 'Father'),
                ('Mother', 'Mother'),
                ('Brother', 'Brother'),
                ('Sister', 'Sister'),
                ('Wife', 'Wife'),
                ('Husband', 'Husband'),
                ('Grand Father', 'Grand Father'),
                ('Grand Mother', 'Grand Mother'),
                ('Aunt', 'Aunt'),
                ('Uncle', 'Uncle'),
                ('Nephew', 'Nephew'),
                ('Niece', 'Niece'),
                ('Cousin', 'Cousin'),
                ('Relative', 'Relative'),
                ('Other', 'Other'),
    ]

    name = fields.Char(size=256, string='Name', required=True, help='Family Member Name')
    relation = fields.Selection(FAMILY_RELATION, string='Relation', help="Family Relation", index=True)
    age = fields.Integer(string='Age', help='Family Member Age')
    deceased = fields.Boolean(string='Deceased?',help="Mark if the family member has died")
    patient_id = fields.Many2one('oeh.medical.patient', 'Patient', required=True, ondelete='cascade', index=True)

# Patient Management

class OeHealthPatient(models.Model):
    _name='oeh.medical.patient'
    _inherits={
        'res.partner': 'partner_id',
    }

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

    @api.multi
    def _app_count(self):
        oe_apps = self.env['oeh.medical.appointment']
        for pa in self:
            domain = [('patient', '=', pa.id)]
            app_ids = oe_apps.search(domain)
            apps = oe_apps.browse(app_ids)
            app_count = 0
            for ap in apps:
                app_count+=1
            pa.app_count = app_count
        return True

    @api.multi
    def _prescription_count(self):
        oe_pres = self.env['oeh.medical.prescription']
        for pa in self:
            domain = [('patient', '=', pa.id)]
            pres_ids = oe_pres.search(domain)
            pres = oe_pres.browse(pres_ids)
            pres_count = 0
            for pr in pres:
                pres_count+=1
            pa.prescription_count = pres_count
        return True

    @api.multi
    def _admission_count(self):
        oe_admission = self.env['oeh.medical.inpatient']
        for adm in self:
            domain = [('patient', '=', adm.id)]
            admission_ids = oe_admission.search(domain)
            admissions = oe_admission.browse(admission_ids)
            admission_count = 0
            for ad in admissions:
                admission_count+=1
            adm.admission_count = admission_count
        return True

    @api.multi
    def _vaccine_count(self):
        oe_vac = self.env['oeh.medical.vaccines']
        for va in self:
            domain = [('patient', '=', va.id)]
            vec_ids = oe_vac.search(domain)
            vecs = oe_vac.browse(vec_ids)
            vecs_count = 0
            for vac in vecs:
                vecs_count+=1
            va.vaccine_count = vecs_count
        return True

    @api.multi
    def _invoice_count(self):
        oe_invoice = self.env['account.invoice']
        for inv in self:
            invoice_ids = self.env['account.invoice'].search([('patient', '=', inv.id)])
            invoices = oe_invoice.browse(invoice_ids)
            invoice_count = 0
            for inv_id in invoices:
                invoice_count+=1
            inv.invoice_count = invoice_count
        return True

    @api.multi
    def _patient_age(self):
        def compute_age_from_dates (patient_dob,patient_deceased,patient_dod):
            now=datetime.datetime.now()
            if (patient_dob):
                dob=datetime.datetime.strptime(patient_dob,'%Y-%m-%d')
                if patient_deceased :
                    dod=datetime.datetime.strptime(patient_dod,'%Y-%m-%d')
                    delta= dod - dob
                    deceased=" (deceased)"
                    years_months_days = str(delta.days // 365)+" years "+ str(delta.days%365)+" days" + deceased
                else:
                    delta= now - dob
                    years_months_days = str(delta.days // 365)+" years "+ str(delta.days%365)+" days"
            else:
                years_months_days = "No DoB !"

            return years_months_days
        for patient_data in self:
            patient_data.age = compute_age_from_dates(patient_data.dob,patient_data.deceased,patient_data.dod)
        return True

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade', help='Partner-related data of the patient')
    family = fields.One2many('oeh.medical.patient.family', 'patient_id', string='Family')
    ssn = fields.Char(size=256, string='SSN')
    current_insurance = fields.Many2one('oeh.medical.insurance', string="Insurance", domain="[('patient','=', active_id),('state','=','Active')]", help="Insurance information. You may choose from the different insurances belonging to the patient")
    doctor = fields.Many2one('oeh.medical.physician', string='Family Physician', help="Current primary care physician / family doctor", domain=[('is_pharmacist','=',False)])
    dob = fields.Date(string='Date of Birth')
    age = fields.Char(compute=_patient_age, size=32, string='Patient Age', help="It shows the age of the patient in years(y), months(m) and days(d).\nIf the patient has died, the age shown is the age at time of death, the age corresponding to the date on the death certificate. It will show also \"deceased\" on the field")
    sex = fields.Selection(SEX, string='Sex', index=True)
    marital_status = fields.Selection(MARITAL_STATUS, string='Marital Status')
    blood_type = fields.Selection(BLOOD_TYPE, string='Blood Type')
    rh = fields.Selection(RH, string='Rh')
    identification_code = fields.Char(string='Patient ID', size=256, help='Patient Identifier provided by the Health Center', readonly=True)
    ethnic_group = fields.Many2one('oeh.medical.ethnicity','Ethnic group')
    critical_info = fields.Text(string='Important disease, allergy or procedures information', help="Write any important information on the patient's disease, surgeries, allergies, ...")
    general_info = fields.Text(string='General Information', help="General information about the patient")
    genetic_risks = fields.Many2many('oeh.medical.genetics', 'oeh_genetic_risks_rel', 'patient_id', 'genetic_risk_id', string='Genetic Risks')
    deceased = fields.Boolean(string='Patient Deceased ?', help="Mark if the patient has died")
    dod = fields.Date(string='Date of Death')
    cod = fields.Many2one('oeh.medical.pathology', string='Cause of Death')
    app_count = fields.Integer(compute=_app_count, string="Appointments")
    prescription_count = fields.Integer(compute=_prescription_count, string="Prescriptions")
    admission_count = fields.Integer(compute=_admission_count, string="Admission / Discharge")
    vaccine_count = fields.Integer(compute=_vaccine_count, string="Vaccines")
    invoice_count = fields.Integer(compute=_invoice_count, string="Invoices")
    oeh_patient_user_id = fields.Many2one('res.users', string='Responsible Odoo User')
    prescription_line = fields.One2many('oeh.medical.prescription.line', 'patient', string='Medicines', readonly=True)
    curp = fields.Char(string='CURP')
    seguro_social = fields.Char(string='Número de seguro social')


    _sql_constraints = [
        ('code_oeh_patient_userid_uniq', 'unique (oeh_patient_user_id)', "Selected 'Responsible' user is already assigned to another patient !")
    ]

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.patient')
        vals['identification_code'] = sequence
        vals['is_patient'] = True
        health_patient = super(OeHealthPatient, self).create(vals)
        return health_patient

    @api.onchange('state_id')
    def onchange_state(self):
        if self.state_id:
            self.country_id = self.state_id.country_id.id

    @api.multi
    def print_patient_label(self):
        return self.env.ref('oehealth.action_report_patient_label').report_action(self)

# Physician Management

class OeHealthPhysicianSpeciality(models.Model):
    _name = "oeh.medical.speciality"
    _description = "Physician Speciality"

    name = fields.Char(string='Description', size=128, help="ie, Addiction Psychiatry", required=True)
    code = fields.Char(string='Code', size=128, help="ie, ADP")

    _order = 'name'
    _sql_constraints = [
        ('code_uniq', 'unique (name)', 'The Medical Speciality code must be unique')]


class OeHealthPhysicianDegree(models.Model):
    _name = "oeh.medical.degrees"
    _description = "Physicians Degrees"

    name = fields.Char(string='Degree', size=128, required=True)
    full_name = fields.Char(string='Full Name', size=128)
    physician_ids = fields.Many2many('oeh.medical.physician', id1='degree_id', id2='physician_id', string='Physicians')

    _sql_constraints = [
        ('full_name_uniq', 'unique (name)', 'The Medical Degree must be unique')]

class OeHealthPhysician(models.Model):
    _name = "oeh.medical.physician"
    _description = "Information about the doctor"
    _inherits={
        'hr.employee': 'employee_id',
    }

    CONSULTATION_TYPE = [
        ('Residential', 'Residential'),
        ('Visiting', 'Visiting'),
        ('Other', 'Other'),
    ]

    APPOINTMENT_TYPE = [
        ('Not on Weekly Schedule', 'Not on Weekly Schedule'),
        ('On Weekly Schedule', 'On Weekly Schedule'),
    ]

    @api.multi
    def _app_count(self):
        oe_apps = self.env['oeh.medical.appointment']
        for pa in self:
            domain = [('doctor', '=', pa.id)]
            app_ids = oe_apps.search(domain)
            apps = oe_apps.browse(app_ids)
            app_count = 0
            for ap in apps:
                app_count+=1
            pa.app_count = app_count
        return True

    @api.multi
    def _prescription_count(self):
        oe_pres = self.env['oeh.medical.prescription']
        for pa in self:
            domain = [('doctor', '=', pa.id)]
            pres_ids = oe_pres.search(domain)
            pres = oe_pres.browse(pres_ids)
            pres_count = 0
            for pr in pres:
                pres_count+=1
            pa.prescription_count = pres_count
        return True

    employee_id = fields.Many2one('hr.employee', string='Related Employee', required=True, ondelete='cascade', help='Employee-related data of the physician')
    institution = fields.Many2one('oeh.medical.health.center', string='Institution', help="Institution where doctor works")
    code = fields.Char(string='Licence ID', size=128, help="Physician's License ID")
    speciality = fields.Many2one('oeh.medical.speciality', string='Speciality', help="Speciality Code")
    consultancy_type = fields.Selection(CONSULTATION_TYPE, string='Consultancy Type', help="Type of Doctor's Consultancy", default=lambda *a: 'Residential')
    consultancy_price = fields.Integer(string='Consultancy Charge', help="Physician's Consultancy price")
    available_lines = fields.One2many('oeh.medical.physician.line', 'physician_id', string='Physician Availability')
    degree_id = fields.Many2many('oeh.medical.degrees', id1='physician_id', id2='degree_id', string='Degrees')
    app_count = fields.Integer(compute=_app_count, string="Appointments")
    prescription_count = fields.Integer(compute=_prescription_count, string="Prescriptions")
    is_pharmacist = fields.Boolean(string='Pharmacist?', default=lambda *a: False)
    oeh_user_id = fields.Many2one('res.users', string='Responsible Odoo User')
    appointment_type = fields.Selection(APPOINTMENT_TYPE, string='Allow Appointment on?', default=lambda *a: 'Not on Weekly Schedule')

    _sql_constraints = [
        ('code_oeh_physician_userid_uniq', 'unique(oeh_user_id)', "Selected 'Responsible' user is already assigned to another physician !")
    ]

    @api.onchange('state_id')
    def onchange_state(self):
        if self.state_id:
            self.country_id = self.state_id.country_id.id

    @api.onchange('address_id')
    def _onchange_address(self):
        self.work_phone = self.address_id.phone
        self.mobile_phone = self.address_id.mobile

    @api.onchange('company_id')
    def _onchange_company(self):
        address = self.company_id.partner_id.address_get(['default'])
        self.address_id = address['default'] if address else False

    @api.onchange('user_id')
    def _onchange_user(self):
        self.work_email = self.user_id.email
        self.name = self.user_id.name
        self.image = self.user_id.image

    @api.multi
    def write(self, vals):
        if 'name' in vals:
           vals['name_related'] = vals['name']
        return super(OeHealthPhysician, self).write(vals)

class OeHealthPhysicianLine(models.Model):

    # Array containing different days name
    PHY_DAY = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    _name = "oeh.medical.physician.line"
    _description = "Information about doctor availability"

    name = fields.Selection(PHY_DAY, string='Available Day(s)', required=True)
    start_time = fields.Float(string='Start Time (24h format)')
    end_time = fields.Float(string='End Time (24h format)')
    physician_id = fields.Many2one('oeh.medical.physician', string='Physician', index=True, ondelete='cascade')

# Appointment Management

class OeHealthAppointment(models.Model):
    _name = 'oeh.medical.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread']

    URGENCY_LEVEL = [
                ('Normal', 'Normal'),
                ('Urgent', 'Urgent'),
                ('Medical Emergency', 'Medical Emergency'),
            ]

    PATIENT_STATUS = [
                ('Ambulatory', 'Ambulatory'),
                ('Outpatient', 'Outpatient'),
                ('Inpatient', 'Inpatient'),
            ]

    APPOINTMENT_STATUS = [
            ('Scheduled', 'Scheduled'),
            ('Completed', 'Completed'),
            ('Invoiced', 'Invoiced'),
        ]

    # Automatically detect logged in physician
    @api.multi
    def _get_physician(self):
        """Return default physician value"""
        therapist_obj = self.env['oeh.medical.physician']
        domain = [('oeh_user_id', '=', self.env.uid)]
        user_ids = therapist_obj.search(domain, limit=1)
        if user_ids:
            return user_ids.id or False
        else:
            return False

    # Calculating Appointment End date
    @api.multi
    def _get_appointment_end(self):
        for apm in self:
            end_date = False
            duration = 1
            if apm.duration:
                duration = apm.duration
            if apm.appointment_date:
                end_date = datetime.datetime.strptime(apm.appointment_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=duration)
            apm.appointment_end = end_date
        return True

    name = fields.Char(string='Appointment #', size=64, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True, readonly=True, states={'Scheduled': [('readonly', False)]})
    doctor = fields.Many2one('oeh.medical.physician', string='Physician', help="Current primary care / family doctor", domain=[('is_pharmacist','=',False)], required=True, readonly=True,states={'Scheduled': [('readonly', False)]}, default=_get_physician)
    appointment_date = fields.Datetime(string='Appointment Date', required=True, readonly=True,states={'Scheduled': [('readonly', False)]}, default=datetime.datetime.now())
    appointment_end = fields.Datetime(compute=_get_appointment_end, string='Appointment End Date', readonly=True, states={'Scheduled': [('readonly', False)]})
    duration = fields.Integer(string='Duration (Hours)', readonly=True, states={'Scheduled': [('readonly', False)]}, default=lambda *a: 1)
    institution = fields.Many2one('oeh.medical.health.center', string='Lugar de Cita', help="Medical Center", readonly=True, states={'Scheduled': [('readonly', False)]})
    institution_origin = fields.Many2one('oeh.medical.health.center', string='Hospital Origen', help="Medical Center", readonly=True, states={'Scheduled': [('readonly', False)]})
    urgency_level = fields.Selection(URGENCY_LEVEL, string='Urgency Level', readonly=True, states={'Scheduled': [('readonly', False)]}, default=lambda *a: 'Normal')
    comments = fields.Text(string='Comments', readonly=True, states={'Scheduled': [('readonly', False)]})
    patient_status = fields.Selection(PATIENT_STATUS, string='Patient Status', readonly=True, states={'Scheduled': [('readonly', False)]}, default=lambda *a: 'Inpatient')
    state = fields.Selection(APPOINTMENT_STATUS, string='State', readonly=True, default=lambda *a: 'Scheduled')
    lab_department = fields.Many2one('oeh.medical.labtest.department', string='Department')

    _order = "appointment_date desc"

    @api.model
    def create(self, vals):
        if vals.get('doctor') and vals.get('appointment_date'):
            self.check_physician_availability(vals.get('doctor'),vals.get('appointment_date'))

        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.appointment')
        vals['name'] = sequence
        health_appointment = super(OeHealthAppointment, self).create(vals)
        return health_appointment

    @api.multi
    def check_physician_availability(self,doctor,appointment_date):
        available = False
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        patient_line_obj = self.env['oeh.medical.physician.line']
        need_to_check_availability = False

        query_doctor_availability = _("select appointment_type from oeh_medical_physician where id=%s") % (doctor)
        self.env.cr.execute(query_doctor_availability)
        val = self.env.cr.fetchone()
        if val and val[0]:
            if val[0] == "On Weekly Schedule":
                need_to_check_availability = True


        #check if doctor is working on selected day of the week
        if need_to_check_availability:
            selected_day = datetime.datetime.strptime(appointment_date, DATETIME_FORMAT).strftime('%A')

            if selected_day:
                avail_days = patient_line_obj.search([('name', '=', str(selected_day)),('physician_id', '=', doctor)], limit=1)

                if not avail_days:
                    raise UserError(_('Physician is not available on selected day!'))
                else:
                    #get selected day's start and end time

                    phy_start_time = self.get_time_string(avail_days.start_time).split(':')
                    phy_end_time = self.get_time_string(avail_days.end_time).split(':')

                    user_pool = self.env['res.users']
                    user = user_pool.browse(self.env.uid)
                    tz = pytz.timezone(user.partner_id.tz) or pytz.utc

                    # get localized dates
                    appointment_date = pytz.utc.localize(datetime.datetime.strptime(appointment_date, DATETIME_FORMAT)).astimezone(tz)

                    t1 = datetime.time(int(phy_start_time[0]), int(phy_start_time[1]),0)
                    t3 = datetime.time(int(phy_end_time[0]), int(phy_end_time[1]),0)

                    #get appointment hour and minute
                    t2 = datetime.time(appointment_date.hour,appointment_date.minute,0)

                    if not (t2 > t1 and t2 < t3):
                        raise UserError(_('Physician is not available on selected time!'))
                    else:
                        available = True
        return available


    def get_time_string(self,duration):
        result =''
        currentHours = int(duration // 1)
        currentMinutes =int(round(duration % 1 * 60))
        if(currentHours <= 9):
            currentHours = "0" + str(currentHours)
        if(currentMinutes <= 9):
            currentMinutes = "0" + str(currentMinutes)
        result = str(currentHours)+":"+str(currentMinutes)
        return result

    @api.multi
    def _default_account(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        return journal.default_credit_account_id.id

    def action_appointment_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        inv_ids = []

        for acc in self:
            # Create Invoice
            if acc.patient:
                curr_invoice = {
                    'partner_id': acc.patient.partner_id.id,
                    'account_id': acc.patient.partner_id.property_account_receivable_id.id,
                    'patient': acc.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice':acc.appointment_date,
                    'origin': "Appointment # : " + acc.name,
                }

                inv_ids = invoice_obj.create(curr_invoice)
                inv_id = inv_ids.id

                if inv_ids:
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
        return {
                'domain': "[('id','=', " + str(inv_id) + ")]",
                'name': _('Appointment Invoice'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }
        return True

    @api.multi
    def set_to_completed(self):
        return self.write({'state': 'Completed'})


# Prescription Management

class OeHealthPrescriptions(models.Model):
    _name = 'oeh.medical.prescription'
    _description = 'Prescriptions'

    STATES = [
        ('Draft', 'Draft'),
        ('Invoiced', 'Invoiced'),
        ('Sent to Pharmacy', 'Sent to Pharmacy'),
    ]

    # Automatically detect logged in physician
    @api.multi
    def _get_physician(self):
        """Return default physician value"""
        therapist_obj = self.env['oeh.medical.physician']
        domain = [('oeh_user_id', '=', self.env.uid)]
        user_ids = therapist_obj.search(domain, limit=1)
        if user_ids:
            return user_ids.id or False
        else:
            return False

    name = fields.Char(string='Prescription #', size=64, readonly=True, required=True, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    doctor = fields.Many2one('oeh.medical.physician', string='Physician', domain=[('is_pharmacist','=',False)], help="Current primary care / family doctor", required=True, readonly=True, states={'Draft': [('readonly', False)]}, default=_get_physician)
    pharmacy = fields.Many2one('oeh.medical.health.center.pharmacy', 'Pharmacy', readonly=True, states={'Draft': [('readonly', False)]})
    date = fields.Datetime(string='Prescription Date', readonly=True, states={'Draft': [('readonly', False)]}, default=datetime.datetime.now())
    info = fields.Text(string='Prescription Notes', readonly=True, states={'Draft': [('readonly', False)]})
    prescription_line = fields.One2many('oeh.medical.prescription.line', 'prescription_id', string='Prescription Lines', readonly=True, states={'Draft': [('readonly', False)]})
    state = fields.Selection(STATES, 'State', readonly=True, default=lambda *a: 'Draft')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.prescription')
        vals['name'] = sequence
        health_prescription = super(OeHealthPrescriptions, self).create(vals)
        return health_prescription

    @api.multi
    def _default_account(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        return journal.default_credit_account_id.id

    def action_prescription_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        inv_ids = []

        for pres in self:
            # Create Invoice
            if pres.patient:
                curr_invoice = {
                    'partner_id': pres.patient.partner_id.id,
                    'account_id': pres.patient.partner_id.property_account_receivable_id.id,
                    'patient': pres.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice': pres.date,
                    'origin': "Prescription# : " + pres.name,
                }

                inv_ids = invoice_obj.create(curr_invoice)
                inv_id = inv_ids.id

                if inv_ids:
                    prd_account_id = self._default_account()
                    if pres.prescription_line:
                        for ps in pres.prescription_line:

                            # Create Invoice line
                            curr_invoice_line = {
                                'name': ps.name.product_id.name,
                                'product_id': ps.name.product_id.id,
                                'price_unit': ps.name.product_id.list_price,
                                'quantity': ps.qty,
                                'account_id': prd_account_id,
                                'invoice_id': inv_id,
                            }

                            inv_line_ids = invoice_line_obj.create(curr_invoice_line)

                self.write({'state': 'Invoiced'})

        return {
                'domain': "[('id','=', " + str(inv_id) + ")]",
                'name': 'Prescription Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }

    @api.multi
    def unlink(self):
        for priscription in self.filtered(lambda priscription: priscription.state not in ['Draft']):
            raise UserError(_('You can not delete a prescription which is not in "Draft" state !!'))
        return super(OeHealthPrescriptions, self).unlink()

    def action_prescription_send_to_pharmacy(self):
        pharmacy_obj = self.env["oeh.medical.health.center.pharmacy.line"]
        pharmacy_line_obj = self.env["oeh.medical.health.center.pharmacy.prescription.line"]
        res = {}
        for pres in self:
            if not pres.pharmacy:
                raise UserError(_('No pharmacy selected !!'))
            else:
                curr_pres = {
                    'name': pres.id,
                    'patient': pres.patient.id,
                    'doctor': pres.doctor.id,
                    'pharmacy_id': pres.pharmacy.id,
                }
                phy_ids = pharmacy_obj.create(curr_pres)

                if phy_ids:
                    if pres.prescription_line:
                        for ps in pres.prescription_line:

                            # Create Prescription line
                            curr_pres_line = {
                                'name': ps.name.id,
                                'indication': ps.indication.id,
                                'price_unit': ps.name.product_id.list_price,
                                'qty': ps.qty,
                                'actual_qty': ps.qty,
                                'prescription_id': phy_ids.id,
                                'state': 'Draft',
                            }

                            phy_line_ids = pharmacy_line_obj.create(curr_pres_line)

                res = self.write({'state': 'Sent to Pharmacy'})

        return True


class OeHealthPrescriptionLines(models.Model):
    _name = 'oeh.medical.prescription.line'
    _description = 'Prescription Lines'

    FREQUENCY_UNIT = [
        ('Seconds', 'Seconds'),
        ('Minutes', 'Minutes'),
        ('Hours', 'Hours'),
        ('Days', 'Days'),
        ('Weeks', 'Weeks'),
        ('When Required', 'When Required'),
    ]

    DURATION_UNIT = [
        ('Minutes', 'Minutes'),
        ('Hours', 'Hours'),
        ('Days', 'Days'),
        ('Months', 'Months'),
        ('Years', 'Years'),
        ('Indefinite', 'Indefinite'),
    ]

    prescription_id = fields.Many2one('oeh.medical.prescription', string='Prescription Reference', required=True, ondelete='cascade', index=True)
    name = fields.Many2one('oeh.medical.medicines', string='Medicines', help="Prescribed Medicines", domain=[('medicament_type','=','Medicine')], required=True)
    indication = fields.Many2one('oeh.medical.pathology', string='Indication', help="Choose a disease for this medicament from the disease list. It can be an existing disease of the patient or a prophylactic.")
    dose = fields.Integer(string='Dose', help="Amount of medicines (eg, 250 mg ) each time the patient takes it")
    dose_unit = fields.Many2one('oeh.medical.dose.unit', string='Dose Unit', help="Unit of measure for the medication to be taken")
    dose_route = fields.Many2one('oeh.medical.drug.route', string='Administration Route', help="HL7 or other standard drug administration route code.")
    dose_form = fields.Many2one('oeh.medical.drug.form','Form', help="Drug form, such as tablet or gel")
    qty = fields.Integer(string='x', help="Quantity of units (eg, 2 capsules) of the medicament", default=lambda *a: 1.0)
    common_dosage = fields.Many2one('oeh.medical.dosage', string='Frequency', help="Common / standard dosage frequency for this medicines")
    frequency = fields.Integer('Frequency')
    frequency_unit = fields.Selection(FREQUENCY_UNIT, 'Unit', index=True)
    admin_times = fields.Char(string='Admin hours', size=128, help='Suggested administration hours. For example, at 08:00, 13:00 and 18:00 can be encoded like 08 13 18')
    duration = fields.Integer(string='Treatment duration')
    duration_period = fields.Selection(DURATION_UNIT, string='Treatment period', help="Period that the patient must take the medication. in minutes, hours, days, months, years or indefinately", index=True)
    start_treatment = fields.Datetime(string='Start of treatment')
    end_treatment = fields.Datetime('End of treatment')
    info = fields.Text('Comment')
    patient = fields.Many2one('oeh.medical.patient','Patient', help="Patient Name")


# Vaccines Management
class OeHealthVaccines(models.Model):
    _name = 'oeh.medical.vaccines'
    _description = 'Vaccines'

    # Automatically detect logged in physician
    @api.multi
    def _get_physician(self):
        """Return default physician value"""
        therapist_obj = self.env['oeh.medical.physician']
        domain = [('oeh_user_id', '=', self.env.uid)]
        user_ids = therapist_obj.search(domain, limit=1)
        if user_ids:
            return user_ids.id or False
        else:
            return False

    name = fields.Many2one('oeh.medical.medicines', string='Vaccine', domain=[('medicament_type','=','Vaccine')], required=True)
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True)
    doctor = fields.Many2one('oeh.medical.physician', string='Physician', domain=[('is_pharmacist','=',False)], help="Current primary care / family doctor", required=True, default=_get_physician)
    date = fields.Datetime(string='Date', required=True, default=datetime.datetime.now())
    institution = fields.Many2one('oeh.medical.health.center', string='Institution', help="Health Center where the patient is being or was vaccinated")
    dose = fields.Integer(string='Dose #', default=lambda *a: 1)
    info = fields.Text('Observation')

    @api.onchange('patient')
    def onchange_patient(self):
        res = {}
        if self.patient:
            dose = 0
            query = _("select max(dose) from oeh_medical_vaccines where patient=%s") % (str(self.patient.id))
            self.env.cr.execute(query)
            val = self.env.cr.fetchone()
            if val and val[0]:
                dose = int(val[0]) + 1
            else:
                dose = 1
            self.dose = dose
        return res
