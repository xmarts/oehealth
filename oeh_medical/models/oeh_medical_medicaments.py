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


# Medicines
class OeHealthMedicines(models.Model):
    _name = 'oeh.medical.medicines'
    _description = "Information about the medicines"
    _inherits={
        'product.product': 'product_id',
    }

    MEDICAMENT_TYPE = [
        ('Medicine', 'Medicine'),
        ('Vaccine', 'Vaccine'),
    ]

    product_id = fields.Many2one('product.product', string='Related Product', required=True,ondelete='cascade', help='Product-related data of the medicines')
    therapeutic_action = fields.Char(string='Therapeutic effect', size=128, help="Therapeutic action")
    composition = fields.Text(string='Composition',help="Components")
    indications = fields.Text(string='Indication',help="Indications")
    dosage = fields.Text(string='Dosage Instructions',help="Dosage / Indications")
    overdosage = fields.Text(string='Overdosage',help="Overdosage")
    pregnancy_warning = fields.Boolean(string='Pregnancy Warning', help="Check when the drug can not be taken during pregnancy or lactancy")
    pregnancy = fields.Text(string='Pregnancy and Lactancy',help="Warnings for Pregnant Women")
    adverse_reaction = fields.Text(string='Adverse Reactions')
    storage = fields.Text(string='Storage Conditions')
    info = fields.Text(string='Extra Info')
    medicament_type = fields.Selection(MEDICAMENT_TYPE, string='Medicament Type')

# Medicaments Configuration
class OeHealthDoseUnit(models.Model):
    _name = "oeh.medical.dose.unit"
    _description = "Medical Dose Unit"
    name = fields.Char(string='Unit', size=32, required=True)
    desc = fields.Char(string='Description', size=64)

class OeHealthDrugRoute(models.Model):
    _name = "oeh.medical.drug.route"
    _description = "Medical Drug Route"
    name = fields.Char(string='Route', size=32, required=True)
    code = fields.Char(string='Code', size=64)

class OeHealthDrugForm(models.Model):
    _name = "oeh.medical.drug.form"
    _description = "Medical Dose Form"
    name = fields.Char(string='Form', size=32, required=True)
    code = fields.Char(string='Code', size=64)

class OeHealthDosage (models.Model):
    _name = "oeh.medical.dosage"
    _description = "Medicines Dosage"
    name = fields.Char(string='Frequency', size=256, help='Common dosage frequency')
    code = fields.Char(string='Code', size=64, help='Dosage Code, such as SNOMED, 229798009 = 3 times per day')
    abbreviation = fields.Char(string='Abbreviation', size=64, help='Dosage abbreviation, such as tid in the US or tds in the UK')
