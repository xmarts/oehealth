# -*- encoding: utf-8 -*-
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
import calendar
import time
import datetime

class OeHealthSurgeryRCRI(models.Model):
    _name = "oeh.medical.surgery.rcri"
    _description = "Revised Cardiac Risk Index"

    RCRI_CLASS = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
    ]

    @api.multi
    def get_rcri_name(self):
        result = {}
        rcri_name = ''
        for rc in self:
            rcri_name = 'Points: ' + str(rc.rcri_total) + ' (Class ' + str(rc.rcri_class) + ')'
            rc.name = rcri_name
        return result

    name = fields.Char(compute=get_rcri_name, string="RCRI", size=64)
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name",required=True)
    doctor = fields.Many2one('oeh.medical.physician', string='Physician', domain=[('is_pharmacist','=',False)], help="Health professional / Cardiologist who signed the assesment RCRI")
    rcri_date = fields.Datetime('Date', required=True, default=lambda *a: datetime.datetime.now())
    rcri_high_risk_surgery = fields.Boolean(string='High Risk surgery', help='Includes andy suprainguinal vascular, intraperitoneal or intrathoracic procedures')
    rcri_ischemic_history = fields.Boolean(string='History of Ischemic heart disease', help='History of MI or a positive exercise test, current complaint of chest pain considered to be secondary to myocardial ischemia, use of nitrate therapy, or ECG with pathological Q waves; do not count prior coronary revascularization procedure unless one of the other criteria for ischemic heart disease is present"')
    rcri_congestive_history = fields.Boolean(string='History of Congestive heart disease')
    rcri_diabetes_history = fields.Boolean(string='Preoperative Diabetes', help="Diabetes Mellitus requiring treatment with Insulin")
    rcri_cerebrovascular_history = fields.Boolean(string='History of Cerebrovascular disease')
    rcri_kidney_history = fields.Boolean(string='Preoperative Kidney disease', help="Preoperative serum creatinine >2.0 mg/dL (177 mol/L)")
    rcri_total = fields.Integer(string='Score', help='Points 0: Class I Very Low (0.4% complications)\n'
    'Points 1: Class II Low (0.9% complications)\n'
    'Points 2: Class III Moderate (6.6% complications)\n'
    'Points 3 or more : Class IV High (>11% complications)', default=lambda *a: 0)
    rcri_class = fields.Selection(RCRI_CLASS, string='RCRI Class', required=True, default=lambda *a: 'I')

    @api.onchange('rcri_high_risk_surgery', 'rcri_ischemic_history', 'rcri_congestive_history', 'rcri_diabetes_history', 'rcri_cerebrovascular_history', 'rcri_kidney_history')
    def on_change_with_rcri(self):
        total = 0
        rcri_class = 'I'
        if self.rcri_high_risk_surgery:
            total = total + 1
        if self.rcri_ischemic_history:
            total = total + 1
        if self.rcri_congestive_history:
            total = total + 1
        if self.rcri_diabetes_history:
            total = total + 1
        if self.rcri_kidney_history:
            total = total + 1
        if self.rcri_cerebrovascular_history:
            total = total + 1

        self.rcri_total = total

        if total == 1:
            rcri_class = 'II'
        if total == 2:
            rcri_class = 'III'
        if (total > 2):
            rcri_class = 'IV'

        self.rcri_class = rcri_class


class OeHealthSurgeryTeam(models.Model):
    _name = "oeh.medical.surgery.team"
    _description = "Surgery Team"

    name = fields.Many2one('oeh.medical.surgery', string='Surgery')
    team_member = fields.Many2one('oeh.medical.physician', string='Member', help="Health professional that participated on this surgery", domain=[('is_pharmacist','=',False)], required=True)
    role = fields.Many2one('oeh.medical.speciality', string='Role')
    notes = fields.Char(string='Notes')

    @api.onchange('team_member')
    def onchange_team_member(self):
        if self.team_member:
            if self.team_member.speciality:
                self.role = self.team_member.speciality.id



