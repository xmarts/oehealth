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
import time
import datetime
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools.translate import _


# Lab Units Management

class OeHealthLabTestUnits(models.Model):
    _name = 'oeh.medical.lab.units'
    _description = 'Lab Test Units'

    name = fields.Char(string='Unit Name', size=25, required=True)
    code = fields.Char(string='Code', size=25, required=True)

    _sql_constraints = [('name_uniq', 'unique(name)', 'The Lab unit name must be unique')]

# Lab Test Department
class OeHealthLabTestDepartment(models.Model):
    _name = 'oeh.medical.labtest.department'
    _description = 'Lab Test Departments'

    name = fields.Char(string='Name', size=128, required=True)
    hospital = fields.Many2one('oeh.medical.health.center', string='Hospital', help="Medical Center")
    suf_dep = fields.Char(string='Sufijo del Dep',size=2, help='Sufijo para identificar el departamento o tipo de estudio')
# Lab Test Types Management

class OeHealthLabTestCriteria(models.Model):
    _name = 'oeh.medical.labtest.criteria'
    _description = 'Lab Test Criteria'

    name = fields.Char(string='Tests', size=128, required=True)
    normal_range = fields.Text(string='Normal Range')
    units = fields.Many2one('oeh.medical.lab.units', string='Units')
    sequence = fields.Integer(string='Sequence')
    medical_type_id = fields.Many2one('oeh.medical.labtest.types', string='Lab Test Types')

    _order="sequence"


class OeHealthLabTestMaterial(models.Model):
    _name = 'oeh.medical.labtest.material'
    _description = 'Materiales para prueba de laboratorio'
    name = fields.Many2one('product.product',string='Producto')
    cantidad = fields.Integer(string="Cantidad")
    medical_type_id = fields.Many2one('oeh.medical.labtest.types', string='Lab Test Types')



class OeHealthLabTestTypes(models.Model):
    _name = 'oeh.medical.labtest.types'
    _description = 'Lab Test Types'

    name = fields.Char(string='Lab Test Name', size=128, required=True, help="Test type, eg X-Ray, Hemogram, Biopsy...")
    code = fields.Char(string='Code', size=128, help="Short code for the test")
    info = fields.Text(string='Description')
    test_charge = fields.Float(string='Test Charge', default=lambda *a: 0.0)
    lab_criteria = fields.One2many('oeh.medical.labtest.criteria', 'medical_type_id', string='Lab Test Cases')
    lab_material = fields.One2many('oeh.medical.labtest.material', 'medical_type_id', string='Materiales para prueba de laboratorio')
    lab_department = fields.Many2one('oeh.medical.labtest.department', string='Department')


