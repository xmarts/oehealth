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

# Domiciliary Unit Management

class OeHealthDomiciliaryUnit(models.Model):
    _name = 'oeh.medical.domiciliary.unit'
    _description = 'Domiciliary Unit Management'

    DWELLING = [
        ('Single / Detached House', 'Single / Detached House'),
        ('Apartment', 'Apartment'),
        ('Townhouse', 'Townhouse'),
        ('Factory', 'Factory'),
        ('Building', 'Building'),
        ('Mobile House', 'Mobile House'),
    ]

    MATERIAL = [
        ('Concrete', 'Concrete'),
        ('Adobe', 'Adobe'),
        ('Wood', 'Wood'),
        ('Mud / Straw', 'Mud / Straw'),
        ('Stone', 'Stone'),
    ]

    ROOF_TYPE = [
        ('Concrete', 'Concrete'),
        ('Adobe', 'Adobe'),
        ('Wood', 'Wood'),
        ('Thatched', 'Thatched'),
        ('Mud / Straw', 'Mud / Straw'),
        ('Stone', 'Stone'),
    ]

    HOUSING = [
        ('Shanty, deficient sanitary conditions', 'Shanty, deficient sanitary conditions'),
        ('Small, crowded but with good sanitary conditions', 'Small, crowded but with good sanitary conditions'),
        ('Comfortable and good sanitary conditions', 'Comfortable and good sanitary conditions'),
        ('Roomy and excellent sanitary conditions', 'Roomy and excellent sanitary conditions'),
        ('Luxury and excellent sanitary conditions', 'Luxury and excellent sanitary conditions'),
    ]

    name = fields.Char(string='Code', size=128, required=True)
    desc = fields.Char(string='Desc', size=25, required=True)
    address_street = fields.Char(string='Street', size=25)
    address_street_number = fields.Integer(string='Street #')
    address_street_bis = fields.Char(string='Apartment', size=25)
    address_district = fields.Char(string='District', size=25, help="Neighborhood, Village, Barrio....")
    address_municipality = fields.Char(string='Municipality', size=25, help="Municipality, Township, county ..")
    address_city = fields.Char(string='City', size=25)
    address_zip = fields.Char(string='Zip Code', size=25)
    address_country = fields.Many2one('res.country', string='Country', help='Country')
    address_state = fields.Many2one('res.country.state', string='State', help='State')
    institution = fields.Many2one('oeh.medical.health.center', string='Health Center')
    picture = fields.Binary(string="Picture", attachment=True)
    dwelling = fields.Selection(DWELLING, string='Type')
    materials = fields.Selection(MATERIAL, string='Material')
    roof_type = fields.Selection(ROOF_TYPE, string='Roof')
    total_surface = fields.Integer(string='Surface', help="Surface in sq. meters")
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    housing = fields.Selection(HOUSING, string='Conditions', help="Housing and sanitary living conditions")
    sewers = fields.Boolean(string='Sanitary Sewers')
    water = fields.Boolean(string='Running Water')
    trash = fields.Boolean(string='Trash recollection')
    electricity = fields.Boolean(string='Electrical supply')
    gas = fields.Boolean(string='Gas supply')
    telephone = fields.Boolean(string='Telephone')
    television = fields.Boolean(string='Television')
    internet = fields.Boolean(string='Internet')

    _sql_constraints = [('name_uniq', 'unique(name)', 'The Domiciliary Unit name must be unique')]

    @api.onchange('address_state')
    def onchange_state(self):
        if self.address_state:
            self.address_country = self.address_state.country_id.id