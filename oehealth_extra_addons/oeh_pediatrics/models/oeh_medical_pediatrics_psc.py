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

# Pediatrics Symptom Checklist Management

class OeHealthPediatricSymptomsChecklist(models.Model):
    _name = "oeh.medical.pediatrics.psc"
    _description = "Pediatrics Symptom Checklist"

    PSC_CONF = [
        ('0', 'Never'),
        ('1', 'Sometimes'),
        ('2', 'Often'),
    ]

    name = fields.Char(string='PSC #', size=64, readonly=True, required=True, default=lambda *a: '/')
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True)
    doctor = fields.Many2one('oeh.medical.physician', string='Physician', domain=[('is_pharmacist','=',False)], help="Current primary care / family doctor", required=True)
    evaluation_start = fields.Datetime(string='Date', required=True)
    notes = fields.Text('Notes')
    psc_aches_pains = fields.Selection(PSC_CONF, string='Complains of aches and pains')
    psc_less_interest_in_school = fields.Selection(PSC_CONF, string='Less interested in school')
    psc_spend_time_alone = fields.Selection(PSC_CONF, string='Spends more time alone')
    psc_tires_easily = fields.Selection(PSC_CONF, string='Tires easily, has little energy')
    psc_fidgety = fields.Selection(PSC_CONF, string='Fidgety, unable to sit still')
    psc_trouble_with_teacher = fields.Selection(PSC_CONF, string='Has trouble with teacher')
    psc_acts_as_driven_by_motor = fields.Selection(PSC_CONF, string='Acts as if driven by a motor')
    psc_daydreams_too_much = fields.Selection(PSC_CONF, string='Daydreams too much')
    psc_distracted_easily = fields.Selection(PSC_CONF, string='Distracted easily')
    psc_afraid_of_new_situations = fields.Selection(PSC_CONF, string='Is afraid of new situations')
    psc_sad_unhappy = fields.Selection(PSC_CONF, string='Feels sad, unhappy')
    psc_irritable_angry = fields.Selection(PSC_CONF, string='Is irritable, angry')
    psc_feels_hopeless = fields.Selection(PSC_CONF, string='Feels hopeless')
    psc_trouble_concentrating = fields.Selection(PSC_CONF, string='Has trouble concentrating')
    psc_less_interested_in_friends = fields.Selection(PSC_CONF, string='Less interested in friends')
    psc_fights_with_others = fields.Selection(PSC_CONF, string='Fights with other children')
    psc_absent_from_school = fields.Selection(PSC_CONF, string='Absent from school')
    psc_school_grades_dropping = fields.Selection(PSC_CONF, string='School grades dropping')
    psc_down_on_self = fields.Selection(PSC_CONF, string='Is down on him or herself')
    psc_visit_doctor_finds_ok = fields.Selection(PSC_CONF, string='Visits the doctor with doctor finding nothing wrong')
    psc_trouble_sleeping = fields.Selection(PSC_CONF, string='Has trouble sleeping')
    psc_worries_a_lot = fields.Selection(PSC_CONF, string='Worries a lot')
    psc_wants_to_be_with_parents = fields.Selection(PSC_CONF, string='Wants to be with you more than before')
    psc_feels_is_bad_child = fields.Selection(PSC_CONF, string='Feels he or she is bad')
    psc_takes_unnecesary_risks = fields.Selection(PSC_CONF, string='Takes unnecessary risks')
    psc_gets_hurt_often = fields.Selection(PSC_CONF, string='Gets hurt frequently')
    psc_having_less_fun = fields.Selection(PSC_CONF, string='Seems to be having less fun')
    psc_act_as_younger = fields.Selection(PSC_CONF, string='Acts younger than children his or her age')
    psc_does_not_listen_to_rules = fields.Selection(PSC_CONF, string='Does not listen to rules')
    psc_does_not_show_feelings = fields.Selection(PSC_CONF, string='Does not show feelings')
    psc_does_not_get_people_feelings = fields.Selection(PSC_CONF, string='Does not get people feelings')
    psc_teases_others = fields.Selection(PSC_CONF, string='Teases others')
    psc_blames_others = fields.Selection(PSC_CONF, string='Blames others for his or her troubles')
    psc_takes_things_from_others = fields.Selection(PSC_CONF, string='Takes things that do not belong to him or her')
    psc_refuses_to_share = fields.Selection(PSC_CONF, string='Refuses to share')
    psc_total = fields.Integer(string='PSC Total', required=True, default=lambda *a: 0)


    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('oeh.medical.pediatrics.psc')
        vals['name'] = sequence
        return super(OeHealthPediatricSymptomsChecklist, self).create(vals)

    @api.onchange('psc_aches_pains', 'psc_spend_time_alone',
                                 'psc_tires_easily', 'psc_fidgety', 'psc_trouble_with_teacher',
                                 'psc_less_interest_in_school', 'psc_acts_as_driven_by_motor',
                                 'psc_daydreams_too_much', 'psc_distracted_easily',
                                 'psc_afraid_of_new_situations', 'psc_sad_unhappy',
                                 'psc_irritable_angry', 'psc_feels_hopeless',
                                 'psc_trouble_concentrating', 'psc_less_interested_in_friends',
                                 'psc_fights_with_others', 'psc_absent_from_school',
                                 'psc_school_grades_dropping', 'psc_down_on_self',
                                 'psc_visit_doctor_finds_ok', 'psc_trouble_sleeping',
                                 'psc_worries_a_lot', 'psc_wants_to_be_with_parents',
                                 'psc_feels_is_bad_child', 'psc_takes_unnecesary_risks',
                                 'psc_gets_hurt_often', 'psc_having_less_fun',
                                 'psc_act_as_younger', 'psc_does_not_listen_to_rules',
                                 'psc_does_not_show_feelings',
                                 'psc_does_not_get_people_feelings',
                                 'psc_teases_others', 'psc_takes_things_from_others',
                                 'psc_refuses_to_share')
    def on_change_with_psc_total(self):
        psc_aches_pains = self.psc_aches_pains or '0'
        psc_spend_time_alone = self.psc_spend_time_alone or '0'
        psc_tires_easily = self.psc_tires_easily or '0'
        psc_fidgety = self.psc_fidgety or '0'
        psc_trouble_with_teacher = self.psc_trouble_with_teacher or '0'
        psc_less_interest_in_school = self.psc_less_interest_in_school or '0'
        psc_acts_as_driven_by_motor = self.psc_acts_as_driven_by_motor or '0'
        psc_daydreams_too_much = self.psc_daydreams_too_much or '0'
        psc_distracted_easily = self.psc_distracted_easily or '0'
        psc_afraid_of_new_situations = self.psc_afraid_of_new_situations or '0'
        psc_sad_unhappy = self.psc_sad_unhappy or '0'
        psc_irritable_angry = self.psc_irritable_angry or '0'
        psc_feels_hopeless = self.psc_feels_hopeless or '0'
        psc_trouble_concentrating = self.psc_trouble_concentrating or '0'
        psc_less_interested_in_friends = self.psc_less_interested_in_friends or '0'
        psc_fights_with_others = self.psc_fights_with_others or '0'
        psc_absent_from_school = self.psc_absent_from_school or '0'
        psc_school_grades_dropping = self.psc_school_grades_dropping or '0'
        psc_down_on_self = self.psc_down_on_self or '0'
        psc_visit_doctor_finds_ok = self.psc_visit_doctor_finds_ok or '0'
        psc_trouble_sleeping = self.psc_trouble_sleeping or '0'
        psc_worries_a_lot = self.psc_worries_a_lot or '0'
        psc_wants_to_be_with_parents = self.psc_wants_to_be_with_parents or '0'
        psc_feels_is_bad_child = self.psc_feels_is_bad_child or '0'
        psc_takes_unnecesary_risks = self.psc_takes_unnecesary_risks or '0'
        psc_gets_hurt_often = self.psc_gets_hurt_often or '0'
        psc_having_less_fun = self.psc_having_less_fun or '0'
        psc_act_as_younger = self.psc_act_as_younger or '0'
        psc_does_not_listen_to_rules = self.psc_does_not_listen_to_rules or '0'
        psc_does_not_show_feelings = self.psc_does_not_show_feelings or '0'
        psc_does_not_get_people_feelings = self.psc_does_not_get_people_feelings or '0'
        psc_teases_others = self.psc_teases_others or '0'
        psc_takes_things_from_others = self.psc_takes_things_from_others or '0'
        psc_refuses_to_share = self.psc_refuses_to_share or '0'

        self.psc_total = int(psc_aches_pains) + int(psc_spend_time_alone) + \
            int(psc_tires_easily) + int(psc_fidgety) + \
            int(psc_trouble_with_teacher) + \
            int(psc_less_interest_in_school) + \
            int(psc_acts_as_driven_by_motor) + \
            int(psc_daydreams_too_much) + int(psc_distracted_easily) + \
            int(psc_afraid_of_new_situations) + int(psc_sad_unhappy) + \
            int(psc_irritable_angry) + int(psc_feels_hopeless) + \
            int(psc_trouble_concentrating) + \
            int(psc_less_interested_in_friends) + \
            int(psc_fights_with_others) + int(psc_absent_from_school) + \
            int(psc_school_grades_dropping) + int(psc_down_on_self) + \
            int(psc_visit_doctor_finds_ok) + int(psc_trouble_sleeping) + \
            int(psc_worries_a_lot) + int(psc_wants_to_be_with_parents) + \
            int(psc_feels_is_bad_child) + int(psc_takes_unnecesary_risks) + \
            int(psc_gets_hurt_often) + int(psc_having_less_fun) + \
            int(psc_act_as_younger) + int(psc_does_not_listen_to_rules) + \
            int(psc_does_not_show_feelings) + \
            int(psc_does_not_get_people_feelings) + \
            int(psc_teases_others) + \
            int(psc_takes_things_from_others) + \
            int(psc_refuses_to_share)

# Inheriting Patient module to add "Pediatrics Symptom Checklist" screen reference
class OeHealthPatient(models.Model):
    _inherit='oeh.medical.patient'
    pediatrics_psc_ids = fields.One2many('oeh.medical.pediatrics.psc', 'patient', string='Pediatrics Symptom Checklist')
