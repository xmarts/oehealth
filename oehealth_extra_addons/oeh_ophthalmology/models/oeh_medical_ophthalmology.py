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
import datetime


# Ophthalmology Management

class OeHealthOphthalmology(models.Model):
    _name = "oeh.medical.ophthalmology"
    _description = "Ophthalmology Management"

    SEX = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    OPHTHO_STATUS = [
        ('Draft', 'Draft'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    SNELL_CHART = [
        ('6_6', '6/6'),
        ('6_9', '6/9'),
        ('6_12', '6/12'),
        ('6_18', '6/18'),
        ('6_24', '6/24'),
        ('6_36', '6/36'),
        ('6_60', '6/60'),
        ('5_60', '5/60'),
        ('4_60', '4/60'),
        ('3_60', '3/60'),
        ('2_60', '2/60'),
        ('1_60', '1/60'),
        ('1 Meter FC', '1 Meter FC'),
        ('1/2 Meter FC', '1/2 Meter FC'),
        ('HMCF', 'HMCF'),
        ('P/L', 'P/L'),
    ]

    NEAR_VISION_CHART = [
        ('N6', 'N6'),
        ('N8', 'N8'),
        ('N12', 'N12'),
        ('N18', 'N18'),
        ('N24', 'N24'),
        ('N36', 'N36'),
        ('N60', 'N60'),
    ]

    IOP_METHOD = [
        ('Non-contact tonometry', 'Non-contact tonometry'),
        ('Schiotz tonometry', 'Schiotz tonometry'),
        ('Goldman tonometry', 'Goldman tonometry'),
    ]


    @api.multi
    def _patient_age_at_evaluation(self):
        def compute_age_from_dates (patient_dob,patient_visit_date):
            if (patient_dob):
                dob = datetime.datetime.strptime(patient_dob,'%Y-%m-%d').date()
                visit_date = datetime.datetime.strptime(patient_visit_date,'%Y-%m-%d %H:%M:%S').date()
                delta= visit_date - dob
                years_months_days = str(delta.days // 365)+" years "+ str(delta.days%365)+" days"
            else:
                years_months_days = "No DoB !"
            return years_months_days
        result={}
        for patient_data in self:
            patient_data.computed_age = compute_age_from_dates(patient_data.patient.dob,patient_data.visit_date)
        return result

    # Automatically detect logged in physician
    def _get_physician(self):
        """Return default physician value"""
        therapist_obj = self.env['oeh.medical.physician']
        domain = [('oeh_user_id', '=', self.env.uid)]
        user_ids = therapist_obj.search(domain)
        if user_ids:
            return user_ids.id or False
        else:
            return False


    name = fields.Char(string='Visit #', size=64, readonly=True, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name",required=True, readonly=True, states={'Draft': [('readonly', False)]})
    visit_date = fields.Datetime(string='Date', help="Date of Consultation", required=True, readonly=True, states={'Draft': [('readonly', False)]}, default=lambda *a: datetime.datetime.now())
    doctor = fields.Many2one('oeh.medical.physician','Physician', domain=[('is_pharmacist','=',False)], help="Health professional / Ophthalmologist / OptoMetrist", required=True, readonly=True, states={'Draft': [('readonly', False)]}, default=_get_physician)
    rdva = fields.Selection(SNELL_CHART, string='RDVA', help="Right Eye Vision of Patient without aid", readonly=True, states={'In Progress': [('readonly', False)]})
    ldva = fields.Selection(SNELL_CHART, string='LDVA', help="Left Eye Vision of Patient without aid", readonly=True, states={'In Progress': [('readonly', False)]})
    rdva_pinhole = fields.Selection(SNELL_CHART, string='RDVA', help="Right Eye Vision Using Pin Hole", readonly=True, states={'In Progress': [('readonly', False)]})
    ldva_pinhole = fields.Selection(SNELL_CHART, string='LDVA', help="Left Eye Vision Using Pin Hole", readonly=True, states={'In Progress': [('readonly', False)]})
    rdva_aid = fields.Selection(SNELL_CHART, string='RDVA AID', help="Vision with glasses or contact lens", readonly=True, states={'In Progress': [('readonly', False)]})
    ldva_aid = fields.Selection(SNELL_CHART, string='LDVA AID', help="Vision with glasses or contact lens", readonly=True, states={'In Progress': [('readonly', False)]})
    rspherical = fields.Float(string='SPH',help='Right Eye Spherical', readonly=True, states={'In Progress': [('readonly', False)]})
    lspherical = fields.Float(string='SPH',help='Left Eye Spherical', readonly=True, states={'In Progress': [('readonly', False)]})
    rcylinder = fields.Float(string='CYL',help='Right Eye Cylinder', readonly=True, states={'In Progress': [('readonly', False)]})
    lcylinder = fields.Float(string='CYL',help='Left Eye Cylinder', readonly=True, states={'In Progress': [('readonly', False)]})
    raxis = fields.Float(string='Axis',help='Right Eye Axis', readonly=True, states={'In Progress': [('readonly', False)]})
    laxis = fields.Float(string='Axis',help='Left Eye Axis', readonly=True, states={'In Progress': [('readonly', False)]})
    rnv_add = fields.Float(string='NV Add',help='Right Eye Best Corrected NV Add', readonly=True, states={'In Progress': [('readonly', False)]})
    lnv_add = fields.Float(string='NV Add',help='Left Eye Best Corrected NV Add', readonly=True, states={'In Progress': [('readonly', False)]})
    rnv = fields.Selection(SNELL_CHART, string='RNV', help="Right Eye Near Vision", readonly=True, states={'In Progress': [('readonly', False)]})
    lnv = fields.Selection(SNELL_CHART, string='LNV', help="Left Eye Near Vision", readonly=True, states={'In Progress': [('readonly', False)]})
    rbcva_spherical = fields.Float(string='SPH',help='Right Eye Best Corrected Spherical', readonly=True, states={'In Progress': [('readonly', False)]})
    lbcva_spherical = fields.Float(string='SPH',help='Left Eye Best Corrected Spherical', readonly=True, states={'In Progress': [('readonly', False)]})
    rbcva_cylinder = fields.Float(string='CYL',help='Right Eye Best Corrected Cylinder', readonly=True, states={'In Progress': [('readonly', False)]})
    lbcva_cylinder = fields.Float(string='CYL',help='Left Eye Best Corrected Cylinder', readonly=True, states={'In Progress': [('readonly', False)]})
    rbcva_axis = fields.Float(string='Axis',help='Right Eye Best Corrected Axis', readonly=True, states={'In Progress': [('readonly', False)]})
    lbcva_axis = fields.Float(string='Axis',help='Left Eye Best Corrected Axis', readonly=True, states={'In Progress': [('readonly', False)]})
    rbcva_nv_add = fields.Float(string='BCVA - Add',help='Right Eye Best Corrected NV Add', readonly=True, states={'In Progress': [('readonly', False)]})
    lbcva_nv_add = fields.Float(string='BCVA - Add',help='Left Eye Best Corrected NV Add', readonly=True, states={'In Progress': [('readonly', False)]})
    rbcva = fields.Selection(SNELL_CHART, string='RBCVA', help="Right Eye Best Corrected VA", readonly=True, states={'In Progress': [('readonly', False)]})
    lbcva = fields.Selection(SNELL_CHART, string='LBCVA', help="Left Eye Best Corrected VA", readonly=True, states={'In Progress': [('readonly', False)]})
    rbcva_nv = fields.Selection(SNELL_CHART, string='RBCVANV', help="Right Eye Best Corrected Near Vision", readonly=True, states={'In Progress': [('readonly', False)]})
    lbcva_nv = fields.Selection(SNELL_CHART, string='LBCVANV', help="Left Eye Best Corrected Near Vision", readonly=True, states={'In Progress': [('readonly', False)]})
    notes = fields.Text(string='Notes', readonly=True, states={'Draft': [('readonly', False)],'In Progress': [('readonly', False)]})
    iop_method = fields.Selection(SNELL_CHART, string='Method', help="Tonometry / Intraocular pressure reading method", readonly=True, states={'In Progress': [('readonly', False)]})
    riop = fields.Float(string='RIOP',help='Right Intraocular Pressure in mmHg', readonly=True, states={'In Progress': [('readonly', False)]})
    liop = fields.Float(string='LIOP',help='Left Intraocular Pressure in mmHg', readonly=True, states={'In Progress': [('readonly', False)]})
    findings = fields.One2many('oeh.medical.ophthalmology.findings', 'name', string='Findings',  readonly=True, states={'In Progress': [('readonly', False)]})
    computed_age = fields.Char(compute=_patient_age_at_evaluation, size=32, string='Age during evaluation', help="Computed patient age at the moment of the surgery", readonly=True)
    state = fields.Selection(OPHTHO_STATUS, string='State', readonly=True, default=lambda *a: 'Draft')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.ophthalmology')
        vals['name'] = sequence
        return super(OeHealthOphthalmology, self).create(vals)

    @api.multi
    # Preventing deletion of a Ophthalmology details which is not in draft state
    def unlink(self):
        for opthal in self.filtered(lambda opthal: opthal.state not in ['Draft']):
            raise UserError(_('You can not delete information which is not in "Draft" state !!'))
        return super(OeHealthOphthalmology, self).unlink()

    @api.multi
    def start_evaluation(self):
        return self.write({'state': 'In Progress'})

    @api.multi
    def complete_evaluation(self):
        return self.write({'state': 'Completed'})


# Opthalmology Findings Management

class OeHealthOphthalmologyFindingslist(models.Model):
    _name = "oeh.medical.ophthalmology.findings"
    _description = "Ophthalmology Findings Management"

    STRUCTURE = [
        ('Lid', 'Lid'),
        ('Naso-lacrimal System', 'Naso-lacrimal System'),
        ('Conjunctiva', 'Conjunctiva'),
        ('Cornea', 'Cornea'),
        ('Anterior Chamber', 'Anterior Chamber'),
        ('Iris', 'Iris'),
        ('Pupil', 'Pupil'),
        ('Lens', 'Lens'),
        ('Vitreous', 'Vitreous'),
        ('Fundus Disc', 'Fundus Disc'),
        ('Macula', 'Macula'),
        ('Fundus Background', 'Fundus Background'),
        ('Fundus Vessels', 'Fundus Vessels'),
        ('Other', 'Other'),
    ]

    AFFECTED_EYE = [
        ("Right","Right"),
        ("Left","Left"),
        ("Both","Both"),
    ]

    name = fields.Many2one('oeh.medical.ophthalmology', string='Evaluation', readonly=True)
    eye_structure = fields.Selection(STRUCTURE, string='Structure', help="Affected eye structure")
    affected_eye = fields.Selection(AFFECTED_EYE, string='Eye', help="Affected eye")
    finding = fields.Char(string='Finding', size=56)