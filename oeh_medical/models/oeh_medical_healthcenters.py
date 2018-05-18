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

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

# Health Center Management

class OeHealthCenters(models.Model):
    _name = 'oeh.medical.health.center'
    _description = "Information about the health centers"
    _inherits={
        'res.partner': 'partner_id',
    }

    HEALTH_CENTERS = [
        ('Hospital', 'Hospital'),
        ('Nursing Home', 'Nursing Home'),
        ('Clinic', 'Clinic'),
        ('Community Health Center', 'Community Health Center'),
        ('Military Medical Facility', 'Military Medical Facility'),
        ('Other', 'Other'),
    ]

    @api.multi
    def _building_count(self):
        oe_buildings = self.env['oeh.medical.health.center.building']
        for hec in self:
            domain = [('institution', '=', hec.id)]
            buildings_ids = oe_buildings.search(domain)
            buildings = oe_buildings.browse(buildings_ids)
            bu_count = 0
            for bul in buildings:
                bu_count+=1
            hec.building_count = bu_count
        return True

    @api.multi
    def _pharmacy_count(self):
        oe_pharmacies = self.env['oeh.medical.health.center.pharmacy']
        for hec in self:
            domain = [('institution', '=', hec.id)]
            pharmacies_ids = oe_pharmacies.search(domain)
            pharmacies = oe_pharmacies.browse(pharmacies_ids)
            pha_count = 0
            for pha in pharmacies:
                pha_count+=1
            hec.building_count = pha_count
        return True


    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True,ondelete='cascade', help='Partner-related data of the hospitals')
    health_center_type = fields.Selection(HEALTH_CENTERS, string='Type', help="Health center type", index=True)
    info = fields.Text('Extra Information')
    building_count = fields.Integer(compute=_building_count, string="Buildings")
    pharmacy_count = fields.Integer(compute=_pharmacy_count, string="Pharmacies")

    @api.model
    def create(self, vals):
        vals["is_institution"] = True
        vals["is_company"] = True
        health_center = super(OeHealthCenters, self).create(vals)
        return health_center

    @api.onchange('state_id')
    def onchange_state(self):
        if self.state_id:
            self.country_id = self.state_id.country_id.id

# Health Center Building

class OeHealthCentersBuilding(models.Model):
    _name = 'oeh.medical.health.center.building'
    _description = "Health Centers buildings"

    @api.multi
    def _ward_count(self):
        oe_wards = self.env['oeh.medical.health.center.ward']
        for building in self:
            domain = [('building', '=', building.id)]
            wards_ids = oe_wards.search(domain)
            wards = oe_wards.browse(wards_ids)
            wa_count = 0
            for war in wards:
                wa_count+=1
            building.ward_count = wa_count
        return True

    @api.multi
    def _bed_count(self):
        oe_beds = self.env['oeh.medical.health.center.beds']
        for building in self:
            domain = [('building', '=', building.id)]
            beds_ids = oe_beds.search(domain)
            beds = oe_beds.browse(beds_ids)
            be_count = 0
            for bed in beds:
                be_count+=1
            building.bed_count = be_count
        return True

    name = fields.Char(string='Name', size=128, required=True, help="Name of the building within the institution")
    institution = fields.Many2one('oeh.medical.health.center', string='Health Center',required=True)
    code = fields.Char (string='Code', size=64)
    info = fields.Text (string='Extra Info')
    ward_count = fields.Integer(compute=_ward_count, string="Wards")
    bed_count = fields.Integer(compute=_bed_count, string="Beds")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The building name must be unique !')
    ]

# Health Center Wards Management

class OeHealthCentersWards(models.Model):
    _name = "oeh.medical.health.center.ward"

    GENDER = [
        ('Men Ward','Men Ward'),
        ('Women Ward','Women Ward'),
        ('Unisex','Unisex'),
    ]

    WARD_STATES = [
        ('Beds Available','Beds Available'),
        ('Full','Full'),
    ]

    @api.multi
    def _bed_count(self):
        oe_beds = self.env['oeh.medical.health.center.beds']
        for ward in self:
            domain = [('ward', '=', ward.id)]
            beds_ids = oe_beds.search(domain)
            beds = oe_beds.browse(beds_ids)
            be_count = 0
            for bed in beds:
                be_count+=1
            ward.bed_count = be_count
        return True

    name = fields.Char(string='Name', size=128, required=True, help="Ward / Room code")
    institution = fields.Many2one('oeh.medical.health.center',string='Health Center', required=True)
    building = fields.Many2one('oeh.medical.health.center.building',string='Building', required=True)
    floor = fields.Integer(string='Floor Number')
    private = fields.Boolean(string='Private Room',help="Check this option for private room")
    bio_hazard = fields.Boolean(string='Bio Hazard',help="Check this option if there is biological hazard")
    telephone = fields.Boolean(string='Telephone access')
    ac = fields.Boolean(string='Air Conditioning')
    private_bathroom = fields.Boolean(string='Private Bathroom')
    guest_sofa = fields.Boolean(string='Guest sofa-bed')
    tv = fields.Boolean(string='Television')
    internet = fields.Boolean(string='Internet Access')
    refrigerator = fields.Boolean(string='Refrigerator')
    microwave = fields.Boolean(string='Microwave')
    gender = fields.Selection(GENDER,string='Gender',default=lambda *a: 'Unisex')
    state = fields.Selection(WARD_STATES,string='Status',default='Beds Available')
    info = fields.Text('Extra Info')
    bed_count = fields.Integer(compute=_bed_count, string="Beds")

    _sql_constraints = [
        ('name_ward_uniq', 'unique (name,building)', 'The ward name is already configured in selected building !')
    ]

