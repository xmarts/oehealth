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

# Insurance Types

class OeHealthInsuranceType(models.Model):
    _name = 'oeh.medical.insurance.type'
    _description = "Insurance Types"

    name = fields.Char(string='Types', size=256, required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The insurance type must be unique')]


# Insurances

class OeHealthInsurance(models.Model):
    _name = 'oeh.medical.insurance'
    _description = "Insurances"
    _inherits={
        'res.partner': 'partner_id',
    }

    STATE = [
        ('Draft','Draft'),
        ('Active','Active'),
        ('Expired','Expired'),
    ]

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade', help='Partner-related data of the insurance company')
    ins_no = fields.Char(string='Insurance #', size=64, required=True)
    patient = fields.Many2one('oeh.medical.patient', string='Patient', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    exp_date = fields.Date(string='Expiration date', required=True)
    ins_type = fields.Many2one('oeh.medical.insurance.type', string='Insurance Type', required=True)
    info = fields.Text(string='Extra Info')
    state = fields.Selection(STATE, string='State', readonly=True, copy=False, help="Status of insurance", default=lambda *a: 'Draft')

    _defaults={
            'is_insurance_company': True,
            'state':'Draft',
    }

    @api.model
    def create(self, vals):
        vals["is_insurance_company"] = True
        insurance = super(OeHealthInsurance, self).create(vals)
        return insurance

    @api.multi
    @api.depends('name', 'ins_no')
    def name_get(self):
        res = []
        for record in self:
            name = self.name
            if self.ins_no:
                name = "[" + self.ins_no + '] ' + name
            res += [(record.id, name)]
        return res

    @api.multi
    def make_active(self):
        self.write({'state': 'Active'})
        return True