class OeHealthLabTests(models.Model):
    _name = 'oeh.medical.lab.test'
    _description = 'Lab Tests'

    LABTEST_STATE = [
        ('Draft', 'Draft'),
        ('Test In Progress', 'Test In Progress'),
        ('Completed', 'Completed'),
        ('Invoiced', 'Invoiced'),
    ]
    LABTEST_INVOICE = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]

    name = fields.Char(string='Lab Test #', size=16, readonly=True, required=True, help="Lab result ID", default=lambda *a: '/')
    lab_department = fields.Many2one('oeh.medical.labtest.department', string='Department', readonly=True, states={'Draft': [('readonly', False)]})
    test_type = fields.Many2one('oeh.medical.labtest.types',string='Test Type', required=True, readonly=True, states={'Draft': [('readonly', False)]}, help="Lab test type")
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    pathologist = fields.Many2one('oeh.medical.physician', string='Pathologist', help="Pathologist", required=False, readonly=True, states={'Draft': [('readonly', False)]})
    requestor = fields.Char(string='Doctor who requested the test', help="Doctor who requested the test", readonly=True, states={'Draft': [('readonly', False)]})
    results = fields.Text(string='Results', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    diagnosis = fields.Text(string='Diagnosis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    lab_test_criteria = fields.One2many('oeh.medical.lab.resultcriteria', 'medical_lab_test_id', string='Lab Test Result', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    date_requested = fields.Datetime(string='Date requested', readonly=True, states={'Draft': [('readonly', False)]}, default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
    date_analysis = fields.Datetime(string='Date of the Analysis', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]}, required=True)
    state = fields.Selection(LABTEST_STATE, string='State', readonly=True, default=lambda *a: 'Draft')


    #First fields added
    duration = fields.Float(string='Duración (Horas:Minutos)', readonly=True, states={'Draft': [('readonly', False)]}, default='0.5', required=True)
    have_imss = fields.Boolean(string='¿Tiene Seguro?', readonly=True, states={'Draft': [('readonly', False)], 'Test In Progress': [('readonly', False)]})
    discount = fields.Integer(string='Porcentaje de Descuento', readonly=True, states={'Draft': [('readonly', False)]}, default="100")
    vale = fields.Char(string='N° de Vale', readonly=True, states={'Draft': [('readonly', False)]})
    hospital_estudio = fields.Many2one('oeh.medical.health.center', string='Hospital donde de hará el estudio', help="Medical Center", readonly=True, states={'Draft': [('readonly', False)]}, required=True)
    lab_test_indications = fields.One2many('oeh.medical.lab.indications.lines', 'medical_lab_test_id', string='Indicaciones', readonly=True, states={'Draft': [('readonly', False)]})
    code_cause = fields.Many2one('oeh.medical.lab.causes', string='Código Causa',readonly=True, states={'Draft': [('readonly', False)]})
    diagnostico = fields.Text(string='Diagnostico', readonly=True, states={'Completed': [('readonly', False)]})
    test_facturado = fields.Selection(LABTEST_INVOICE,string='¿Facturado?', readonly=True,default=lambda *a: 'No')
    
    #Second Fields added
    siconvenio = fields.Boolean(string='¿Cuentas con convenio?', help='Selecciona si cuentas con convenio')
    empresa = fields.Char(string='Empresa con Convenio', help='Empresa con la cual se tiene un Convenio')
    conv_porce = fields.Integer(string='Porcentaje de Descuento', help='Si cuenta con un convenio mostrara el porcentaje autorizado')
    pref_hosp = fields.Char(string='Prefijo del Hospital', help='Campo oculto que recupera el prefijo del hospital')
    pref_dep = fields.Char(string='Prefijo del Estudio', help='Campo oculto que recupera el prefijo cel Estudio ')
    pref_merge = fields.Char(string='Solicitud #', compute='merge_func', store=True)

    #Third fields added
    hospital_origen = fields.Many2one('oeh.medical.health.center', string='Hospital Origen', default=lambda self: self.env.user.hospital_usuario)

    @api.depends('pref_hosp','pref_dep','name')
    def merge_func(self):
        self.pref_merge = (self.pref_hosp or '')+''+(self.pref_dep or '')+''+(self.name or '')

    @api.model
    def lab_test_searchs(self):
        if(self.env.user.id==1):
            action = {
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form,calendar',
                'name': _('Rayos X'),
                'res_model': 'oeh.medical.lab.test',
            }
            return action
        else:
            cr = self.env.cr
            sql = "select id from oeh_medical_lab_test where hospital_origen='"+str(self.env.user.hospital_usuario.id)+"' or hospital_estudio='"+str(self.env.user.hospital_usuario.id)+"'"
            cr.execute(sql)
            tests = cr.fetchall()

            lista=[]
            for l in tests:
                lista.append(l[0])
            action = {
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form,calendar',
                'name': _('Rayos X'),
                'res_model': 'oeh.medical.lab.test',
                'domain': [('id', 'in', lista)],
                #'domain': ['&',('valid_purchase', '=', False),('id', 'in', lista)],
            }
            return action


    @api.onchange('siconvenio')
    def onchange_sico(self):    
        if self.siconvenio == True:
           self.have_imss == False

    @api.onchange('patient')
    def onchange_patient(self):
        self.siconvenio = self.patient.empresa.convenio
        self.empresa = self.patient.empresa.name
        self.conv_porce = self.patient.disc_porcent


    @api.onchange('hospital_estudio')
    def onechange_hospital_estudio(self):
        self.pref_hosp = self.hospital_estudio.suf_center

    @api.onchange('lab_department')
    def onchange_lab_department(self):
        self.pref_dep = self.lab_department.suf_dep 

    @api.onchange('hospital_estudio')
    def onchange_hosp(self):
        self.lab_department = None
        self.code_cause = None
        self.test_type = None

    @api.onchange('have_imss')
    def onchange_imss(self):
        self.lab_department = None
        self.code_cause = None
        self.test_type = None
        if self.have_imss == True:
           self.siconvenio = False

    @api.onchange('code_cause')
    def onchange_code(self):
        self.test_type = None
        lista = []
        res = {}
        if self.code_cause:
            for line in self.code_cause.estudios:
                if(line.name.lab_department == self.lab_department):
                    lista.append(line.name.id)
        res.update({
            'domain': {
                'test_type': [('id', 'in', list(set(lista)))],
            }
        })
        return res

    @api.onchange('lab_department')
    def onchange_dep(self):
        self.test_type = None
        lista = []
        res = {}
        if self.have_imss == True:
            if self.code_cause:
                for line in self.code_cause.estudios:
                    if(line.name.lab_department == self.lab_department):
                        lista.append(line.name.id)
            res.update({
                'domain': {
                    'test_type': [('id', 'in', list(set(lista)))],
                }
            })
        if self.have_imss == False:
            cr = self.env.cr
            self.code_cause = None
            if self.lab_department.id != False:
                sql = "select id from oeh_medical_labtest_types where lab_department='"+str(self.lab_department.id)+"';"
                cr.execute(str(sql))
                deps = cr.fetchall()
                if deps != None:
                    depts = []
                    for l in deps:
                        depts.append(l[0])
                    res.update({
                        'domain': {
                            'test_type': [('id', 'in', list(set(depts)))],
                        }
                    })
        return res


    @api.model
    def create(self, vals):
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        # get localized dates
        fc = vals.get('date_analysis')
        fechahora = datetime.datetime.strptime(fc, DATETIME_FORMAT)

        anho = str(fechahora.strftime('%Y'))
        mes = str(fechahora.strftime('%m'))
        dia = str(fechahora.strftime('%d'))
        hora = str(fechahora.strftime('%H'))
        minuto = str(fechahora.strftime('%M'))
        segundo = str(fechahora.strftime('%S'))
        fecha = anho+'-'+mes+'-'+dia
        if(vals.get('duration')==0):
            raise UserError(_("La duración no puede ser 0"))
        dur = vals.get('duration')
        currentHours = int(dur // 1)
        currentMinutes =int(round(dur % 1 * 60))
        if(currentHours <= 9):
            currentHours = "0" + str(currentHours)
        if(currentMinutes <= 9):
            currentMinutes = "0" + str(currentMinutes)

        hora1 = datetime.datetime(int(anho),int(mes),int(dia),int(hora),int(minuto),int(segundo))
        if((int(currentMinutes)+int(minuto))>=60):
            if(int(hora)+int(currentHours)+1 > 23):
                hora2 = datetime.datetime(int(anho),int(mes),int(dia),int(0),int((int(currentMinutes)+int(minuto))-60),int(segundo))
                dias = timedelta(days=1)
                hora2 = hora2 + dias
            else:
                hora2 = datetime.datetime(int(anho),int(mes),int(dia),int(int(hora)+int(currentHours)+1),int((int(currentMinutes)+int(minuto))-60),int(segundo))
        else:
            if(int(hora)+int(currentHours) > 23):
                hora2 = datetime.datetime(int(anho),int(mes),int(dia),int(0),int(int(currentMinutes)+int(minuto)),int(segundo))
                dias = timedelta(days=1)
                hora2 = hora2 + dias
            else:
                hora2 = datetime.datetime(int(anho),int(mes),int(dia),int(int(hora)+int(currentHours)),int(int(currentMinutes)+int(minuto)),int(segundo))
        #raise UserError(_(str(hora1)+"--"+str(hora2)))
        cr = self.env.cr
        sql = "select date_analysis,duration,lab_department from oeh_medical_lab_test WHERE date_analysis >= '"+str(fecha)+" 00:00:00' AND date_analysis <= '"+str(fecha)+" 23:59:59' AND hospital_estudio = '"+str(vals.get('hospital_estudio'))+"' AND lab_department = '"+str(vals.get('lab_department'))+"';"
        cr.execute(str(sql))
        citas = cr.fetchall()
        if(citas!=[]):
            for c in citas:
                fc1 = datetime.datetime.strptime(c[0], DATETIME_FORMAT)
                a1 = str(fc1.strftime('%Y'))
                m1 = str(fc1.strftime('%m'))
                d1 = str(fc1.strftime('%d'))
                h1 = str(fc1.strftime('%H'))
                mi1 = str(fc1.strftime('%M'))
                s1 = str(fc1.strftime('%S'))
                du1 = int(c[1])
                if du1 == 0:
                    du1 = 0.5
                currentHours2 = int(du1 // 1)
                currentMinutes2 =int(round(du1 % 1 * 60))
                if(currentHours2 <= 9):
                    currentHours2 = "0" + str(currentHours)
                if(currentMinutes2 <= 9):
                    currentMinutes2 = "0" + str(currentMinutes)
                if((int(currentMinutes2)+int(mi1))>=60):
                    if(int(h1)+int(currentHours2)+1 > 23):
                        horaf = datetime.datetime(int(a1),int(m1),int(d1),int(0),int((int(currentMinutes2)+int(mi1))-60),int(s1))
                        dias = timedelta(days=1)
                        horaf = horaf + dias
                    else:
                        horaf = datetime.datetime(int(a1),int(m1),int(d1),int(int(h1)+int(currentHours2)+1),int((int(currentMinutes2)+int(mi1))-60),int(s1))
                else:
                    if(int(h1)+int(currentHours2) > 23):
                        horaf = datetime.datetime(int(a1),int(m1),int(d1),int(0),int(int(currentMinutes2)+int(mi1)),int(s1))
                        dias = timedelta(days=1)
                        horaf = horaf + dias
                    else:
                        horaf = datetime.datetime(int(a1),int(m1),int(d1),int(int(h1)+int(currentHours2)),int(int(currentMinutes2)+int(mi1)),int(s1))
                horai = datetime.datetime(int(a1),int(m1),int(d1),int(h1),int(mi1),int(s1))
                if(horai == hora1):
                    raise UserError(_('Laboratorio ocupado en esta Fecha y Hora.'))
                if(hora1 > horai and  hora1 < horaf):
                    raise UserError(_('Laboratorio ocupado en esta Fecha y Hora.'))
                if(hora1 < horai and hora2 > horai and hora2 <= horaf):
                    raise UserError(_('Laboratorio ocupado en esta Fecha y Hora.'))
                if(hora1 < horai and hora2 > horaf):
                    raise UserError(_('Laboratorio ocupado en esta Fecha y Hora.'))

        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.lab.test')
        vals['name'] = sequence or '/'
        return super(OeHealthLabTests, self).create(vals)
 
 


    # Fetching lab test types
    @api.onchange('test_type')
    def onchange_test_type_id(self):
        values = self.onchange_test_type_id_values(self.test_type.id if self.test_type else False)
        return values


    @api.multi
    def onchange_test_type_id_values(self, test_type):
        criteria_obj = self.env['oeh.medical.labtest.criteria']
        labtest_ids =[]

        res = {}

         # if no test type present then nothing will process
        if (not test_type):
            return res

        #defaults
        res = {'value':{
                'lab_test_criteria':[],
            }
        }

        # Getting lab test lines values
        query = _("select name, sequence, normal_range, units from oeh_medical_labtest_criteria where medical_type_id=%s") % (str(test_type))
        self.env.cr.execute(query)
        vals = self.env.cr.fetchall()
        if vals:
            for va in vals:
                specs = {
                          'name': va[0],
                          'sequence': va[1],
                          'normal_range': va[2],
                          'units': va[3],
                        }
                labtest_ids += [specs]

        res['value'].update({
            'lab_test_criteria': labtest_ids,
        })
        return res


    # This function prints the lab test
    @api.multi
    def print_patient_labtest(self):
        return self.env.ref('oehealth.action_report_patient_labtest').report_action(self)

    @api.multi
    def set_to_test_inprogress(self):
        for l in self.test_type.lab_material:
            # Toma por defecto la ubicacion "Existencias" - (WH/Existencias)
            stockquant_id = self.env['stock.quant'].search([('location_id.id', '=', 15),('product_id', '=', l.name.id)], limit=1)
            stockquant_id.quantity = (stockquant_id.quantity)-(l.cantidad)
        return self.write({'state': 'Test In Progress', 'date_analysis': datetime.datetime.now()})

    @api.multi
    def set_to_test_complete(self):
        if(self.test_facturado=='Si'):
            return self.write({'state': 'Invoiced'})
        else:
            return self.write({'state': 'Completed'})

    @api.multi
    def _default_account(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        return journal.default_credit_account_id.id

    def action_lab_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        desc = 0
        #nvale = ''
        for lab in self:
            # Create Invoice
            if lab.patient:
                if self.siconvenio == True:
                    desc = self.conv_porce
                if self.have_imss == True:
                    desc = self.discount
                    #nvale = "\nNo. de Vale: " + self.vale
                curr_invoice = {
                    'partner_id': lab.patient.partner_id.id,
                    'account_id': lab.patient.partner_id.property_account_receivable_id.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice':datetime.datetime.now(),
                    'origin': "Lab Test# : " + lab.name,
                    'target': 'new',
                }

                inv_ids = invoice_obj.create(curr_invoice)
                inv_id = inv_ids.id

                if inv_ids:
                    prd_account_id = self._default_account()
                    if lab.test_type:

                        # Create Invoice line
                        curr_invoice_line = {
                            'name': "Charge for " + str(lab.test_type.name) + " laboratory test",
                            'price_unit': (lab.test_type.test_charge - ((lab.test_type.test_charge / 100) * desc)) or 0,
                            'quantity': 1.0,
                            'account_id': prd_account_id,
                            'invoice_id': inv_id,
                        }

                        inv_line_ids = invoice_line_obj.create(curr_invoice_line)
                self.write({'test_facturado': 'Si'})
                if(self.state=="Complete"):
                    self.write({'state': 'Invoiced'})

        return {
                'domain': "[('id','=', " + str(inv_id) + ")]",
                'name': 'Lab Test Invoice',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.invoice',
                'type': 'ir.actions.act_window'
        }



class OeHealthLabTestsIndications(models.Model):
    _name = 'oeh.medical.lab.indications'
    _description = 'Indicaciones para pruebas de laboratorio'
    name = fields.Char(string='Descripción', required=True)


class OeHealthLabTestsCauses(models.Model):
    _name = 'oeh.medical.lab.causes'
    _description = 'Códigos Causes'
    name = fields.Char(string='Código')
    familia = fields.Integer(string="Familia")
    definicion = fields.Char(string="Definición")
    description = fields.Char(string="Descripción")
    estudios = fields.One2many("oeh.medical.lab.causes.lines",'t_id',string="Estudios aplicables")

class OeHealthLabTestsCausesLines(models.Model):
    _name = 'oeh.medical.lab.causes.lines'
    _description = 'Códigos Causes Lines'
    name = fields.Many2one("oeh.medical.labtest.types",string="Estudios aplicables")
    t_id = fields.Many2one('oeh.medical.lab.causes', string="Cause ID", ondelete='cascade', index=True, copy=False,invisible=True)
    


class OeHealthLabTestsIndicationsLine(models.Model):
    _name = 'oeh.medical.lab.indications.lines'
    _description = 'Indicaciones'
    name = fields.Many2one("oeh.medical.lab.indications",string='Indicaciones', required=True)
    extra_info = fields.Char(string="Datos adicionales")
    medical_lab_test_id = fields.Many2one('oeh.medical.lab.test', string='Lab Tests')


class OeHealthLabTestsResultCriteria(models.Model):
    _name = 'oeh.medical.lab.resultcriteria'
    _description = 'Lab Test Result Criteria'

    name = fields.Char(string='Tests', size=128, required=True)
    result = fields.Text(string='Result')
    normal_range = fields.Text(string='Normal Range')
    units = fields.Many2one('oeh.medical.lab.units', string='Units')
    sequence = fields.Integer(string='Sequence')
    medical_lab_test_id = fields.Many2one('oeh.medical.lab.test', string='Lab Tests')

    _order="sequence"

# Inheriting Patient module to add "Lab" screen reference
class OeHealthPatient(models.Model):
    _inherit='oeh.medical.patient'
    
    @api.multi
    def _labtest_count(self):
        oe_labs = self.env['oeh.medical.lab.test']
        for ls in self:
            domain = [('patient', '=', ls.id)]
            lab_ids = oe_labs.search(domain)
            labs = oe_labs.browse(lab_ids)
            labs_count = 0
            for lab in labs:
                labs_count+=1
            ls.labs_count = labs_count
        return True

    lab_test_ids = fields.One2many('oeh.medical.lab.test', 'patient', string='Lab Tests')
    labs_count = fields.Integer(compute=_labtest_count, string="Lab Tests")

class OeHealthModCountry(models.Model):
    _inherit = 'res.partner'
    country_id = fields.Many2one('res.country', string="País", default=156)