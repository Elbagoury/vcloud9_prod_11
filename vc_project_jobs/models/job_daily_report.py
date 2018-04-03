# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class ReportEmployeeHours(models.Model):

    _name = 'report.employee.hours'
    _description = 'Employee Hours'

    # To link us back to the parent
    report_id = fields.Many2one(
        string = 'Daily Report',
        comodel_name = 'job.daily.report',
    )

    county_id = fields.Many2one(
        string = 'County',
        comodel_name = 'res.state.county',
        related = 'report_id.county_id',
    )

    # All lines on the report are in the same class, this is the filter
    type = fields.Selection([('employee', 'Employee'),
         ('prevailing', 'Prevailing'),
         ('standby', 'Standby'),
         ('rates', 'Rates'),
         ('all', 'All')],
         string = 'Type',
         required = True,
    )

    cost_code_id = fields.Many2one(
        string = 'Cost Code',
        comodel_name = 'job.cost.code',
    )

    is_first = fields.Boolean(
        default = False,
    )

    employee_id = fields.Many2one(
        string = 'Employee',
        required = True,
        comodel_name = 'hr.employee'
    )

    employee_standard_rate = fields.Float(
        string = 'Standard Rate',
        related = 'employee_id.timesheet_cost',
    )

    @api.multi
    @api.depends('employee_standard_rate')
    def _passenger_rate(rec):

        for record in rec:
            if record.employee_standard_rate > 0:
                record.employee_passenger_rate = record.employee_standard_rate / 2
        return rec

    employee_passenger_rate = fields.Float(
        string = 'Passenger Rate',
        compute = '_passenger_rate',
    )

    job_class_id = fields.Many2one(
        string = 'Class',
        comodel_name = 'job.class'
    )

    # the time at the shop before driving to the site are these two fields
    shop_time_start = fields.Float(
        string = 'Shop Start',
    )

    shop_time_start_str = fields.Char(
        string = 'Shop Start',
    )

    def _swizzle_time(rec,ttime):
        # Given a time from the Widget in the form "8:30 pm", return a float_time in the format "20.5"
        if len(ttime) == 0:
            return 0
        hour_part, min_part = ttime.split(":")
        am_pm = min_part[-2:]
        min_part = float(min_part[:-2]) * 1/60
        if am_pm == 'am' or int(hour_part) == 12:
            float_time = int(hour_part) + min_part
        else:
            float_time = int(hour_part) + 12 + min_part
        #raise ValidationError(hour_part + "*-*" + str(min_part) + "*-*" + am_pm + "*-*" + str(float_time))
        return float_time

    @api.onchange('shop_time_start_str')
    def _onchange_shop_time_start_str(self):
        for rec in self:
            rec.shop_time_start = rec._swizzle_time(rec.shop_time_start_str)
            # check if the shop start and shop end are compatible
            if rec.shop_time_start > 0 and rec.shop_time_end > 0:
                rec.total_regular_hours_before = rec.shop_time_end - rec.shop_time_start

    shop_time_end = fields.Float(
        string = 'Shop End',
    )

    shop_time_end_str = fields.Char(
        string = 'Shop End',
    )

    @api.onchange('shop_time_end_str')
    def _onchange_shop_time_end_str(self):
        for rec in self:
            rec.shop_time_end = rec._swizzle_time(rec.shop_time_end_str)
            # check if the shop start and shop end are compatible
            if rec.shop_time_start > 0 and rec.shop_time_end > 0:
                rec.total_regular_hours_before = rec.shop_time_end - rec.shop_time_start

    driver_time_start = fields.Float(
        string = 'Driver Out',
    )

    driver_time_start_str = fields.Char(
        string = 'Driver Out',
    )

    @api.onchange('driver_time_start_str')
    def _onchange_driver_time_start_str(self):
        for rec in self:
            rec.driver_time_start = rec._swizzle_time(rec.driver_time_start_str)
            if rec.driver_time_start == 0.00:
                rec.total_drive_hours_before = 0
                if rec.driver_time_arrive > 0:
                    rec.total_passenger_hours = rec.driver_time_arrive - rec.shop_time_end
            if rec.driver_time_arrive > 0 and rec.driver_time_start > 0:
                rec.total_drive_hours_before = rec.driver_time_arrive - rec.driver_time_start

    driver_time_arrive = fields.Float(
        string = 'On Site',
    )

    driver_time_arrive_str = fields.Char(
        string = 'On Site',
    )

    @api.onchange('driver_time_arrive_str')
    def _onchange_driver_time_arrive_str(self):
        for rec in self:
            rec.driver_time_arrive = rec._swizzle_time(rec.driver_time_arrive_str)
            if rec.driver_time_start == 0.00:
                rec.total_drive_hours_before = 0
                rec.total_passenger_hours_before = rec.driver_time_arrive - rec.shop_time_end
            else:
                rec.total_drive_hours_before = rec.driver_time_arrive - rec.driver_time_start


    lunch = fields.Selection(
        string = 'Lunch',
        selection = [
         ('0', 'None'),
         ('30', '30 mins'),
         ('60', '60 mins'),
        ],
        default = '0',

    )

    time_depart = fields.Float(
        string = 'Off Site',
    )

    time_depart_str = fields.Char(
        string = 'Off Site',
    )

    @api.onchange('time_depart_str')
    def _onchange_time_depart_str(self):
        for rec in self:
            rec.time_depart = rec._swizzle_time(rec.time_depart_str)
            if rec.time_depart > 0 and rec.driver_time_arrive > 0:
                rec.total_regular_hours_during = rec.time_depart - rec.driver_time_arrive

    driver_time_depart = fields.Float(
        string = 'Driver Out',
    )

    driver_time_depart_str = fields.Char(
        string = 'Driver Out',
    )

    @api.onchange('driver_time_depart_str')
    def _onchange_driver_time_depart_str(self):
        for rec in self:
            rec.driver_time_depart = rec._swizzle_time(rec.driver_time_depart_str)
            if rec.driver_time_depart == 0.0:
                rec.total_drive_hours_after = 0
                rec.regular_hours_after = rec.driver_time_arrive - rec.driver_time_depart
            if rec.driver_time_depart > 0 and rec.driver_time_end > 0:
                rec.total_drive_hours_after = rec.driver_time_end - rec.driver_time_depart

    driver_time_end = fields.Float(
        string = 'At Shop',
    )

    driver_time_end_str = fields.Char(
        string = 'At Shop',
    )

    @api.onchange('driver_time_end_str')
    def _onchange_driver_time_end_str(self):
        for rec in self:
            rec.driver_time_end = rec._swizzle_time()

    @api.onchange('driver_time_end_str')
    def _onchange_driver_time_end_str(self):
        for rec in self:
            rec.driver_time_end = rec._swizzle_time(rec.driver_time_end_str)
            if rec.driver_time_depart == 0:
                rec.total_passenger_hours_after = rec.driver_time_end - rec.time_depart
            else:
                rec.total_drive_hours_after = rec.driver_time_end - rec.driver_time_depart


    total_regular_hours_before = fields.Float(
    )

    total_regular_hours_during = fields.Float(
    )

    @api.multi
    @api.depends('lunch','total_regular_hours_before','total_regular_hours_during')
    def _regular_hours(rec):

        for record in rec:
        # Work out what the lunch deduction is
            if int(record.lunch) == 0:
                lunch_deduction = 0
            elif int(record.lunch) == 30:
                lunch_deduction = 0.5
            else:
                lunch_deduction = 1
            record.total_regular_hours = record.total_regular_hours_before + \
                                         record.total_regular_hours_during - \
                                         lunch_deduction
        return rec

    total_regular_hours = fields.Float(
        string = 'Regular',
        compute = '_regular_hours',
    )

    total_passenger_hours_before = fields.Float(
    )

    total_passenger_hours_after = fields.Float(
    )

    @api.multi
    @api.depends('total_passenger_hours_before','total_passenger_hours_after')
    def _passenger_hours(rec):
        for record in rec:
            record.total_passenger_hours = record.total_passenger_hours_before + \
                                         record.total_passenger_hours_after
        return rec

    total_passenger_hours = fields.Float(
        string = 'Passenger',
        compute = '_passenger_hours',
    )

    total_drive_hours_before = fields.Float(
    )

    total_drive_hours_after = fields.Float(
    )

    @api.multi
    @api.depends('total_drive_hours_before','total_drive_hours_after')
    def _drive_hours(rec):
        for record in rec:
            record.total_drive_hours = record.total_drive_hours_before + \
                                         record.total_drive_hours_after
        return rec


    total_drive_hours = fields.Float(
        string = 'Driving',
        compute = '_drive_hours',
    )

    total_pw_hours = fields.Float(
        string = 'PW',
    )

    total_standby_hours = fields.Float(
        string = 'Standby',
    )

    total_hours = fields.Float(
        string = 'Total',
    )

    per_diem = fields.Float(
        string = 'Per Diem',
    )

    timesheet_cost = fields.Float(
        string = 'Rate',
        related = 'employee_standard_rate',
    )

    @api.multi
    @api.depends('timesheet_cost')
    def _passenger_cost(rec):
        for record in rec:
            record.passenger_cost = record.employee_standard_rate / 2
        return rec

    passenger_cost = fields.Float(
        string = 'Rate',
        compute = '_passenger_cost',
    )

    drive_cost = fields.Float(
        string = 'Rate',
        related = 'employee_standard_rate',
    )

    pw_cost = fields.Float(
        string = 'Rate',
    )

    standby_cost = fields.Float(
        string = 'Rate',
    )

    @api.multi
    @api.depends('total_regular_hours')
    def _regular_pay(rec):
        for record in rec:
            record.regular_pay = record.total_regular_hours  * record.timesheet_cost
            record.regular_pay_str = str(record.total_regular_hours) + " h x $" +str(record.timesheet_cost) + " = $" + str(record.regular_pay)
        return rec

    regular_pay = fields.Float(
        compute = '_regular_pay',
    )

    regular_pay_str = fields.Char(
        string = "Regular",
        compute = '_regular_pay'
    )

    @api.multi
    @api.depends('total_passenger_hours')
    def _passenger_pay(rec):
        for record in rec:
            record.passenger_pay = record.passenger_cost * record.total_passenger_hours
            record.passenger_pay_str = str(record.total_passenger_hours) + " h x $" + str(record.passenger_cost) + " = $" + str(record.passenger_pay)
        return rec

    passenger_pay = fields.Float(
        compute = '_passenger_pay'
    )

    passenger_pay_str = fields.Char(
        string = 'Passenger',
        compute = '_passenger_pay'
    )

    @api.multi
    @api.depends('total_drive_hours')
    def _drive_pay(rec):
        for record in rec:
            record.drive_pay = record.drive_cost * record.total_drive_hours
            record.drive_pay_str = str(record.total_drive_hours) + " h x $" + str(record.drive_cost) + " = $" + str(record.drive_pay)
        return rec

    drive_pay = fields.Float(
        compute = '_drive_pay'
    )

    drive_pay_str = fields.Char(
        string = 'Driving',
        compute = '_drive_pay'
    )


    @api.multi
    @api.depends('total_pw_hours')
    def _pw_pay(rec):
        for record in rec:
            record.pw_pay = record.pw_cost * record.total_pw_hours
            record.pw_pay_str = str(record.total_pw_hours) + " h x $" + str(record.pw_cost) + " = $" + str(record.pw_pay)
        return rec

    pw_pay = fields.Float(
        compute = '_pw_pay'
    )

    pw_pay_str = fields.Char(
        string = 'PW',
        compute = '_pw_pay'
    )


    @api.multi
    @api.depends('total_standby_hours')
    def _standby_pay(rec):
        for record in rec:
            record.standby_pay = record.standby_cost * record.total_standby_hours
            record.standby_pay_str = str(record.total_standby_hours) + " h x $" + str(record.standby_cost) + " = $" + str(record.standby_pay)
        return rec

    standby_pay = fields.Float(
        compute = '_standby_pay'
    )

    standby_pay_str = fields.Char(
        string = 'Standby',
        compute = '_standby_pay'
    )

    @api.multi
    @api.depends('total_regular_hours','total_passenger_hours','total_drive_hours','total_pw_hours','total_standby_hours')
    def _total_pay(rec):
        for record in rec:
            record.total_pay = record.regular_pay + record.passenger_pay + record.drive_pay + record.pw_pay + record.standby_pay
            record.total_pay_str = "= $" + str(record.total_pay)
        return rec

    total_pay = fields.Float(
        compute = '_total_pay'
    )

    total_pay_str = fields.Char(
        string = 'Grand Total',
        compute = '_total_pay'
    )


    approved = fields.Boolean(
        string = 'Approved',
    )

    standby_reason = fields.Char(
        string = 'Reason',
    )







