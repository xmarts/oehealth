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

# Patient Call Logs Management

class OeHealthPatientCallLog(models.Model):
    _name = 'oeh.medical.patient.call.log'
    _description = 'Patient Call Logs Management'

    CALL_TYPE = [
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Other', 'Other'),
    ]

    name = fields.Char(string='Call Log #', size=64, readonly=True, default=lambda *a: '/')
    call_type = fields.Selection(CALL_TYPE, string="Call Type", required=True)
    log_date = fields.Datetime('Date/Time of contact', required=True, default=lambda *a: datetime.datetime.now())
    person_in_charge = fields.Many2one('res.users', string='Person In Charge', required=True, default=lambda self: self.env.uid)
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True)
    call_log = fields.Text(string='Call Log', required=True)

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.patient.call.log')
        vals['name'] = sequence
        return super(OeHealthPatientCallLog, self).create(vals)

    @api.multi
    def write(self, vals):
        for clog in self:
            if clog.person_in_charge.id != self.env.uid:
                raise UserError(_('Only the person in charge is allowed to update the details'))
        return super(OeHealthPatientCallLog, self).write(vals)

    # Inheriting Patient module to add "Call Logs" screen reference
class OeHealthPatient(models.Model):
    _inherit='oeh.medical.patient'
    call_log_ids = fields.One2many('oeh.medical.patient.call.log', 'patient', string='Call Logs')
