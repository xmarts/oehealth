##############################################################################
#    Copyright (C) 2017 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

{
    'name': 'oeHealth Personalizado',
    'version': '1.0',
    'author': "Braincrew Apps",
    'category': 'Generic Modules/Medical',
    'summary': 'Odoo 11 Hospital Management Solutions',
    'depends': ['base', 'sale', 'purchase', 'account', 'product','document','hr','web', 'account_invoicing'],
    'description': """

About oeHealth
---------------

oeHealth is a multi-user, highly scalable, centralized Electronic Medical Record (EMR) and Hospital Information System for Odoo.

Manage your patients with their important details including family info, prescriptions, appointments, diseases, insurances, lifestyle,mental & social status, lab test details, invoices and surgical histories.

Administer all your doctors with their complete details, weekly consultancy schedule, prescriptions, inpatient admissions and many more.

Allow your doctors and patients to login inside your oeHealth system to manage their appointments. oeHealth is tightly integrated with Odoo’s calendar control so you will be always updated for your upcoming schedules.
""",
    "website": "http://oehealth.in",
    "data": [

        'views/oehealth.xml',

        'sequence/oeh_sequence.xml',
        'oeh_navigation.xml',
        'oeh_medical/views/res_partner_view.xml',
        'oeh_medical/views/product_product_view.xml',
        'oeh_medical/views/oeh_medical_medicaments_view.xml',
        'oeh_medical/views/oeh_medical_pharmacy_view.xml',
        'oeh_medical/views/oeh_medical_healthcenters_view.xml',
        'oeh_medical/views/oeh_medical_pathology_view.xml',
        'oeh_medical/views/oeh_medical_inpatient_view.xml',
        'oeh_medical/views/oeh_medical_view.xml',
        'oeh_medical/views/account_invoice_view.xml',
        'oeh_medical/views/oeh_medical_insurance_view.xml',
        'oeh_medical/views/oeh_medical_ethnic_groups_view.xml',
        'oeh_medical/views/oeh_medical_genetics_view.xml',
        'oeh_medical/data/oeh_physician_specialities.xml',
        'oeh_medical/data/oeh_physician_degrees.xml',
        'oeh_medical/data/oeh_insurance_types.xml',
        'oeh_medical/data/oeh_ethnic_groups.xml',
        'oeh_medical/data/oeh_who_medicaments.xml',
        'oeh_medical/data/oeh_dose_units.xml',
        'oeh_medical/data/oeh_drug_administration_routes.xml',
        'oeh_medical/data/oeh_drug_form.xml',
        'oeh_medical/data/oeh_dose_frequencies.xml',
        'oeh_medical/data/oeh_genetic_risks.xml',
        'oeh_medical/data/oeh_report_paperformat.xml',
        'oeh_medical/reports/report_patient_label.xml',
        'oeh_medical/reports/report_patient_medicines.xml',
        'oeh_medical/reports/report_appointment_receipt.xml',
        'oeh_medical/reports/report_patient_prescriptions.xml',
        'oeh_medical/views/oeh_medical_report.xml',

        'oeh_evaluation/views/oeh_medical_evaluation_view.xml',
        'oeh_socioeconomics/views/oeh_medical_socioeconomics_view.xml',
        'oeh_socioeconomics/data/oeh_occupations.xml',
        'oeh_gyneco/views/oeh_medical_gyneco_view.xml',
        'oeh_lifestyle/views/oeh_medical_lifestyle_view.xml',
        'oeh_lifestyle/data/oeh_recreational_drugs.xml',
        'oeh_lab/data/oeh_lab_test_units.xml',
        'oeh_lab/data/oeh_lab_test_types.xml',
        'oeh_lab/views/report_patient_labtest.xml',
        'oeh_lab/views/oeh_medical_lab_report.xml',
        'oeh_lab/views/oeh_medical_lab_view.xml',

        'security/oeh_security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',

        'oeh_medical/data/oeh_disease_categories.xml',
        'oeh_medical/data/oeh_diseases.xml',

    ],
    "images": ['images/main_screenshot.png'],
    "demo": [

    ],
    'test':[
    ],
    'css': [],
    'js': [

    ],
    'qweb': [

    ],
    "active": False
}