class JobDailyReport(models.Model):

    _name = 'job.daily.report'
    _inherit = ['mail.thread',]
    _description = 'Job Daily Reports'

    state = fields.Selection(
        string = 'State',
        selection = [
         ('draft', 'Draft'),
         ('submitted', 'Submitted'),
         ('reviewed', 'Reviewed'),
         ('approved', 'Approved'),
         ('paid', 'Paid'),
         ('cancelled', 'Cancelled'),
        ],
        required = True,
        default = 'draft',
    )

    @api.multi
    def action_submit(self):
        self.write({'state': 'submitted'})

    @api.multi
    def action_review(self):
        self.write({'state': 'reviewed'})

    @api.multi
    def action_approve(self):
        self.write({'state': 'approved'})

    @api.multi
    def action_pay(self):
        self.write({'state': 'paid'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})


    name = fields.Char(
        string = 'Name',
        required = True,
    )

    date = fields.Date(
        string = 'Name',
        required = True,
    )

    project_id = fields.Many2one(
        string = 'Job Project',
        comodel_name = 'project.project',
        required = True,
        domain = "[('project_type','=','subscription')]"
    )

    customer_id = fields.Many2one(
        string = 'Customer',
        comodel_name = 'res.partner',
        related = 'project_id.partner_id',
    )

    job_id = fields.Many2one(
        comodel_name = 'project.project',
        string = 'Job',
        required = True,
        domain = "[('project_type','=','job'),('partner_id','=',customer_id)]"
    )


    site_id = fields.Many2one(
        string = 'Site',
        comodel_name = 'res.partner',
        related = 'job_id.site_id',
    )

    site_reference = fields.Char(
        string = 'Site Reference',
        related = 'site_id.ref',
    )

    crew_id = fields.Many2one(
        comodel_name = 'job.crew',
        string = 'Job Crew',
    )

    crew_employees = fields.Many2many(
        comodel_name = 'hr.employee',
        string = 'Crew Members',
        related = 'crew_id.employee_ids',
    )

    crew_readonly = fields.Boolean(
        default = False
    )

    # Automatically add Employees
    @api.onchange('crew_employees')
    def crew_employees_change(self):

        employee_hours = []
        prevailing_hours = []
        standby_hours = []
        all_hours = []
        rates = []

        is_first = True
        for employee in self.crew_employees:
            employee_hours.append([0,0,
                {'type': 'employee',
                 'job_class_id': 1,
                 'cost_code_id': 1,
                 'is_first': is_first,
                 'employee_id': employee.id,}])
            prevailing_hours.append([0,0,
                {'type': 'prevailing',
                 'job_class_id': 1,
                 'cost_code_id': 1,
                 'is_first': is_first,
                 'employee_id': employee.id,}])
            standby_hours.append([0,0,
                {'type': 'standby',
                 'job_class_id': 1,
                 'cost_code_id': 1,
                 'is_first': is_first,
                 'employee_id': employee.id,}])
            all_hours.append([0,0,
                {'type': 'all',
                 'job_class_id': 1,
                 'cost_code_id': 1,
                 'is_first': is_first,
                 'employee_id': employee.id,}])
            rates.append([0,0,
                {'type': 'rates',
                 'job_class_id': 1,
                 'cost_code_id': 1,
                 'is_first': is_first,
                 'employee_id': employee.id,}])
            if is_first == True:
                is_first = False


        return {'value': {'employee_hours': employee_hours, 'prevailing_hours': prevailing_hours, 
                          'standby_hours': standby_hours, 'all_hours': all_hours, 'rates': rates,}}

    county_id = fields.Many2one(
        string = 'County',
        comodel_name = 'res.state.county',
        related = 'site_id.county_id',
    )

    weather_id = fields.Many2many(
        string = 'Weather',
        comodel_name = 'job.weather.type',
        required = False,
    )

    structure_type_id = fields.Many2one(
        string = 'Structure Type',
        comodel_name = 'job.structure.type',
        required = True,
    )

    hotel_name = fields.Many2one(
        string = 'Hotel Name',
        comodel_name = 'res.partner',
        related = "job_id.hotel_name",
    )

    project_manager_id = fields.Many2one(
        string = 'Project Manager',
        comodel_name = 'res.users',
        related = 'job_id.user_id',
    )

    foreman_id = fields.Many2one(
        string = 'Foreman',
        comodel_name = 'hr.employee',
        related = "job_id.foreman_id",
    )

    vehicle_ids = fields.Many2many(
        string = 'Vehicles',
        comodel_name = 'fleet.vehicle',
        relation = 'job_daily_report_fleet_vehicle_rel',
        column1 = 'job_daily_report_id',
        column2 = 'fleet_vehicle_id',
    )

    task_type_ids = fields.Many2many(
        string = 'Items/Tasks Completed',
        comodel_name = 'job.task.type',
        relation = 'job_daily_report_task_type_rel',
        column1 = 'job_daily_report_id',
        column2 = 'task_type_id',
    )

    notes = fields.Text(
        name = 'Notes',
    )

    foreman_signature = fields.Binary(
        string='Approved By',
    )

    foreman_signature_date = fields.Date(
        string='Date',
    )

    project_manager_signature = fields.Binary(
        string='Approved By',
    )

    project_manager_signature_date = fields.Date(
        string='Date',
    )


    employee_hours = fields.One2many(
        string = 'Employee Hours',
        comodel_name = 'report.employee.hours',
        inverse_name = 'report_id',
        domain = [('type','=','employee')]
    )

    # Automatically add Employees
    @api.onchange('employee_hours')
    def employee_hours_change(self):

        all_hours = []
        rates = []

        for rec in self.employee_hours:
            all_hours.append([0,0,
                {'type': 'all',
                 'job_class_id': rec.job_class_id,
                 'cost_code_id': rec.cost_code_id,
                 'lunch': rec.lunch,
                 'total_regular_hours_before': rec.total_regular_hours_before,
                 'total_regular_hours_during': rec.total_regular_hours_during,
                 'total_passenger_hours_before': rec.total_passenger_hours_before,
                 'total_passenger_hours_after': rec.total_passenger_hours_after,
                 'total_drive_hours_before': rec.total_drive_hours_before,
                 'total_drive_hours_after': rec.total_drive_hours_after,
                 'employee_id': rec.employee_id,}])
            rates.append([0,0,
                {'type': 'rates',
                 'job_class_id': rec.job_class_id,
                 'cost_code_id': rec.cost_code_id,
                 'lunch': rec.lunch,
                 'total_regular_hours_before': rec.total_regular_hours_before,
                 'total_regular_hours_during': rec.total_regular_hours_during,
                 'total_passenger_hours_before': rec.total_passenger_hours_before,
                 'total_passenger_hours_after': rec.total_passenger_hours_after,
                 'total_drive_hours_before': rec.total_drive_hours_before,
                 'total_drive_hours_after': rec.total_drive_hours_after,
                 'employee_standard_rate': rec.employee_standard_rate,
                 'employee_id': rec.employee_id,}])

        return {'value': {'all_hours': all_hours,'rates': rates}}

    prevailing_hours = fields.One2many(
        string = 'Prevailing Hours',
        comodel_name = 'report.employee.hours',
        inverse_name = 'report_id',
        domain = [('type','=','prevailing')]
    )

    standby_hours = fields.One2many(
        string = 'Standby Hours',
        comodel_name = 'report.employee.hours',
        inverse_name = 'report_id',
        domain = [('type','=','standby')]
    )

    all_hours = fields.One2many(
        string = 'Prevailing Hours',
        comodel_name = 'report.employee.hours',
        inverse_name = 'report_id',
       domain = [('type','=','all')]
    )

    rates = fields.One2many(
        string = 'Rates',
        comodel_name = 'report.employee.hours',
        inverse_name = 'report_id',
        domain = [('type','=','rates')]
    )


    _sql_constraints = [
        ('name_date_uniq', 'unique (date,name)', 'This Report is already in the system for the date entered!  Please check the Date and Name and try again.')
    ]

    @api.multi
    def action_view_projects(self):
        return {
                "type": "ir.actions.act_window",
                "res_model": "project.project",
                "res_id": self.project_id.id,
                "domain": [["id", "=", self.project_id.id]],
                "views": [[self.env.ref('project.edit_project').id, "form"]],
                "name": "Projects",
        }
