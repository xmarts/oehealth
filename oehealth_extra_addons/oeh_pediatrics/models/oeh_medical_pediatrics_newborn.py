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

class OeHealthPediatricsNewBorn(models.Model):
    _name = "oeh.medical.pediatrics.newborn"
    _inherits={
        'res.partner': 'partner_id',
    }

    SEX = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    PEDIA_STATUS = [
        ('Draft', 'Draft'),
        ('Signed', 'Signed'),
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

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade', help='Partner-related data of the patient')
    newborn_code = fields.Char(string='Newborn ID', size=256, readonly=True, default=lambda *a: '/')
    mother = fields.Many2one('oeh.medical.patient', string='Mother', domain=[('sex','=','Female')], required=True, readonly=True, states={'Draft': [('readonly', False)]})
    birth_date = fields.Datetime(string='Date of Birth', required=True, help="Date and Time of birth", readonly=True, states={'Draft': [('readonly', False)]}, default=lambda *a: datetime.datetime.now())
    sex = fields.Selection(SEX, string='Sex', required=True, help="Sex at birth. It might differ from the current patient gender. This is the biological sex.", readonly=True, states={'Draft': [('readonly', False)]})
    cephalic_perimeter = fields.Integer(string='Cephalic Perimeter (CP)', help="Cephalic Perimeter in centimeters (cm)", readonly=True, states={'Draft': [('readonly', False)]})
    length = fields.Integer(string='Length (in)', help="Length in centimeters (cm)", readonly=True, states={'Draft': [('readonly', False)]})
    weight = fields.Float(string='Weight (pound or kg)', help="Weight in grams (g)", readonly=True, states={'Draft': [('readonly', False)]})
    apgar_scores = fields.One2many('oeh.medical.pediatrics.neonatal.apgar', 'name', 'APGAR scores', readonly=True, states={'Draft': [('readonly', False)]})
    meconium = fields.Boolean(string='Meconium', readonly=True, states={'Draft': [('readonly', False)]})
    congenital_diseases = fields.Many2one('oeh.medical.pathology', string='Congenital Diseases', help="Choose a disease for this medicament from the disease list. It can be an existing disease of the patient or a prophylactic.", states={'Draft': [('readonly', False)]})
    reanimation_stimulation = fields.Boolean(string='Stimulation', readonly=True, states={'Draft': [('readonly', False)]})
    reanimation_aspiration = fields.Boolean(string='Aspiration', readonly=True, states={'Draft': [('readonly', False)]})
    reanimation_intubation = fields.Boolean(string='Intubation', readonly=True, states={'Draft': [('readonly', False)]})
    reanimation_mask = fields.Boolean(string='Mask', readonly=True, states={'Draft': [('readonly', False)]})
    reanimation_oxygen = fields.Boolean(string='Oxygen', readonly=True, states={'Draft': [('readonly', False)]})
    test_vdrl = fields.Boolean(string='VDRL', readonly=True, states={'Draft': [('readonly', False)]})
    test_toxo = fields.Boolean(string='Toxoplasmosis', readonly=True, states={'Draft': [('readonly', False)]})
    test_chagas = fields.Boolean(string='Chagas', readonly=True, states={'Draft': [('readonly', False)]})
    test_billirubin = fields.Boolean(string='Billirubin', readonly=True, states={'Draft': [('readonly', False)]})
    test_audition = fields.Boolean(string='Audition', readonly=True, states={'Draft': [('readonly', False)]})
    test_metabolic = fields.Boolean(string='Metabolic ("heel stick screening")', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_ortolani = fields.Boolean(string='Positive Ortolani', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_barlow = fields.Boolean(string='Positive Barlow', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_hernia = fields.Boolean(string='Hernia', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_ambiguous_genitalia = fields.Boolean(string='Ambiguous Genitalia', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_erbs_palsy = fields.Boolean(string='Erbs Palsy', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_hematoma = fields.Boolean(string='Hematomas', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_talipes_equinovarus = fields.Boolean(string='Talipes Equinovarus', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_polydactyly = fields.Boolean(string='Polydactyly', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_syndactyly = fields.Boolean(string='Syndactyly', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_moro_reflex = fields.Boolean(string='Moro Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_grasp_reflex = fields.Boolean(string='Grasp Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_stepping_reflex = fields.Boolean(string='Stepping Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_babinski_reflex = fields.Boolean(string='Babinski Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_blink_reflex = fields.Boolean(string='Blink Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_sucking_reflex = fields.Boolean(string='Sucking Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_swimming_reflex = fields.Boolean(string='Swimming Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_tonic_neck_reflex = fields.Boolean(string='Tonic Neck Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_rooting_reflex = fields.Boolean(string='Rooting Reflex', readonly=True, states={'Draft': [('readonly', False)]})
    neonatal_palmar_crease = fields.Boolean(string='Transversal Palmar Crease', readonly=True, states={'Draft': [('readonly', False)]})
    medication = fields.Many2one('oeh.medical.medicines', string='Medicines', help="Prescribed Medicines", domain=[('medicament_type','=','Medicine')], readonly=True, states={'Draft': [('readonly', False)]})
    doctor = fields.Many2one('oeh.medical.physician', string='Doctor in charge', readonly=True, states={'Draft': [('readonly', False)]}, default=_get_physician)
    signed_by = fields.Many2one('oeh.medical.physician', string='Signed by', readonly=True, states={'Draft': [('readonly', False)]})
    dismissed = fields.Datetime(string='Discharged', readonly=True, states={'Draft': [('readonly', False)]})
    notes = fields.Text(string='Notes', readonly=True, states={'Draft': [('readonly', False)]})
    bd = fields.Boolean(string='Stillbirth', readonly=True, states={'Draft': [('readonly', False)]})
    died_at_delivery = fields.Boolean(string='Died at delivery room', readonly=True, states={'Draft': [('readonly', False)]})
    died_at_the_hospital = fields.Boolean(string='Died at the hospital', readonly=True, states={'Draft': [('readonly', False)]})
    died_being_transferred = fields.Boolean(string='Died being transferred', readonly=True, states={'Draft': [('readonly', False)]})
    time_of_death = fields.Datetime(string='Time of Death', readonly=True, states={'Draft': [('readonly', False)]})
    cause_of_death = fields.Many2one('oeh.medical.pathology', string='Cause of Death', readonly=True, states={'Draft': [('readonly', False)]})
    institution = fields.Many2one('oeh.medical.health.center', string='Birth at Health Center', required=True, readonly=True, states={'Draft': [('readonly', False)]})
    state = fields.Selection(PEDIA_STATUS, string='State', readonly=True, default=lambda *a: 'Draft')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.pediatrics.newborn')
        vals['newborn_code'] = sequence
        vals['is_baby'] = True
        return super(OeHealthPediatricsNewBorn, self).create(vals)

    @api.multi
    def sign_newborn(self):
        signed_by = []
        for nb in self:
            therapist_obj = self.env['oeh.medical.physician']
            domain = [('oeh_user_id', '=', self.env.uid)]
            user_ids = therapist_obj.search(domain)
            if user_ids:
                signed_by = user_ids.id or False
            else:
                raise UserError(_('Correct Physician ID not found to complete the signing process !!'))
        return self.write({'state': 'Signed', 'signed_by': signed_by})


class OeHealthPediatricsAPGAR(models.Model):
    _name = "oeh.medical.pediatrics.neonatal.apgar"
    _description = "Neonatal APGAR Score"

    APGAR_APPEARANCE = [
        ('0', 'Central Cyanosis'),
        ('1', 'Acrocyanosis'),
        ('2', 'No Cyanosis'),
    ]

    APGAR_PULSE = [
        ('0', 'Absent'),
        ('1', '< 100'),
        ('2', '> 100'),
    ]

    APGAR_GRIMACE = [
        ('0', 'No response to stimulation'),
        ('1', 'Grimace when stimulated'),
        ('2', 'Cry or pull away when stimulated'),
    ]

    APGAR_ACTIVITY = [
        ('0', 'None'),
        ('1', 'Some flexion'),
        ('2', 'Flexed arms and legs'),
    ]

    APGAR_RESPIRATION = [
        ('0', 'Absent'),
        ('1', 'Weak / Irregular'),
        ('2', 'Strong'),
    ]

    name = fields.Many2one('oeh.medical.pediatrics.newborn', string='Newborn ID')
    apgar_minute = fields.Integer(string='Minute', required=True)
    apgar_appearance = fields.Selection(APGAR_APPEARANCE, string='Appearance', required=True)
    apgar_pulse = fields.Selection(APGAR_PULSE, string='Pulse', required=True)
    apgar_grimace = fields.Selection(APGAR_GRIMACE, string='Grimace', required=True)
    apgar_activity = fields.Selection(APGAR_ACTIVITY, string='Activity', required=True)
    apgar_respiration = fields.Selection(APGAR_RESPIRATION, string='Respiration', required=True)
    apgar_score = fields.Integer(string='APGAR Score', required=True, default=lambda *a: 0)


    @api.onchange('apgar_appearance','apgar_pulse','apgar_grimace','apgar_activity','apgar_respiration')
    def on_change_with_apgar_score(self):
        apgar_appearance = self.apgar_appearance or '0'
        apgar_pulse = self.apgar_pulse or '0'
        apgar_grimace = self.apgar_grimace or '0'
        apgar_activity = self.apgar_activity or '0'
        apgar_respiration = self.apgar_respiration or '0'

        self.apgar_score = int(apgar_appearance) + int(apgar_pulse) + \
            int(apgar_grimace) + int(apgar_activity) + int(apgar_respiration)