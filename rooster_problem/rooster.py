'''

==========================================================================
Inputs :

Number of days in a month = n
Minimum number of employee required each day = x
Number of holidays in a month = h

==========================================================================
Output :

Number of required employee = P
                            = (days_in_a_month * daily_employee_requierd) / (days_in_a_month - holidays_in_a_month)
Rooster for the month :
-------------------------------------------------------------------------------------------------------------------
| p1  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p2  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p3  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p4  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p5  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p6  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p7  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p8  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p9  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| p0  |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
-------------------------------------------------------------------------------------------------------------------

'''
from math import ceil

from day import Day
from employee import Employee
from itertools import cycle

days_in_a_month = 31
daily_employee_required = 7
holidays_in_a_month = 8


class Rooster:
    days = []

    def __init__(self, days_in_a_month, daily_employee_required, holidays_in_a_month):
        self.days_in_a_month = days_in_a_month
        self.daily_employee_required = daily_employee_required
        self.holidays_in_a_month = holidays_in_a_month
        self.total_employee_required = ceil((self.days_in_a_month * self.daily_employee_required) / \
                                            (self.days_in_a_month - self.holidays_in_a_month))
        self.rooster = [Day(day + 1) for day in range(self.days_in_a_month)]
        self.consecutive_work_days = 5
        self.week_holidays = 2
        self.employees = self.create_employees(self.total_employee_required)

    def compute(self):
        work_days_template = [1, 1, 1, 1, 1, 0, 0]
        self.employee_pool = []
        for employee in self.employees:
            day_counter = 0
            holiday_counter = 0
            for day in self.rooster:
                week_day = day_counter % len(work_days_template)
                if work_days_template[week_day] == 1:
                    day.add_employee_to_working_list(employee)
                    employee.working_days.append(day)
                elif work_days_template[week_day] == 0 and holiday_counter + 1 <= self.holidays_in_a_month:
                    day.add_employee_to_holiday_list(employee)
                    employee.holidays.append(day)
                    holiday_counter += 1
                else :
                    self.employee_pool.append(employee)

                day_counter += 1
            work_days_template = self.update_work_days_template(work_days_template)
        self.clear_employee_pool()
        self.print()
        print()

    def create_employees(self, total_employee_required):
        return [Employee(employee_counter + 1) for employee_counter in range(total_employee_required)]

    def update_work_days_template(self, work_days_template):
        first_holiday_index = work_days_template.index(0)
        next_holiday_index = (first_holiday_index + 1) % len(work_days_template)
        print(work_days_template)
        for index in range(len(work_days_template)):
            if index == next_holiday_index or index == (next_holiday_index + 1) % len(work_days_template):
                work_days_template[index] = 0
            else:
                work_days_template[index] = 1

        return work_days_template

    def print(self):
        day_counter = 0
        for day in self.rooster:
            print("Day : {}, Employees : {}".format(day_counter + 1, len(day.employees_working)))
            day_counter += 1

        for employee in self.employees:
            working_days = [day.name for day in employee.working_days]
            holidays = [day.name for day in employee.holidays]
            print("Employee : {}, Working days [{}] : {}, Holidays [{}] : {}"
                  .format(employee.name, len(working_days), working_days, len(holidays), holidays))

    def clear_employee_pool(self):
        days_with_less_employees = [day for day in self.rooster if len(day.employees_working) < self.daily_employee_required]
        day_counter = 0
        if days_with_less_employees :
            for employee in self.employee_pool:
                day = days_with_less_employees[day_counter]
                day.add_employee_to_working_list(employee)
                employee.working_days.append(day)
                day_counter += 1

if __name__ == '__main__':
    rooster = Rooster(days_in_a_month, daily_employee_required, holidays_in_a_month)
    rooster.compute()
