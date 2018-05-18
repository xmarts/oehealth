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
import datetime

# Perinantal Monitor Management
class OeHealthPerinatalMonitor(models.Model):
    _name = "oeh.medical.perinatal.monitor"
    _description = "Gyneco Perinatal Monitor"

    FETUS_POSITION = [
        ('Correct','Correct'),
        ('Occiput / Cephalic Posterior', 'Occiput / Cephalic Posterior'),
        ('Frank Breech', 'Frank Breech'),
        ('Complete Breech', 'Complete Breech'),
        ('Transverse Lie', 'Transverse Lie'),
        ('Footling Breech', 'Footling Breech'),
    ]

    name = fields.Char(string='Internal Code', size=128, required=True, readonly=True, default=lambda *a: '/')
    date = fields.Datetime(string='Date and Time', required=True, default=datetime.datetime.now())
    systolic = fields.Integer(string='Systolic Pressure')
    diastolic = fields.Integer(string='Diastolic Pressure')
    contractions = fields.Integer(string='Contractions')
    frequency = fields.Integer(string='Mother\'s Heart Frequency')
    dilation = fields.Integer(string='Cervix Dilation')
    f_frequency = fields.Integer(string='Fetus Heart Frequency')
    meconium = fields.Boolean(string='Meconium')
    bleeding = fields.Boolean(string='Bleeding')
    fundal_height = fields.Integer(string='Fundal Height')
    fetus_position = fields.Selection(FETUS_POSITION, string='Fetus Position', index=True)
    gyneco_id = fields.Many2one('oeh.medical.gyneco', string='Gynecology', ondelete='cascade')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.perinatal.monitor')
        vals['name'] = sequence or '/'
        return super(OeHealthPerinatalMonitor, self).create(vals)


# Puerperium Monitor Management
class OeHealthPuerperiumMonitor(models.Model):
    _name = "oeh.medical.puerperium.monitor"
    _description = "Gyneco Puerperium Monitor"

    LOCHIA_AMOUNT = [
        ('Normal','Normal'),
        ('Abundant', 'Abundant'),
        ('Hemorrhage', 'Hemorrhage'),
    ]

    LOCHIA_COLOR = [
        ('Rubra','Rubra'),
        ('Serosa', 'Serosa'),
        ('Alba', 'Alba'),
    ]

    LOCHIA_ODOR = [
        ('Normal','Normal'),
        ('Offensive', 'Offensive'),
    ]

    name = fields.Char(string='Internal Code', size=128, required=True, readonly=True, default=lambda *a: '/')
    date = fields.Datetime(string='Date and Time', required=True, default=datetime.datetime.now())
    systolic = fields.Integer(string='Systolic Pressure')
    diastolic = fields.Integer(string='Diastolic Pressure')
    frequency = fields.Integer(string='Heart Frequency')
    lochia_amount = fields.Selection(LOCHIA_AMOUNT, string='Lochia Amount')
    lochia_color = fields.Selection(LOCHIA_COLOR, string='Lochia Color')
    lochia_odor = fields.Selection(LOCHIA_ODOR, string='Lochia Odor')
    uterus_involution = fields.Integer(string='Fundal Height', help="Distance between the symphysis pubis and the uterine fundus (S-FD) in cm")
    temperature = fields.Float(string='Temperature')
    gyneco_id = fields.Many2one('oeh.medical.gyneco', string='Gynecology', ondelete='cascade')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.puerperium.monitor')
        vals['name'] = sequence or '/'
        return super(OeHealthPuerperiumMonitor, self).create(vals)


