class Day :
    def __init__(self, name):
        self.name = name
        self.employees_working = []
        self.employees_not_working = []

    def add_employee_to_working_list(self, employee):
        self.employees_working.append(employee)

    def add_employee_to_holiday_list(self, employee):
        self.employees_not_working.append(employee)

