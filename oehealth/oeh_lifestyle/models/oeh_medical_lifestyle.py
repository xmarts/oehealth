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

# Recreational Drugs Management
class OeHealthRecreationalDrug(models.Model):
    _name = "oeh.medical.recreational.drugs"
    _description = "Recreational Drugs"

    TOXICITY = [
        ('None', 'None'),
        ('Low', 'Low'),
        ('High', 'High'),
        ('Extreme', 'Extreme'),
    ]

    ADDICTION_LEVEL = [
        ('None', 'None'),
        ('Low', 'Low'),
        ('High', 'High'),
        ('Extreme', 'Extreme'),
    ]

    LEGAL = [
        ('Legal', 'Legal'),
        ('Illegal', 'Illegal'),
    ]

    DRUG_CATEGORY = [
        ('Cannabinoids', 'Cannabinoids'),
        ('Depressants', 'Depressants'),
        ('Dissociative Anesthetics', 'Dissociative Anesthetics'),
        ('Hallucinogens', 'Hallucinogens'),
        ('Opioids', 'Opioids'),
        ('Stimulants', 'Stimulants'),
        ('Others', 'Others'),
    ]

    name = fields.Char(string='Drug Name', size=128, required=True)
    street_name = fields.Char(string='Street Names', size=256, help="Common name of the drug in street jargon")
    toxicity = fields.Selection(TOXICITY, string='Toxicity', required=True)
    addiction_level = fields.Selection(ADDICTION_LEVEL, string='Addiction Level', required=True)
    legal_status = fields.Selection(LEGAL, string='Legal Status', required=True)
    category = fields.Selection(DRUG_CATEGORY, 'Category', required=True)
    withdrawal_level = fields.Integer(string="Withdrawal Level", help="Presence and severity ofcharacteristic withdrawal symptoms.")
    reinforcement_level = fields.Integer(string="Reinforcement Level", help="A measure of the substance's ability to get users to take it again and again, and in preference to other substances.")
    tolerance_level = fields.Integer(string="Tolerance Level", help="How much of the substance is needed to satisfy increasing cravings for it, and the level of stable need that is eventually reached.")
    dependence_level = fields.Integer(string="Dependence", help="How difficult it is for the user to quit, the relapse rate, the percentage of people who eventually become dependent, the rating users give their own need for the substance and the degree to which the substance will be used in the face of evidence that it causes harm.")
    intoxication_level = fields.Integer(string="Intoxication", help="the level of intoxication is associated with addiction and increases the personal and social damage a substance may do.")
    route_oral = fields.Boolean(string='Oral')
    route_popping = fields.Boolean(string='Skin Popping', help="Subcutaneous or Intradermical administration")
    route_inhaling = fields.Boolean(string='Smoke / Inhale', help="Insufflation, exluding nasal")
    route_sniffing = fields.Boolean(string='Sniffing', help="Also called snorting - inhaling through the nares  ")
    route_injection = fields.Boolean(string='Injection', help="Injection - Intravenous, Intramuscular...")
    dea_schedule_i = fields.Boolean(string='DEA schedule I', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter")
    dea_schedule_ii = fields.Boolean(string='II', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter")
    dea_schedule_iii = fields.Boolean(string='III', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter")
    dea_schedule_iv = fields.Boolean(string='IV', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter")
    dea_schedule_v = fields.Boolean(string='V', help="Schedule I and II drugs have a high potential for abuse. They require greater storage security and have a quota on manufacturing, among other restrictions. Schedule I drugs are available for research only and have no approved medical use; Schedule II drugs are available only by prescription (unrefillable) and require a form for ordering. Schedule III and IV drugs are available by prescription, may have five refills in 6 months, and may be ordered orally. Some Schedule V drugs are available over the counter")
    info = fields.Text(string='Extra Info')

# Inheriting Patient module to add information to manage Patient's Lifestyles
class OeHealthPatient(models.Model):
    _inherit='oeh.medical.patient'

    SEXUAL_PREFERENCE = [
        ('Heterosexual', 'Heterosexual'),
        ('Homosexual', 'Homosexual'),
        ('Bisexual', 'Bisexual'),
        ('Transexual', 'Transexual'),
    ]

    SEXUAL_PRACTICES = [
        ('Safe / Protected sex', 'Safe / Protected sex'),
        ('Risky / Unprotected sex', 'Risky / Unprotected sex'),
    ]

    SEXUAL_PARTNERS = [
        ('Monogamous', 'Monogamous'),
        ('Polygamous', 'Polygamous'),
    ]

    ANTI_CONCEPTIVE = [
        ('None', 'None'),
        ('Pill / Minipill', 'Pill / Minipill'),
        ('Male Condom', 'Male Condom'),
        ('Vasectomy', 'Vasectomy'),
        ('Female Sterilisation', 'Female Sterilisation'),
        ('Intra-uterine Device', 'Intra-uterine Device'),
        ('Withdrawal Method', 'Withdrawal Method'),
        ('Fertility Cycle Awareness', 'Fertility Cycle Awareness'),
        ('Contraceptive Injection', 'Contraceptive Injection'),
        ('Skin Patch', 'Skin Patch'),
        ('Female Condom', 'Female Condom'),
    ]

    SEXUAL_ORAL = [
        ('None', 'None'),
        ('Active', 'Active'),
        ('Passive', 'Passive'),
        ('Both', 'Both'),
    ]

    SEXUAL_ANAL = [
        ('None', 'None'),
        ('Active', 'Active'),
        ('Passive', 'Passive'),
        ('Both', 'Both'),
    ]

    exercise = fields.Boolean(string='Exercise')
    exercise_minutes_day = fields.Integer(string='Minutes / day', help="How many minutes a day the patient exercises")
    sleep_hours = fields.Integer(string='Hours of Sleep', help="Average hours of sleep per day")
    sleep_during_daytime = fields.Boolean(string='Sleeps at Daytime', help="Check if the patient sleep hours are during daylight rather than at night")
    number_of_meals = fields.Integer('Meals / day')
    eats_alone = fields.Boolean(string='Eats alone', help="Check this box if the patient eats by him / herself.")
    salt = fields.Boolean(string='Salt', help="Check if patient consumes salt with the food")
    coffee = fields.Boolean(string='Coffee')
    coffee_cups = fields.Integer(string='Cups / day', help="Number of cup of coffee a day")
    soft_drinks = fields.Boolean(string='Soft Drinks (sugar)', help="Check if the patient consumes soft drinks with sugar")
    diet = fields.Boolean(string='Currently on a Diet', help="Check if the patient is currently on a diet")
    diet_info= fields.Char(string='Diet Info', size=256, help="Short description on the diet")
    smoking = fields.Boolean(string='Smokes')
    smoking_number = fields.Integer(string='Cigarretes a Day')
    ex_smoker = fields.Boolean(string='Ex-smoker')
    second_hand_smoker = fields.Boolean(string='Passive Smoker', help="Check it the patient is a passive / second-hand smoker")
    age_start_smoking = fields.Integer(string='Age Started to Smoke')
    age_quit_smoking = fields.Integer(string='Age of Quitting',help="Age of quitting smoking")
    alcohol = fields.Boolean(string='Drinks Alcohol')
    age_start_drinking = fields.Integer(string='Age Started to Drink ', help="Date to start drinking")
    age_quit_drinking = fields.Integer(string='Age Quit Drinking ', help="Date to stop drinking")
    ex_alcoholic = fields.Boolean(string='Ex Alcoholic')
    alcohol_beer_number = fields.Integer(string='Beer / day')
    alcohol_wine_number = fields.Integer(string='Wine / day')
    alcohol_liquor_number = fields.Integer(string='Liquor / day')
    drug_usage = fields.Boolean(string='Drug Habits')
    ex_drug_addict = fields.Boolean(string='Ex Drug Addict')
    drug_iv = fields.Boolean(string='IV Drug User', help="Check this option if the patient injects drugs")
    age_start_drugs = fields.Integer(string='Age Started Drugs ', help="Age of start drugs")
    age_quit_drugs = fields.Integer(string='Age Quit Drugs ', help="Date of quitting drugs")
    drugs = fields.Many2many('oeh.medical.recreational.drugs', 'oeh_medical_patient_recreational_drugs_rel', 'partner_id', 'oeh_drugs_recreational_id', string='Recreational Drugs', help="Name of drugs that the patient consumes")
    traffic_laws = fields.Boolean(string='Obeys Traffic Laws', help="Check if the patient is a safe driver")
    car_revision = fields.Boolean(string='Car Revision', help="Maintain the vehicle. Do periodical checks - tires, engine, breaks ...")
    car_seat_belt = fields.Boolean(string='Seat Belt', help="Safety measures when driving : safety belt")
    car_child_safety = fields.Boolean(string='Car Child Safety', help="Safety measures when driving : child seats, proper seat belting, not seating on the front seat, ....")
    home_safety = fields.Boolean(string='Home Safety', help="Keep safety measures for kids in the kitchen, correct storage of chemicals, ...")
    motorcycle_rider = fields.Boolean(string='Motorcycle Rider', help="The patient rides motorcycles")
    helmet = fields.Boolean(string='Uses Helmet', help="The patient uses the proper motorcycle helmet")
    lifestyle_info = fields.Text(string='Extra Information')
    sexual_preferences = fields.Selection(SEXUAL_PREFERENCE, string='Sexual Orientation')
    sexual_practices = fields.Selection(SEXUAL_PRACTICES, string='Sexual Practices')
    sexual_partners = fields.Selection(SEXUAL_PARTNERS, string='Sexual Partners')
    sexual_partners_number = fields.Integer(string='Number of Sexual Partners')
    first_sexual_encounter = fields.Integer(string='Age first Sexual Encounter')
    anticonceptive = fields.Selection(ANTI_CONCEPTIVE, string='Anticonceptive Method')
    sex_oral = fields.Selection(SEXUAL_PARTNERS, string='Oral Sex')
    sex_anal = fields.Selection(SEXUAL_PARTNERS, string='Anal Sex')
    prostitute = fields.Boolean(string='Prostitute', help="Check if the patient (he or she) is a prostitute")
    sex_with_prostitutes = fields.Boolean(string='Sex with Prostitutes', help="Check if the patient (he or she) has sex with prostitutes")
    sexuality_info = fields.Text(string='Extra Information')
