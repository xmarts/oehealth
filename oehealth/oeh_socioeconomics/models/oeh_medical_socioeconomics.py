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

# Occupation Master table
class OeHealthOccupations(models.Model):
    _name = "oeh.medical.occupation"

    name = fields.Char(string='Occupation', size=128, required=True)
    code = fields.Char(string='Code', size=128)

    _order = 'code'
    _sql_constraints = [
            ('name_uniq', 'unique (name)', 'The occupation name must be unique !')]

# Inherit Patient screen to add Socioeconomics fields

class OeHealthPatient(models.Model):
    _inherit = 'oeh.medical.patient'

    SOCIO_STATUS = [
        ('Lower', 'Lower'),
        ('Lower-middle', 'Lower-middle'),
        ('Middle', 'Middle'),
        ('Middle-upper', 'Middle-upper'),
        ('Higher', 'Higher'),
    ]

    EDUCATION_LEVEL = [
        ('None', 'None'),
        ('Incomplete Primary School', 'Incomplete Primary School'),
        ('Primary School', 'Primary School'),
        ('Incomplete Secondary School', 'Incomplete Secondary School'),
        ('Secondary School', 'Secondary School'),
        ('University', 'University'),
    ]

    HOUSING_CONDITION = [
        ('Shanty, deficient sanitary conditions', 'Shanty, deficient sanitary conditions'),
        ('Small, crowded but with good sanitary conditions', 'Small, crowded but with good sanitary conditions'),
        ('Comfortable and good sanitary conditions', 'Comfortable and good sanitary conditions'),
        ('Roomy and excellent sanitary conditions', 'Roomy and excellent sanitary conditions'),
        ('Luxury and excellent sanitary conditions', 'Luxury and excellent sanitary conditions'),
    ]

    APGAR_HELP = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_DISCUSSION = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_DESICIONS = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_TIMESHARING = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    APGAR_AFFECTION = [
        ('None', 'None'),
        ('Moderately', 'Moderately'),
        ('Very much', 'Very much'),
    ]

    INCOME = [
        ('High', 'High'),
        ('Medium / Average', 'Medium / Average'),
        ('Low', 'Low'),
    ]

    socioeconomics = fields.Selection(SOCIO_STATUS, string='Socioeconomics', help="SES - Socioeconomic Status")
    education_level = fields.Selection(EDUCATION_LEVEL, string='Education Level')
    housing_condition = fields.Selection(HOUSING_CONDITION, string='Housing conditions', help="Housing and sanitary living conditions")
    hostile_area = fields.Boolean(string='Hostile Area', help="Check this box if the patient lives in a zone of high hostility (eg, war)")
    sewers = fields.Boolean(string='Sanitary Sewers')
    water = fields.Boolean(string='Running Water')
    trash = fields.Boolean(string='Trash recollection')
    electricity = fields.Boolean(string='Electrical supply')
    gas = fields.Boolean(string='Gas supply')
    telephone = fields.Boolean(string='Telephone')
    television = fields.Boolean(string='Television')
    internet = fields.Boolean(string='Internet')
    single_parent = fields.Boolean(string='Single parent family')
    domestic_violence = fields.Boolean(string='Domestic violence')
    working_children = fields.Boolean(string='Working children')
    teenage_pregnancy = fields.Boolean(string='Teenage pregnancy')
    sexual_abuse = fields.Boolean(string='Sexual abuse')
    drug_addiction = fields.Boolean(string='Drug addiction')
    school_withdrawal = fields.Boolean(string='School withdrawal')
    prison_past = fields.Boolean(string='Has been in prison')
    prison_current = fields.Boolean(string='Is currently in prison')
    relative_in_prison = fields.Boolean(string='Relative in prison', help="Check if someone from the nuclear family - parents / sibblings  is or has been in prison")
    info = fields.Text(string="Extra info")
    apgar_help = fields.Selection(APGAR_HELP, string='Family Help', help="Is the patient satisfied with the level of help coming from the family when there is a problem ?")
    apgar_discussion = fields.Selection(APGAR_DISCUSSION, string='Family discussions on problems', help="Is the patient satisfied with the level talking over the problems as family ?")
    apgar_decision = fields.Selection(APGAR_DESICIONS, string='Family decision ability', help="Is the patient satisfied with the level of making important decisions as a group ?")
    apgar_timesharing = fields.Selection(APGAR_TIMESHARING, string='Family time sharing', help="Is the patient satisfied with the level of time that they spend together ?")
    apgar_affection = fields.Selection(APGAR_AFFECTION, string='Family affection',help="Is the patient satisfied with the level of affection coming from the family ?")
    income = fields.Selection(INCOME, string='Income (Monthly)', help="Patient's monthly income")
    occupation = fields.Many2one('oeh.medical.occupation', string='Occupation')
    works_at_home = fields.Boolean(string='Works at home',help="Check if the patient works at his / her house")
    hours_outside = fields.Integer(string='Hours stay outside home', help="Number of hours a day the patient spend outside the house")
