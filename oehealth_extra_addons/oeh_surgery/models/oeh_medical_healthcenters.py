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

# Operating Theaters (OT) Management
class OeHealthCentersOperatingRooms(models.Model):

    OT_STATES = [
        ('Free', 'Free'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
        ('Not Available', 'Not Available'),
    ]

    _name = 'oeh.medical.health.center.ot'
    _description = "Information about the health centers operating theaters"

    name = fields.Char(string='Operation Theater Name', size=32, required=True)
    building = fields.Many2one('oeh.medical.health.center.building', string='Building')
    info = fields.Text(string='Extra Info')
    state = fields.Selection(OT_STATES, string='Status', default=lambda *a: 'Free')

    _sql_constraints = [
            ('name_bed_uniq', 'unique (name)', 'The operation theater name is already occupied !')]


    # Preventing deletion of a operating theaters which is not in draft state
    @api.multi
    def unlink(self):
        for healthcenter in self.filtered(lambda healthcenter: healthcenter.state in ['Draft','Not Available']):
            raise UserError(_('You can not delete operating theaters(s) which is in "Reserved" or "Occupied" state !!'))
        return super(OeHealthCentersOperatingRooms, self).unlink()

    @api.multi
    def action_surgery_set_to_not_available(self):
        return self.write({'state': 'Not Available'})

    @api.multi
    def action_surgery_set_to_available(self):
        return self.write({'state': 'Free'})

class OeHealthCentersBuilding(models.Model):

    @api.multi
    def _ot_count(self):
        result = {}
        oe_ot = self.env['oeh.medical.health.center.ot']
        for building in self:
            domain = [('building', '=', building.id)]
            ot_ids = oe_ot.search(domain)
            ots = oe_ot.browse(ot_ids)
            ot_count = 0
            for ot in ots:
                ot_count+=1
            building.ot_count = ot_count
        return result

    _inherit = 'oeh.medical.health.center.building'
    ot_count = fields.Integer(compute=_ot_count, string="Operation Theaters")