class OeHealthSurgerySupply(models.Model):
    _name = "oeh.medical.surgery.supply"
    _description = "Supplies related to the surgery"

    name = fields.Many2one('oeh.medical.surgery', string='Surgery')
    qty = fields.Integer(string='Initial required quantity', required=True, help="Initial required quantity", default=lambda *a: 0)
    supply = fields.Many2one('product.product', string='Supply', required=True, help="Supply to be used in this surgery")
    notes = fields.Char(string='Notes')
    qty_used = fields.Integer(string='Actual quantity used', required=True, help="Actual quantity used", default=lambda *a: 0)


class OeHealthSurgery(models.Model):
    _name = "oeh.medical.surgery"
    _description = "Surgerical Management"

    CLASSIFICATION = [
        ('Optional', 'Optional'),
        ('Required', 'Required'),
        ('Urgent', 'Urgent'),
        ('Emergency', 'Emergency'),
    ]

    STATES = [
        ('Draft', 'Draft'),
        ('Confirmed', 'Confirmed'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
        ('Signed', 'Signed'),
        ('Cancelled', 'Cancelled'),
    ]

    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Female -> Male','Female -> Male'),
        ('Male -> Female','Male -> Female'),
    ]

    PREOP_MALLAMPATI = [
        ('Class 1', 'Class 1: Full visibility of tonsils, uvula and soft '
                    'palate'),
        ('Class 2', 'Class 2: Visibility of hard and soft palate, '
                    'upper portion of tonsils and uvula'),
        ('Class 3', 'Class 3: Soft and hard palate and base of the uvula are '
                    'visible'),
        ('Class 4', 'Class 4: Only Hard Palate visible'),
    ]

    PREOP_ASA = [
        ('PS 1', 'PS 1 : Normal healthy patient'),
        ('PS 2', 'PS 2 : Patients with mild systemic disease'),
        ('PS 3', 'PS 3 : Patients with severe systemic disease'),
        ('PS 4', 'PS 4 : Patients with severe systemic disease that is'
            ' a constant threat to life '),
        ('PS 5', 'PS 5 : Moribund patients who are not expected to'
            ' survive without the operation'),
        ('PS 6', 'PS 6 : A declared brain-dead patient who organs are'
            ' being removed for donor purposes'),
    ]

    SURGICAL_WOUND = [
        ('I', 'Clean . Class I'),
        ('II', 'Clean-Contaminated . Class II'),
        ('III', 'Contaminated . Class III'),
        ('IV', 'Dirty-Infected . Class IV'),
    ]

    @api.multi
    def _surgery_duration(self):
        for su in self:
            if su.surgery_end_date and su.surgery_date:
                surgery_date = 1.0*calendar.timegm(time.strptime(su.surgery_date, "%Y-%m-%d %H:%M:%S"))
                surgery_end_date = 1.0*calendar.timegm(time.strptime(su.surgery_end_date, "%Y-%m-%d %H:%M:%S"))
                duration = (surgery_end_date - surgery_date)/3600
                su.surgery_length = duration
        return True

    @api.multi
    def _patient_age_at_surgery(self):
        def compute_age_from_dates(patient_dob,patient_surgery_date):
            if (patient_dob):
                dob = datetime.datetime.strptime(patient_dob,'%Y-%m-%d').date()
                surgery_date = datetime.datetime.strptime(patient_surgery_date,'%Y-%m-%d %H:%M:%S').date()
                delta= surgery_date - dob
                years_months_days = str(delta.days // 365)+" years "+ str(delta.days%365)+" days"
            else:
                years_months_days = "No DoB !"
            return years_months_days
        result={}
        for patient_data in self:
            patient_data.computed_age = compute_age_from_dates(patient_data.patient.dob,patient_data.surgery_date)
        return result

    @api.multi
    def _get_surgeon(self):
        """Return default physician value"""
        therapist_obj = self.env['oeh.medical.physician']
        domain = [('oeh_user_id', '=', self.env.uid)]
        user_ids = therapist_obj.search(domain)
        if user_ids:
            return user_ids.id or False
        else:
            return False

    name = fields.Char(string='Surgery #',size=64, readonly=True, required=True, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name",required=True, readonly=True,states={'Draft': [('readonly', False)]})
    admission = fields.Many2one('oeh.medical.appointment', string='Admission', help="Patient Name", readonly=True,states={'Draft': [('readonly', False)]})
    procedures = fields.Many2many('oeh.medical.procedure', 'oeh_surgery_procedure_rel', 'surgery_id', 'procedure_id', string='Procedures', help="List of the procedures in the surgery. Please enter the first one as the main procedure", readonly=True,states={'In Progress': [('readonly', False)]})
    pathology = fields.Many2one('oeh.medical.pathology', string='Condition', help="Base Condition / Reason", readonly=True,states={'Draft': [('readonly', False)]})
    classification = fields.Selection(CLASSIFICATION, string='Urgency', help="Urgency level for this surgery", required=True, readonly=True,states={'Draft': [('readonly', False)]})
    surgeon = fields.Many2one('oeh.medical.physician', string='Surgeon', help="Surgeon who did the procedure", domain=[('is_pharmacist','=',False)], required=True, readonly=True,states={'Draft': [('readonly', False)]}, default=_get_surgeon)
    anesthetist = fields.Many2one('oeh.medical.physician', string='Anesthetist', help="Anesthetist in charge", domain=[('is_pharmacist','=',False)], required=True, readonly=True,states={'Draft': [('readonly', False)]})
    surgery_date = fields.Datetime(string='Start date & time', help="Start of the Surgery", readonly=True,states={'Draft': [('readonly', False)]}, default=lambda *a: datetime.datetime.now())
    surgery_end_date = fields.Datetime(string='End date & time', help="End of the Surgery", readonly=True,states={'Draft': [('readonly', False)]})
    surgery_length = fields.Float(compute=_surgery_duration, string='Duration (Hour:Minute)', help="Length of the surgery", readonly=True,states={'Draft': [('readonly', False)]})
    computed_age = fields.Char(compute=_patient_age_at_surgery, size=32, string='Age during surgery', help="Computed patient age at the moment of the surgery", readonly=True,states={'Draft': [('readonly', False)]})
    gender = fields.Selection(GENDER, string='Gender', readonly=True,states={'Draft': [('readonly', False)]})
    signed_by = fields.Many2one('res.users', string='Signed by', help="Health Professional that signed this surgery document")
    description = fields.Text(string='Description', readonly=True, states={'Draft': [('readonly', False)], 'Confirmed': [('readonly', False)], 'In Progress': [('readonly', False)]})
    preop_mallampati = fields.Selection(PREOP_MALLAMPATI, string='Mallampati Score', readonly=True,states={'Draft': [('readonly', False)]})
    preop_bleeding_risk = fields.Boolean(string='Risk of Massive bleeding', help="Patient has a risk of losing more than 500 ml in adults of over 7ml/kg in infants. If so, make sure that intravenous access and fluids are available", readonly=True,states={'Draft': [('readonly', False)]})
    preop_oximeter = fields.Boolean(string='Pulse Oximeter in place', help="Pulse oximeter is in place and functioning", readonly=True, states={'Draft': [('readonly', False)]})
    preop_site_marking = fields.Boolean(string='Surgical Site Marking', help="The surgeon has marked the surgical incision", readonly=True, states={'Draft': [('readonly', False)]})
    preop_antibiotics = fields.Boolean(string='Antibiotic Prophylaxis', help="Prophylactic antibiotic treatment within the last 60 minutes", readonly=True, states={'Draft': [('readonly', False)]})
    preop_sterility = fields.Boolean(string='Sterility Confirmed', help="Nursing team has confirmed sterility of the devices and room", readonly=True, states={'Draft': [('readonly', False)]})
    preop_asa = fields.Selection(PREOP_ASA, string='ASA PS', help="ASA pre-operative Physical Status", readonly=True,states={'Draft': [('readonly', False)]})
    preop_rcri = fields.Many2one('oeh.medical.surgery.rcri', string='RCRI', help='Patient Revised Cardiac Risk Index\n Points 0: Class I Very Low (0.4% complications)\n Points 1: Class II Low (0.9% complications)\n Points 2: Class III Moderate (6.6% complications)\n Points 3 or more : Class IV High (>11% complications)', readonly=True,states={'Draft': [('readonly', False)]})
    surgical_wound = fields.Selection(SURGICAL_WOUND, string='Surgical Wound', readonly=True,states={'Draft': [('readonly', False)]})
    info = fields.Text(string='Extra Info', readonly=True, states={'Draft': [('readonly', False)], 'Confirmed': [('readonly', False)], 'In Progress': [('readonly', False)]})
    anesthesia_report = fields.Text(string='Anesthesia Report', readonly=True, states={'Draft': [('readonly', False)], 'Confirmed': [('readonly', False)], 'In Progress': [('readonly', False)]})
    institution = fields.Many2one('oeh.medical.health.center', string='Health Center',help="Health Center", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    postoperative_dx = fields.Many2one('oeh.medical.pathology', string='Post-op dx', help="Post-operative diagnosis", readonly=True,states={'Draft': [('readonly', False)]})
    surgery_team = fields.One2many('oeh.medical.surgery.team', 'name', string='Team Members', help="Professionals Involved in the surgery", readonly=True, states={'Draft': [('readonly', False)]})
    supplies = fields.One2many('oeh.medical.surgery.supply', 'name', string='Supplies', help="List of the supplies required for the surgery", readonly=True, states={'In Progress': [('readonly', False)]})
    building = fields.Many2one('oeh.medical.health.center.building', string='Building', help="Building of the selected Health Center", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    operating_room = fields.Many2one('oeh.medical.health.center.ot', string='Operation Theater', required=True, readonly=True, states={'Draft': [('readonly', False)]})
    state = fields.Selection(STATES, string='State',readonly=True, default=lambda *a: 'Draft')


    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.surgery')
        vals['name'] = sequence
        return super(OeHealthSurgery, self).create(vals)

    @api.multi
    def action_surgery_confirm(self):
        for surgery in self:
            if surgery.operating_room:
                query = _("update oeh_medical_health_center_ot set state='Reserved' where id=%s")%(str(surgery.operating_room.id))
                self.env.cr.execute(query)
        return self.write({'state': 'Confirmed'})

    @api.multi
    def action_surgery_start(self):
        for surgery in self:
            if surgery.operating_room:
                query = _("update oeh_medical_health_center_ot set state='Occupied' where id=%s")%(str(surgery.operating_room.id))
                self.env.cr.execute(query)
        return self.write({'state': 'In Progress', 'surgery_date': datetime.datetime.now()})

    @api.multi
    def action_surgery_cancel(self):
        for surgery in self:
            if surgery.operating_room:
                query = _("update oeh_medical_health_center_ot set state='Free' where id=%s")%(str(surgery.operating_room.id))
                self.env.cr.execute(query)
        return self.write({'state': 'Cancelled'})

    @api.multi
    def action_surgery_set_to_draft(self):
        return self.write({'state': 'Draft'})

    @api.multi
    def action_surgery_end(self):
        for surgery in self:
            if surgery.operating_room:
                query = _("update oeh_medical_health_center_ot set state='Free' where id=%s")%(str(surgery.operating_room.id))
                self.env.cr.execute(query)
        return self.write({'state': 'Done', 'surgery_end_date': datetime.datetime.now()})

    @api.multi
    def action_surgery_sign(self):
        phy_obj = self.env["oeh.medical.physician"]
        domain = [('oeh_user_id', '=', self.env.uid)]
        user_ids = phy_obj.search(domain)
        if user_ids:
            self.signed_by = self.env.uid or False
            self.state = 'Signed'
        else:
            raise UserError(_('No physician associated to logged in user'))


# Inheriting Patient module to add "Surgeries" screen reference
class OeHealthPatient(models.Model):
    _inherit='oeh.medical.patient'
    pediatrics_surgery_ids = fields.One2many('oeh.medical.surgery', 'patient', string='Surgeries')