# Beds Management
class OeHealthCentersBeds(models.Model):

    BED_TYPES = [
        ('Gatch Bed','Gatch Bed'),
        ('Electric','Electric'),
        ('Stretcher','Stretcher'),
        ('Low Bed','Low Bed'),
        ('Low Air Loss','Low Air Loss'),
        ('Circo Electric','Circo Electric'),
        ('Clinitron','Clinitron'),
    ]

    BED_STATES = [
        ('Free', 'Free'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
        ('Not Available', 'Not Available'),
    ]

    CHANGE_BED_STATUS = [
        ('Mark as Available', 'Mark as Available'),
        ('Mark as Reserved', 'Mark as Reserved'),
        ('Mark as Not Available', 'Mark as Not Available'),
    ]
    _name = 'oeh.medical.health.center.beds'
    _description = "Information about the health centers beds"
    _inherits={
        'product.product': 'product_id',
    }

    product_id = fields.Many2one('product.product', string='Related Product', required=True, ondelete='cascade', help='Product-related data of the hospital beds')
    institution = fields.Many2one('oeh.medical.health.center',string='Health Center')
    building = fields.Many2one('oeh.medical.health.center.building', string='Building')
    ward = fields.Many2one('oeh.medical.health.center.ward','Ward', domain="[('building', '=', building)]", help="Ward or room", ondelete='cascade')
    bed_type = fields.Selection(BED_TYPES,string='Bed Type', required=True, default=lambda *a: 'Gatch Bed')
    telephone_number = fields.Char (string='Telephone Number', size=128, help="Telephone Number / Extension")
    info = fields.Text(string='Extra Info')
    state = fields.Selection(BED_STATES, string='Status', default='Free')
    change_bed_status = fields.Selection(CHANGE_BED_STATUS, string='Change Bed Status')

    @api.onchange('change_bed_status','state')
    def onchange_bed_status(self):
        res = {}
        if self.state and self.change_bed_status:
            if self.state=="Occupied":
                raise UserError(_('Bed status can not change if it already occupied!'))
            else:
                if self.change_bed_status== "Mark as Reserved":
                    self.state = "Reserved"
                elif self.change_bed_status== "Mark as Available":
                    self.state = "Free"
                else:
                    self.state = "Not Available"
        return res


    # Preventing deletion of a beds which is not in draft state
    @api.multi
    def unlink(self):
        for beds in self.filtered(lambda beds: beds.state not in ['Free','Not Available']):
            raise UserError(_('You can not delete bed(s) which is in "Reserved" or "Occupied" state !!'))
        return super(OeHealthCentersBeds, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name') and vals.get('ward'):
            query_bed = _("select count(*) from oeh_medical_health_center_beds oeb, product_product pr, product_template pt where pr.id=oeb.product_id and pr.product_tmpl_id=pt.id and pt.name='%s' and oeb.ward=%s")%(str(vals.get('name')), str(vals.get('ward')))
            self.env.cr.execute(query_bed)
            val = self.env.cr.fetchone()
            if val and int(val[0]) > 0:
               raise UserError(_('The bed name is already configured in selected ward !'))
        if vals.get('change_bed_status') and vals.get('state') and vals.get('state')=="Occupied":
            raise AccessError(_('Bed status can not change if it already occupied!'))
        vals["is_bed"] = True
        beds = super(OeHealthCentersBeds, self).create(vals)
        return beds

    @api.multi
    def write(self, vals):
        if 'change_bed_status' in vals:
            if vals.get('change_bed_status') in ('Mark as Reserved','Mark as Not Available'):
                for beds in self.filtered(lambda beds: beds.state in ['Occupied']):
                    raise AccessError(_('Bed status can not change if it already occupied!'))
        return super(OeHealthCentersBeds, self).write(vals)