# Gynecology Management
class OeHealthGyneco(models.Model):
    _name = "oeh.medical.gyneco"
    _description = "Gynecology Management"

    LABOR_MODE = [
        ('Normal','Normal'),
        ('Induced', 'Induced'),
        ('C-section', 'C-section'),
    ]

    FETUS = [
        ('Correct','Correct'),
        ('Occiput / Cephalic Posterior', 'Occiput / Cephalic Posterior'),
        ('Frank Breech', 'Frank Breech'),
        ('Complete Breech', 'Complete Breech'),
        ('Transverse Lie', 'Transverse Lie'),
        ('Footling Breech','Footling Breech'),
    ]

    name = fields.Char(string='Internal Code', size=128, required=True, readonly=True, default=lambda *a: '/')
    gravida_number = fields.Integer(string='Gravida #')
    abortion = fields.Boolean(string='Abortion')
    abortion_reason = fields.Char(string='Abortion Reason', size=128)
    admission_date = fields.Datetime(string='Admission Date', help="Date when she was admitted to give birth")
    prenatal_evaluations = fields.Integer(string='# of Visit to Doctor', help="Number of visits to the doctor during pregnancy")
    labor_mode = fields.Selection(LABOR_MODE, string='Labor Starting Mode')
    gestational_weeks = fields.Integer(string='Gestational Weeks')
    gestational_days = fields.Integer(string='Gestational Days')
    fetus_presentation = fields.Selection(FETUS, string='Fetus Presentation')
    placenta_incomplete = fields.Boolean(string='Incomplete Placenta')
    placenta_retained = fields.Boolean(string='Retained Placenta')
    episiotomy = fields.Boolean(string='Episiotomy')
    vaginal_tearing = fields.Boolean(string='Vaginal Tearing')
    forceps = fields.Boolean(string='Use of Forceps')
    perinatal_ids = fields.One2many('oeh.medical.perinatal.monitor','gyneco_id', string='Perinatal')
    puerperium_ids = fields.One2many('oeh.medical.puerperium.monitor','gyneco_id', string='Puerperium')
    dismissed = fields.Datetime(string='Dismissed from Hospital')
    died_at_delivery = fields.Boolean(string='Died at Delivery Room')
    died_at_the_hospital = fields.Boolean(string='Died at the Hospital')
    died_being_transferred = fields.Boolean(string='Died being Transferred', help="The mother died being transferred to another health institution")
    notes = fields.Text(string='Notes')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', ondelete='cascade')


    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.gyneco')
        vals['name'] = sequence or '/'
        return super(OeHealthGyneco, self).create(vals)


# Inheriting Patient module to add "Gyanecology" screen reference
class OeHealthPatient(models.Model):
    _inherit = 'oeh.medical.patient'

    currently_pregnant = fields.Boolean(string='Currently Pregnant')
    fertile = fields.Boolean(string='Fertile', help="Check if patient is in fertile age")
    menarche = fields.Integer(string='Menarche Age')
    menopausal = fields.Boolean(string='Menopausal')
    menopause = fields.Integer(string='Menopause Age')
    mammography = fields.Boolean(string='Mammography', help="Check if the patient does periodic mammographys")
    mammography_last = fields.Date(string='Last Mammography', help="Enter the date of the last mammography")
    breast_self_examination = fields.Boolean(string='Breast Self-examination', help="Check if the patient does and knows how to self examine her breasts")
    pap_test = fields.Boolean(string='PAP Test', help="Check if the patient does periodic cytologic pelvic smear screening")
    pap_test_last = fields.Date(string='Last PAP Test', help="Enter the date of the last Papanicolau test")
    colposcopy = fields.Boolean(string='Colposcopy', help="Check if the patient has done a colposcopy exam")
    colposcopy_last = fields.Date('Last Colposcopy', help="Enter the date of the last colposcopy")
    gravida = fields.Integer(string='Gravida', help="Number of pregnancies")
    premature = fields.Integer(string='Premature', help="Premature Deliveries")
    abortions = fields.Integer(string='No of Abortions')
    full_term = fields.Integer(string='Full Term', help="Full term pregnancies")
    gpa = fields.Char(string='GPA', size=32, help="Gravida, Para, Abortus Notation. For example G4P3A1 : 4 Pregnancies, 3 viable and 1 abortion")
    born_alive = fields.Integer(string='Born Alive')
    deaths_1st_week = fields.Integer(string='Deceased during 1st week', help="Number of babies that die in the first week")
    deaths_2nd_week = fields.Integer(string='Deceased after 2nd week', help="Number of babies that die after the second week")
    gyneco_ids = fields.One2many('oeh.medical.gyneco', 'patient', string='Perinatal')
