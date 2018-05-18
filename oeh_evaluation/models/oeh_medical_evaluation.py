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

class OeHealthPatientEvaluation(models.Model):
    _name = 'oeh.medical.evaluation'
    _description = "Patient Evaluation"

    EVALUATION_TYPE = [
            ('Ambulatory', 'Ambulatory'),
            ('Emergency', 'Emergency'),
            ('Inpatient Admission', 'Inpatient Admission'),
            ('Pre-arraganged Appointment', 'Pre-arraganged Appointment'),
            ('Periodic Control', 'Periodic Control'),
            ('Phone Call', 'Phone Call'),
            ('Telemedicine', 'Telemedicine'),
    ]

    MOOD = [
            ('Normal', 'Normal'),
            ('Sad', 'Sad'),
            ('Fear', 'Fear'),
            ('Rage', 'Rage'),
            ('Happy', 'Happy'),
            ('Disgust', 'Disgust'),
            ('Euphoria', 'Euphoria'),
            ('Flat', 'Flat'),
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

    name = fields.Char(string='Evaluation #', size=64, readonly=True, required=True, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True)
    doctor = fields.Many2one('oeh.medical.physician', string='Physician', help="Current primary care / family doctor", domain=[('is_pharmacist','=',False)], required=True, default=_get_physician)
    appointment = fields.Many2one('oeh.medical.appointment', string='Appointment #')
    evaluation_start_date = fields.Datetime(string='Evalution Date', required=True)
    evaluation_end_date = fields.Datetime(string='Evalution End Date')
    derived_from = fields.Many2one('oeh.medical.physician', string='Physician who escalated the case')
    derived_to = fields.Many2one('oeh.medical.physician', string='Physician to whom escalated')
    evaluation_type = fields.Selection(EVALUATION_TYPE, string='Evaluation Type', required=True, index=True, default=lambda *a: 'Pre-arraganged Appointment')
    chief_complaint = fields.Char(string='Chief Complaint', size=128, help='Chief Complaint')
    notes_complaint = fields.Text(string='Complaint details')
    glycemia = fields.Float(string='Glycemia', help="Last blood glucose level. It can be approximative.")
    hba1c = fields.Float(string='Glycated Hemoglobin', help="Last Glycated Hb level. It can be approximative.")
    cholesterol_total = fields.Integer(string='Last Cholesterol',help="Last cholesterol reading. It can be approximative")
    hdl = fields.Integer(string='Last HDL', help="Last HDL Cholesterol reading. It can be approximative")
    ldl = fields.Integer(string='Last LDL', help="Last LDL Cholesterol reading. It can be approximative")
    tag = fields.Integer(string='Last TAGs', help="Triacylglycerols (triglicerides) level. It can be approximative")
    systolic = fields.Integer(string='Systolic Pressure')
    diastolic = fields.Integer(string='Diastolic Pressure')
    bpm = fields.Integer(string='Heart Rate', help="Heart rate expressed in beats per minute")
    respiratory_rate = fields.Integer(string='Respiratory Rate', help="Respiratory rate expressed in breaths per minute")
    osat = fields.Integer(string='Oxygen Saturation', help="Oxygen Saturation (arterial).")
    malnutrition = fields.Boolean(string='Malnutrition', help="Check this box if the patient show signs of malnutrition. If not associated to a disease, please encode the correspondent disease on the patient disease history. For example, Moderate protein-energy malnutrition, E44.0 in ICD-10 encoding")
    dehydration = fields.Boolean(string='Dehydration', help="Check this box if the patient show signs of dehydration. If not associated to a disease, please encode the correspondent disease on the patient disease history. For example, Volume Depletion, E86 in ICD-10 encoding")
    temperature = fields.Float(string='Temperature (celsius)')
    weight = fields.Float(string='Weight (kg)')
    height = fields.Float(string='Height (cm)')
    bmi = fields.Float(string='Body Mass Index (BMI)')
    head_circumference = fields.Float(string='Head Circumference', help="Head circumference")
    abdominal_circ = fields.Float(string='Abdominal Circumference')
    edema = fields.Boolean(string='Edema', help="Please also encode the correspondent disease on the patient disease history. For example,  R60.1 in ICD-10 encoding")
    petechiae = fields.Boolean(string='Petechiae')
    hematoma = fields.Boolean(string='Hematomas')
    cyanosis = fields.Boolean(string='Cyanosis', help="If not associated to a disease, please encode it on the patient disease history. For example,  R23.0 in ICD-10 encoding")
    acropachy = fields.Boolean(string='Acropachy', help="Check if the patient shows acropachy / clubbing")
    nystagmus = fields.Boolean(string='Nystagmus', help="If not associated to a disease, please encode it on the patient disease history. For example,  H55 in ICD-10 encoding")
    miosis = fields.Boolean(string='Miosis', help="If not associated to a disease, please encode it on the patient disease history. For example,  H57.0 in ICD-10 encoding" )
    mydriasis = fields.Boolean(string='Mydriasis', help="If not associated to a disease, please encode it on the patient disease history. For example,  H57.0 in ICD-10 encoding")
    cough = fields.Boolean(string='Cough', help="If not associated to a disease, please encode it on the patient disease history.")
    palpebral_ptosis = fields.Boolean(string='Palpebral Ptosis', help="If not associated to a disease, please encode it on the patient disease history")
    arritmia = fields.Boolean(string='Arritmias', help="If not associated to a disease, please encode it on the patient disease history")
    heart_murmurs = fields.Boolean(string='Heart Murmurs')
    heart_extra_sounds = fields.Boolean(string='Heart Extra Sounds', help="If not associated to a disease, please encode it on the patient disease history")
    jugular_engorgement = fields.Boolean(string='Tremor', help="If not associated to a disease, please encode it on the patient disease history")
    ascites = fields.Boolean(string='Ascites', help="If not associated to a disease, please encode it on the patient disease history")
    lung_adventitious_sounds = fields.Boolean(string='Lung Adventitious sounds', help="Crackles, wheezes, ronchus..")
    bronchophony = fields.Boolean(string='Bronchophony')
    increased_fremitus = fields.Boolean(string='Increased Fremitus')
    decreased_fremitus = fields.Boolean(string='Decreased Fremitus')
    jaundice = fields.Boolean(string='Jaundice', help="If not associated to a disease, please encode it on the patient disease history")
    lynphadenitis = fields.Boolean(string='Linphadenitis', help="If not associated to a disease, please encode it on the patient disease history")
    breast_lump = fields.Boolean(string='Breast Lumps')
    breast_asymmetry = fields.Boolean(string='Breast Asymmetry')
    nipple_inversion = fields.Boolean(string='Nipple Inversion')
    nipple_discharge = fields.Boolean(string='Nipple Discharge')
    peau_dorange = fields.Boolean(string='Peau d orange',help="Check if the patient has prominent pores in the skin of the breast" )
    gynecomastia = fields.Boolean(string='Gynecomastia')
    masses = fields.Boolean(string='Masses', help="Check when there are findings of masses / tumors / lumps")
    hypotonia = fields.Boolean(string='Hypotonia', help="Please also encode the correspondent disease on the patient disease history.")
    hypertonia = fields.Boolean(string='Hypertonia', help="Please also encode the correspondent disease on the patient disease history.")
    pressure_ulcers = fields.Boolean(string='Pressure Ulcers', help="Check when Decubitus / Pressure ulcers are present")
    goiter = fields.Boolean(string='Goiter')
    alopecia = fields.Boolean(string='Alopecia', help="Check when alopecia - including androgenic - is present")
    xerosis = fields.Boolean(string='Xerosis')
    erithema = fields.Boolean(string='Erithema', help="Please also encode the correspondent disease on the patient disease history.")
    loc = fields.Integer(string='Level of Consciousness', help="Level of Consciousness - on Glasgow Coma Scale :  1=coma - 15=normal")
    loc_eyes = fields.Integer(string='Level of Consciousness - Eyes', help="Eyes Response - Glasgow Coma Scale - 1 to 4", default=lambda *a: 4)
    loc_verbal = fields.Integer(string='Level of Consciousness - Verbal', help="Verbal Response - Glasgow Coma Scale - 1 to 5", default=lambda *a: 5)
    loc_motor = fields.Integer(string='Level of Consciousness - Motor', help="Motor Response - Glasgow Coma Scale - 1 to 6", default=lambda *a: 6)
    violent = fields.Boolean(string='Violent Behaviour', help="Check this box if the patient is agressive or violent at the moment")
    mood = fields.Selection(MOOD, string='Mood', index=True)
    indication = fields.Many2one('oeh.medical.pathology', string='Indication', help="Choose a disease for this medicament from the disease list. It can be an existing disease of the patient or a prophylactic.")
    orientation = fields.Boolean(string='Orientation', help="Check this box if the patient is disoriented in time and/or space")
    memory = fields.Boolean(string='Memory', help="Check this box if the patient has problems in short or long term memory")
    knowledge_current_events = fields.Boolean(string='Knowledge of Current Events', help="Check this box if the patient can not respond to public notorious events")
    judgment = fields.Boolean(string='Jugdment', help="Check this box if the patient can not interpret basic scenario solutions")
    abstraction = fields.Boolean(string='Abstraction', help="Check this box if the patient presents abnormalities in abstract reasoning")
    vocabulary = fields.Boolean(string='Vocabulary', help="Check this box if the patient lacks basic intelectual capacity, when she/he can not describe elementary objects")
    calculation_ability = fields.Boolean(string='Calculation Ability',help="Check this box if the patient can not do simple arithmetic problems")
    object_recognition = fields.Boolean(string='Object Recognition', help="Check this box if the patient suffers from any sort of gnosia disorders, such as agnosia, prosopagnosia ...")
    praxis = fields.Boolean(string='Praxis', help="Check this box if the patient is unable to make voluntary movements")
    info_diagnosis = fields.Text(string='Presumptive Diagnosis')
    directions = fields.Text(string='Plan')
    symptom_pain = fields.Boolean(string='Pain')
    symptom_pain_intensity = fields.Integer(string='Pain intensity', help="Pain intensity from 0 (no pain) to 10 (worst possible pain)")
    symptom_arthralgia = fields.Boolean(string='Arthralgia')
    symptom_myalgia = fields.Boolean(string='Myalgia')
    symptom_abdominal_pain = fields.Boolean(string='Abdominal Pain')
    symptom_cervical_pain = fields.Boolean(string='Cervical Pain')
    symptom_thoracic_pain = fields.Boolean(string='Thoracic Pain')
    symptom_lumbar_pain = fields.Boolean(string='Lumbar Pain')
    symptom_pelvic_pain = fields.Boolean(string='Pelvic Pain')
    symptom_headache = fields.Boolean(string='Headache')
    symptom_odynophagia = fields.Boolean(string='Odynophagia')
    symptom_sore_throat = fields.Boolean(string='Sore throat')
    symptom_otalgia = fields.Boolean(string='Otalgia')
    symptom_tinnitus = fields.Boolean(string='Tinnitus')
    symptom_ear_discharge = fields.Boolean(string='Ear Discharge')
    symptom_hoarseness = fields.Boolean(string='Hoarseness')
    symptom_chest_pain = fields.Boolean(string='Chest Pain')
    symptom_chest_pain_excercise = fields.Boolean(string='Chest Pain on excercise only')
    symptom_orthostatic_hypotension = fields.Boolean(string='Orthostatic hypotension', help="If not associated to a disease,please encode it on the patient disease history. For example,  I95.1 in ICD-10 encoding")
    symptom_astenia = fields.Boolean(string='Astenia')
    symptom_anorexia = fields.Boolean(string='Anorexia')
    symptom_weight_change = fields.Boolean(string='Sudden weight change')
    symptom_abdominal_distension = fields.Boolean(string='Abdominal Distension')
    symptom_hemoptysis = fields.Boolean(string='Hemoptysis')
    symptom_hematemesis = fields.Boolean(string='Hematemesis')
    symptom_epistaxis = fields.Boolean(string='Epistaxis')
    symptom_gingival_bleeding = fields.Boolean(string='Gingival Bleeding')
    symptom_rinorrhea = fields.Boolean(string='Rinorrhea')
    symptom_nausea = fields.Boolean(string='Nausea')
    symptom_vomiting = fields.Boolean(string='Vomiting')
    symptom_dysphagia = fields.Boolean(string='Dysphagia')
    symptom_polydipsia = fields.Boolean(string='Polydipsia')
    symptom_polyphagia = fields.Boolean(string='Polyphagia')
    symptom_polyuria = fields.Boolean(string='Polyuria')
    symptom_nocturia = fields.Boolean(string='Nocturia')
    symptom_vesical_tenesmus = fields.Boolean(string='Vesical Tenesmus')
    symptom_pollakiuria = fields.Boolean(string='Pollakiuiria')
    symptom_dysuria = fields.Boolean(string='Dysuria')
    symptom_stress = fields.Boolean(string='Stressed-out')
    symptom_mood_swings = fields.Boolean(string='Mood Swings')
    symptom_pruritus = fields.Boolean(string='Pruritus')
    symptom_insomnia = fields.Boolean(string='Insomnia')
    symptom_disturb_sleep = fields.Boolean(string='Disturbed Sleep')
    symptom_dyspnea = fields.Boolean(string='Dyspnea')
    symptom_orthopnea = fields.Boolean(string='Orthopnea')
    symptom_amnesia = fields.Boolean(string='Amnesia')
    symptom_paresthesia = fields.Boolean(string='Paresthesia')
    symptom_paralysis = fields.Boolean(string='Paralysis')
    symptom_syncope = fields.Boolean(string='Syncope')
    symptom_dizziness = fields.Boolean(string='Dizziness')
    symptom_vertigo = fields.Boolean(string='Vertigo')
    symptom_eye_glasses = fields.Boolean(string='Eye glasses', help="Eye glasses or contact lenses")
    symptom_blurry_vision = fields.Boolean(string='Blurry vision')
    symptom_diplopia = fields.Boolean(string='Diplopia')
    symptom_photophobia = fields.Boolean(string='Photophobia')
    symptom_dysmenorrhea = fields.Boolean(string='Dysmenorrhea')
    symptom_amenorrhea = fields.Boolean(string='Amenorrhea')
    symptom_metrorrhagia = fields.Boolean(string='Metrorrhagia')
    symptom_menorrhagia = fields.Boolean(string='Menorrhagia')
    symptom_vaginal_discharge = fields.Boolean(string='Vaginal Discharge')
    symptom_urethral_discharge = fields.Boolean(string='Urethral Discharge')
    symptom_diarrhea = fields.Boolean(string='Diarrhea')
    symptom_constipation = fields.Boolean(string='Constipation')
    symptom_rectal_tenesmus = fields.Boolean(string='Rectal Tenesmus')
    symptom_melena = fields.Boolean(string='Melena')
    symptom_proctorrhagia = fields.Boolean(string='Proctorrhagia')
    symptom_xerostomia = fields.Boolean(string='Xerostomia')
    symptom_sexual_dysfunction = fields.Boolean(string='Sexual Dysfunction')
    notes = fields.Text(string='Notes')

    @api.model
    def create(self,vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.evaluation')
        vals['name'] = sequence or '/'
        return super(OeHealthPatientEvaluation, self).create(vals)

    @api.onchange('height','weight')
    def onchange_height_weight(self):
        res = {}
        if self.height:
            self.bmi = self.weight / ((self.height/100)**2)
        else:
            self.bmi = 0
        return res

    @api.onchange('loc_motor','loc_eyes','loc_verbal')
    def onchange_loc(self):
        res = {}
        self.loc = self.loc_motor + self.loc_eyes + self.loc_verbal
        return res

# Inheriting Patient module to add "Evaluation" screen reference
class OeHealthPatient(models.Model):
    _inherit='oeh.medical.patient'

    evaluation_ids = fields.One2many('oeh.medical.evaluation', 'patient', string='Evaluation')


# Inheriting Appointment module to add "Evaluation" screen reference
class OeHealthAppointment(models.Model):
    _inherit='oeh.medical.appointment'

    evaluation_ids = fields.One2many('oeh.medical.evaluation', 'appointment', string='Evaluation', readonly=True, states={'Scheduled': [('readonly', False)]})
