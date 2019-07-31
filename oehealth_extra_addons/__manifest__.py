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

{
    'name': 'oeHealth Extra Addons',
    'version': '1.0',
    'author': "Braincrew Apps",
    'category': 'Generic Modules/Medical',
    'summary': 'Pediatrics, Patient Call Logs, Medical History, Nursing, Surgical, Ophthalmology, Imaging, Neglected Tropical Diseases, Walkins, Medical Certificate and Procedure Coding System Management',
    'depends': ['oehealth','product'],
    'description': """

About oeHealth Extra Addons
----------------------------


1) Pediatrics Management:

- Newborn Baby & APGAR Management
- Pediatrics Symptom Checklist
- WHO Pediatrics Growth Chart

2) Surgical Management

- Manage complete details of the Surgery
- Revised Cardiac Risk Index
- Supplies related to the surgery
- Record details of Team Involved in the surgery

3) Ophthalmology Management

- Ophthalmology Visits
- Ophthalmology Findings

4) Nursing & Ambulatory Management

- Manage daily roundings and record details of patients during each rounding.
- Patient Ambulatory care management

5) Imaging Management

- Management of different imaging tests like X-Ray, Ultrasound, MRI, CT Scan and PET Scan
- Choose from existing test types or add custom one
- Print the report and generate invoice for the tests

6) Neglected Tropical Diseases Management

- Domiciliary Unit Management
- Chagas DU Entomological Survey Management
- Surveillance and management of Dengue fever

7) Record complete historical report based on Patient's Evaluation

8) Procedure Coding System for Medical : ICD-10-PCS

9) Patient Walkins Management

- Manage Physician Walkin schedules
- Register Daily patient walkins and view it by date
- Generate invoice for each walkin
- View related details like Evaluation, Vaccines, Prescriptions and Admissions for each walkins

10) Record and print patient medical certificate with leave dates and reason

""",
    "website": "http://oehealth.in",
    "data": [
        'sequence/oeh_sequence.xml',

        'oeh_pediatrics/views/res_partner_view.xml',
        'oeh_pediatrics/views/oeh_medical_pediatrics_newborn_view.xml',
        'oeh_pediatrics/views/oeh_medical_pediatrics_pcs_view.xml',
        'oeh_pediatrics/views/oeh_medical_pediatrics_growth_chart_view.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_boys_p.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_boys_z.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_girls_p.xml',
        'oeh_pediatrics/data/oeh_medical_wfa_girls_z.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_boys_p.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_boys_z.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_girls_p.xml',
        'oeh_pediatrics/data/oeh_medical_lhfa_girls_z.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_boys_p.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_boys_z.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_girls_p.xml',
        'oeh_pediatrics/data/oeh_medical_bmi_girls_z.xml',

        "oeh_icd10pcs/views/oeh_icd10pcs_view.xml",

        'oeh_surgery/views/oeh_medical_healthcenters_view.xml',
        'oeh_surgery/views/oeh_medical_surgery_view.xml',

        'oeh_ophthalmology/views/oeh_medical_ophthalmology_view.xml',
        'oeh_ophthalmology/views/oeh_medical_ophthalmology_report.xml',
        'oeh_ophthalmology/views/oeh_medical_report.xml',

        "oeh_nursing/views/oeh_medical_nursing_view.xml",
        "oeh_nursing/views/oeh_medical_rounding_report.xml",
        "oeh_nursing/views/oeh_medical_report.xml",

        "oeh_imaging/views/oeh_medical_imaging_view.xml",
        "oeh_imaging/views/report_patient_imaging.xml",
        "oeh_imaging/views/oeh_medical_imaging_report.xml",
        "oeh_imaging/data/oeh_imaging_test_types.xml",

        "oeh_ntd/views/oeh_medical_domiciliary_unit_view.xml",
        "oeh_ntd/views/oeh_medical_ntd_chagas_view.xml",
        "oeh_ntd/views/oeh_medical_ntd_dengue_view.xml",
        "oeh_ntd/data/oeh_lab_test_types.xml",

        "oeh_evaluation_history/views/oeh_medical_evaluation_report.xml",
        "oeh_evaluation_history/views/oeh_medical_report.xml",

        'oeh_medical_certificate/views/oeh_medical_certificate_view.xml',
        'oeh_medical_certificate/views/report_medical_certificate.xml',
        'oeh_medical_certificate/views/oeh_medical_report.xml',

        'oeh_walkins/views/oeh_medical_register_for_walkin_view.xml',

        'oeh_patient_call_log/views/oeh_medical_patient_call_log_view.xml',

        'oeh_patient_medical_history/views/oeh_medical_patient_view.xml',

        'security/oeh_security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',

    	'oeh_icd10pcs/data/oeh_icd_10_pcs_2009_part1.xml',
        'oeh_icd10pcs/data/oeh_icd_10_pcs_2009_part2.xml',
        'oeh_icd10pcs/data/oeh_icd_10_pcs_2009_part3.xml',
    ],
    "images": ['images/main_screenshot.png'],
    "demo": [

    ],
    'test':[
    ],
    'css': [

    ],
    'js': [

    ],
    'qweb': [

    ],
    "active": False
}