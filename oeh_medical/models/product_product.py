##############################################################################
#    Copyright (C) 2016 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

from odoo import api, fields, models, _


class oeHealthProduct(models.Model):
    _inherit = 'product.template'

    is_medicine = fields.Boolean(string='Medicine', help='Check if the product is a medicine')
    is_bed = fields.Boolean(string='Bed', help='Check if the product is a bed')
    is_vaccine = fields.Boolean(string='Vaccine', help='Check if the product is a vaccine')
    is_medical_supply = fields.Boolean(string='Medical Supply', help='Check if the product is a medical supply')
    is_insurance_plan = fields.Boolean(string='Insurance Plan', help='Check if the product is an insurance plan')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
