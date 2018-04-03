# -*- coding: utf-8 -*-
{
    'name': "Ramapo Project Jobs",

# This is how long the Summary can be before it gets cutoff in the Apps kanban view:
#    'summary': """
#      Short (1 phrase/line) summary of the module's pur
#        """,
#

    'summary': """
        Subscription -> Project -> Job -> Daily Reports
        """,


    'description': """
        This module supports the ordering, scheduling and recording of Jobs.
        Jobs are used to support field maintenance of Customer Assets under
        contract with Ramapo.

        * During Subscription creation, create a Project with a name matching the Subscription Reference (ie: SUB001)

        * Differentiate between standard Odoo Projects, Subscription Projects, Job Projects and Project Templates
          (via an invisible field project_type = False, subscription, job, templates)

        * Differentiate between standard Odoo Tasks, Job Project Management, Job Expenses and Job Labor Tasks
          (via an invisible field task_type)

        * Add a Jobs App to review Jobs (Job Projects)

        * Add a Tasks App to review Job Tasks (Job Project 'Project Managment' Tasks)



    """,

    'author': "VCloud9",

    'website': "https://www.vcloud9.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',

    'version': '1.5',

    'license': 'Other proprietary',

    # modules necessary for this one to work correctly
    'depends': [
                'base',

                # Jobs are authorized through PROJECTS - which are Odoo Subscriptions
                'sale_contract',

                # Jobs are one of four projec types: '' (default),'job','subscription','template'
                'project',

                # Jobs will be sold or ordered and are done at locations (Addresses on res.partner)
                #'sale',

                # Jobs will be Invoiced
                'account_accountant',

                # Jobs may have Issues
                #'project_issue',

                # Jobs have Crews and SubProjects
                'hr','hr_timesheet',

                # Vehicles are attached to Jobs
                'fleet',

                # Signatures are needed for Daily Reports
                'web_widget_digitized_signature',

                # Timesheet widget is needed
                'web_widget_timepicker',

    ],

    # csv and xml records loaded during install and update
    'data': [
        'security/ir.model.access.csv',
        'data/res.state.county.csv',
        'data/job.class.csv',
        'data/job.cost.code.csv',
        'data/job.structure.type.csv',
        'data/job.task.type.csv',
        'data/job.weather.type.csv',
        'data/sale_subscription.xml',
        'views/sale_subscription.xml',
        'views/res_partner.xml',
        'views/project_project.xml',
        'views/project_task.xml',
        'views/job_prevailing_wage.xml',
        'views/job_class.xml',
        'views/job_crew.xml',
        'views/job_cost_code.xml',
        'views/job_structure_type.xml',
        'views/job_task_type.xml',
        'views/job_weather_type.xml',
        'views/job_daily_report.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
