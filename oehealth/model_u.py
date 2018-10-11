from odoo import api, fields, models, _


class AddFieldUsersOehealth(models.Model):
    _name='res.users'
    _inherit='res.users'
    hospital_employee=fields.Boolean(string="¿Trabaja en algun hospital?",default=False)
    hospital_usuario = fields.Many2one('oeh.medical.health.center', string='Hospital donde trabaja', help="Medical Center")

    @api.onchange('hospital_employee')
    def onchange_hospital_employee(self):
        if self.hospital_employee==False:
            self.hospital_usuario=''
