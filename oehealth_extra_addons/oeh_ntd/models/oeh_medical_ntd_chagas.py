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

from odoo import api, fields, models
import datetime

class OeHealthNTDChagas(models.Model):
    _name = 'oeh.medical.ntd.chagas'
    _description = 'Chagas DU Entomological Survey'

    DU_STATUS = [
        ('Initial', 'Initial'),
        ('Unchanged', 'Unchanged'),
        ('Improved', 'Improved'),
        ('Worsen', 'Worsen'),
    ]

    VECTOR = [
        ('T. infestans', 'T. infestans'),
        ('T. brasilensis', 'T. brasilensis'),
        ('R. prolixus', 'R. prolixus'),
        ('T. dimidiata', 'T. dimidiata'),
        ('P. megistus', 'P. megistus'),
    ]

    name = fields.Char(string='Survey Code', size=128, readonly=True, default=lambda *a: '/')
    du = fields.Many2one('oeh.medical.domiciliary.unit', string='Domiciliary Unit', required=True)
    survey_date = fields.Datetime(string='Survey Date', required=True, default=datetime.datetime.now())
    du_status = fields.Selection(DU_STATUS, string='Status', help="DU status compared to last visit", required=True)
    triatomines = fields.Boolean(string='Triatomines', help="Check this box if triatomines were found")
    vector = fields.Selection(VECTOR, string='Vector')
    nymphs = fields.Boolean(string='Nymphs', help="Check this box if triatomine nymphs were found")
    t_in_house = fields.Boolean(string='Domiciliary', help="Check this box if triatomines were found inside the house")
    t_peri = fields.Boolean(string='Peri-Domiciliary', help="Check this box if triatomines were found in the peridomiciliary area")
    dfloor = fields.Boolean(string='Floor', help="Current floor can host triatomines")
    dwall = fields.Boolean(string='Walls', help="Wall materials or state can host triatomines")
    droof = fields.Boolean(string='Roof', help="Roof materials or state can host triatomines")
    dperi = fields.Boolean(string='Peri-domicilary', help="Peri domiciliary area can host triatomines")
    bugtraps = fields.Boolean(string='Bug traps', help="The DU has traps to detect triatomines")
    du_fumigation = fields.Boolean(string='Fumigation', help="The DU has been fumigated")
    fumigation_date = fields.Date(string='Fumigation Date',help="Last Fumigation Date")
    du_paint = fields.Boolean(string='Insecticide Paint', help="The DU has been treated with insecticide-containing paint")
    paint_date = fields.Date(string='Paint Date', help="Last Paint Date")
    observations = fields.Text(string='Observations')
    next_survey_date = fields.Date(string='Next survey')

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.ntd.chagas')
        vals['name'] = sequence
        return super(OeHealthNTDChagas, self).create(vals)