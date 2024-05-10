from typing import Dict, List, Optional
import secrets
import os

"""
- Composition concept, the concept of passing down classes into other class.
"""

class Company:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.department_list: List[Department] = []
        self.employee_list: List[Employee] = []
    
    def add_department(self, department_name: str) -> str:
        for department in self.department_list:
            if department.name == department_name:
                return f"{department_name} is already a department"
        self.department_list.append(Department(department_name, self))
        return f"Created {department_name} department"

    def remove_department(self, department_name: str) -> str:
        for department in self.department_list:
            if department.name == department_name:
                self.department_list.remove(department)
                for employee in self.employee_list:
                    if employee.department == department_name:
                        employee.department = None
                        employee.position = None
                        employee.salary = 0
                return f"Removed {department_name} department"
        return f"Did not find '{department_name}' as department"

    def hire_employee(self, employee_name: str) -> str:
        self.employee_list.append(Employee(employee_name, self))
        return f"Hired {employee_name}"

    def fire_employee(self, employee_name: str) -> str:
        similar_employees = [index for index, employee in enumerate(self.employee_list) if employee.name == employee_name]
        
        if not similar_employees:
            return f"Did not found {employee_name} as employee"
        
        if len(similar_employees) == 1:
            self.employee_list.pop(similar_employees[0])
            return f"Fired '{employee_name}' from this company"
        
        while True:
            print("Employee with multiple name found:")
            for index in similar_employees:
                employee = self.employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Department: {employee.department} | Position: {employee.position}")
            try:
                input_index = input("Enter the index of the employee to remove or type 'cancel' to cancel: ")
                if input_index == "cancel":
                    return "Operation Canceled"
                
                input_index = int(input_index)
                if input_index in similar_employees:
                    self.employee_list.pop(input_index)
                    return f"Fired '{employee_name}' from this company"
                
                print("Invalid Index")
            except ValueError:
                print("Invalid Input")

    def get_department(self, department_name: str):
        for department in self.department_list:
            if department.name == department_name:
                return department
        return None
    
    def change_company_name(self, new_name: str) -> str:
        previous_name = self.name
        self.name = new_name
        return f"Changed this Company name from '{previous_name}' to '{new_name}'"
    
    def display_department_list(self) -> str:
        if not self.department_list:
            return "Empty"
        
        displayed_text: str = ""
        for department in self.department_list:
            displayed_text += f"- Name: {department.name}\n"
        return displayed_text
    
    def display_employee_list(self, exception_department: str = None) -> str:
        if not self.employee_list:
            return "Empty"
        
        displayed_text: str = ""
        for employee in self.employee_list:
            if exception_department is not None and employee.department == exception_department:
                continue # skip employee with matching department name
            displayed_text += f"{employee}\n"
        return displayed_text
    
    def display_company_status(self) -> str:
        company_name = self.name
        company_department_total = len(self.department_list)
        company_employee_total = len(self.employee_list)

        print(f"Company Name: {company_name}\nDepartment Total: {company_department_total}\nEmployee Total: {company_employee_total}")


class Department:
    def __init__(self, name: str, company: Company) -> None:
        self.name: str = name
        self.company: Company = company
        self.position_list: Dict[str, int] = {}
        self.department_employee_list: List[Employee] = []

    def add_position(self, position_name: str, position_salary: int) -> str:
        if position_name in self.position_list:
            return f"{position_name} is already a position"
        self.position_list[position_name] = position_salary
        return f"Added {position_name} as new position"

    def remove_position(self, position_name: str) -> str:
        if position_name in self.position_list:
            self.position_list.pop(position_name)
            for employee in self.department_employee_list:
                if employee.position == position_name:
                    employee.position = None
                    employee.salary = 0
            return f"Deleted {position_name} from position"
        return f"Did not found '{position_name}' as position"
        
    def change_position_salary(self, position_name: str, new_salary: int) -> str:
        if position_name in self.position_list:
            self.position_list[position_name] = new_salary
            for employee in self.department_employee_list:
                if employee.position == position_name:
                    employee.salary = new_salary
            return f"Changed '{position_name}' salary to ${new_salary}"
        return f"Did not found '{position_name}' as position"

    def add_employee(self, employee_name: str) -> str:
        similar_employees = [index for index, employee in enumerate(self.company.employee_list) if employee.name == employee_name and not employee.department == self.name]

        if not similar_employees:
            return f"Did not found {employee_name} as employee in '{self.company.name}' Company"
        
        if len(similar_employees) == 1:
            employee = self.company.employee_list[similar_employees[0]]
            employee.department = self.name
            employee.position = None
            employee.salary = 0
            self.department_employee_list.append(self.company.employee_list[similar_employees[0]])
            return f"Added '{employee_name}' to this department"
        
        while True:
            print("Employee with multiple name found:")
            for index in similar_employees:
                employee = self.company.employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Department: {employee.department}")
            try:
                input_index = input("Enter the index of the employee to add or type 'cancel' to cancel: ")
                if input_index == "cancel":
                    return "Operation Canceled"
                
                input_index = int(input_index)
                if input_index in similar_employees:
                    employee = self.company.employee_list[input_index]
                    employee.department = self.name
                    employee.position = None
                    employee.salary = 0
                    self.department_employee_list.append(self.company.employee_list[input_index])
                    return f"Added '{employee_name}' to this department"
                
                print("Invalid Index")
            except ValueError:
                print("Invalid Input")

    def remove_employee(self, employee_name: str) -> str:
        similar_employees = [index for index, employee in enumerate(self.department_employee_list) if employee.name == employee_name]

        if not similar_employees:
            return f"Did not found {employee_name} as employee in this department"

        if len(similar_employees) == 1:
            employee = self.department_employee_list[similar_employees[0]]
            employee.department = None
            employee.position = None
            employee.salary = 0
            self.department_employee_list.pop(similar_employees[0])
            return f"Removed '{employee_name}' from this department"
        
        while True:
            print("Employee with multiple name found:")
            for index in similar_employees:
                employee = self.department_employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Position: {employee.position}")
            try:
                input_index = input("Enter the index of the employee to remove or type 'cancel' to cancel: ")
                if input_index == "cancel":
                    return "Operation Canceled"
                
                input_index = int(input_index)
                if input_index in similar_employees:
                    employee = self.department_employee_list[input_index]
                    employee.department = None
                    employee.position = None
                    employee.salary = 0
                    self.department_employee_list.pop(input_index)
                    return f"Removed '{employee_name}' from this department"
                    
                print("Invalid Index")
            except ValueError:
                print("Invalid Input")

    def set_employee_position(self, employee_name: str, new_position: str) -> str:
        if new_position not in self.position_list:
            return f"Did not found '{new_position}' as position"

        similar_employees = [index for index, employee in enumerate(self.department_employee_list) if employee.name == employee_name]

        if not similar_employees:
            return f"Did not found {employee_name} as employee in this department"

        if len(similar_employees) == 1:
            employee = self.department_employee_list[similar_employees[0]]
            employee.position = new_position
            employee.salary = self.position_list.get(new_position)
            return f"Set '{employee_name}' position to '{new_position}'"
        
        while True:
            print("Employee with multiple name found:")
            for index in similar_employees:
                employee = self.department_employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Position: {employee.position}")
            try:
                input_employee_index = input("Enter the index of the employee to add or type 'cancel' to cancel: ")
                if input_employee_index == "cancel":
                    return "Operation Canceled"

                input_employee_index = int(input_employee_index)
                if input_employee_index in similar_employees:
                    employee = self.department_employee_list[input_employee_index]
                    employee.position = new_position
                    employee.salary = self.position_list.get(new_position)
                    return f"Set '{employee_name}' position to '{new_position}'"

                print("Invalid Index")
            except ValueError:
                print("Invalid Input")

    def change_department_name(self, new_name: str) -> str:
        previous_name = self.name
        self.name = new_name
        return f"Changed this Department name from '{previous_name}' to '{new_name}'"

    def display_position(self) -> str:
        if not self.position_list:
            return "Empty"
        return "\n".join(f"- Position: {position} | Salary: {salary}" for position, salary in self.position_list.items())
    
    def display_department_employee(self) -> str:
        if not self.department_employee_list:
            return "Empty"
        return "\n".join(f"Name: {employee.name} | Id: {employee.employee_Id} | Position: {employee.position}" for employee in self.department_employee_list)


class Employee:
    def __init__(self, name: str, company: Company) -> None:
        self.name: str = name
        self.company: Company = company
        self.employee_Id: int = secrets.randbits(32)
        self.department: Optional[Department] = None
        self.position: Optional[str] = None
        self.salary: int = 0

    def __str__(self) -> str:
        return f"Employee > Name: {self.name} | ID: {self.employee_Id} | Department: {self.department} | Worked as {self.position} with Salary ${self.salary}"


def main():
    def clear_terminal(): # Clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

    company_name = input("Enter the name of the company: ")
    while not isinstance(company_name, str) or not company_name.strip():
        print("Invalid input. Please enter a valid company name.")
        company_name = input("Enter the name of the company: ")
        clear_terminal()

    company: Company = Company(company_name)
    selected_department: Optional[Department] = None

    def add_department(): # 1 Choice
        department_name = input("Enter the name of the Department: ")
        print(company.add_department(department_name))

    def remove_department(): # 2 Choice
        if not company.department_list:
            print("Department is Empty")
        else:
            print(company.display_department_list())
            department_name = input("Enter the name of the Department to remove: ")
            print(company.remove_department(department_name))

    def hire_employee(): # 3 Choice
        employee_name = input("Enter the name of the Employee to hire: ")
        print(company.hire_employee(employee_name))

    def fire_employee(): # 4 Choice
        if not company.employee_list:
            print("Employee is Empty")
        else:
            print("\nEmployee List:")
            print(company.display_employee_list())
            employee_name = input("Enter the name of the Employee to fire: ")
            print(company.fire_employee(employee_name))

    def change_company_name(): # 5 Choice
        new_company_name = input("Enter the new name for the Company: ")
        print(company.change_company_name(new_company_name))

    def display_department_list(): # 6 Choice
        print("\nDepartment List:")
        print(company.display_department_list())

    def display_employee_list(): # 7 Choice
        print("\nEmployee List:")
        print(company.display_employee_list())

    def set_current_department(): # 8 Choice
        if not company.department_list:
            print("Department is Empty")
        else:
            print("\nDepartment List:")
            print(company.display_department_list())
            set_department = input("Enter the name of the Department to be selected: ")
            nonlocal selected_department
            selected_department = company.get_department(set_department)
            if selected_department is None:
                print("Invalid Department")

    def change_department_name(): # 9 Choice
        new_department_name = input("Enter the name for this Department: ")
        print(selected_department.change_department_name(new_department_name))

    def add_position(): # 10 Choice
        position_name = input("Enter the name of the Position: ")
        try:
            position_salary = int(input(f"Enter the Salary for '{position_name}' Position: "))
            print(selected_department.add_position(position_name, position_salary))
        except ValueError:
            print("Invalid Input. Expected Integer")

    def remove_position(): # 11 Choice
        if not selected_department.position_list:
            print("Position is Empty")
        else:
            print("\nPosition List:")
            print(selected_department.display_position())
            position_name = input("Enter the name of the Position to remove: ")
            print(selected_department.remove_position(position_name))

    def change_position_salary(): # 12 Choice
        if not selected_department.position_list:
            print("Position is Empty")
        else:
            print("\nPosition List:")
            print(selected_department.display_position())
            position_name = input("Enter the name of the Position: ")
            try:
                position_salary = int(input(f"Enter the new Salary for '{position_name}' Position: "))
                print(selected_department.change_position_salary(position_name, position_salary))
            except ValueError:
                print("Invalid Input. Expected Integer")

    def add_employee_to_department(): # 13 Choice
        if not company.employee_list:
            print("Company Employee is Empty")
        else:
            print("\nCompany Employee List:")
            print(company.display_employee_list(selected_department.name))
            employee_name = input("Enter the name of the Employee to add to this Department: ")
            print(selected_department.add_employee(employee_name))

    def remove_employee_from_department(): # 14 Choice
        if not selected_department.department_employee_list:
            print("Department Employee is Empty")
        else:
            print("\nDepartment Employee List:")
            print(selected_department.display_department_employee())
            employee_name = input("Enter the name of the Employee to be removed from this Department: ")
            print(selected_department.remove_employee(employee_name))

    def set_employee_position(): # 15 Choice
        if not selected_department.department_employee_list:
            print("Department Employee is Empty")
        elif not selected_department.position_list:
            print("Position is Empty")
        else:
            print("Department Employee:")
            print(selected_department.display_department_employee())
            print("Available Position:")
            print(selected_department.display_position())
            employee_name = input("Enter the name of the Employee: ")
            new_position = input("Enter the Position for this Employee: ")
            print(selected_department.set_employee_position(employee_name, new_position))

    def display_position(): # 16 Choice
        print("\nPosition List:")
        print(selected_department.display_position())

    def display_department_employee(): # 17 Choice
        print("\nDepartment Employee List:")
        print(selected_department.display_department_employee())

    choice_functions = {
        "1": add_department,
        "2": remove_department,
        "3": hire_employee,
        "4": fire_employee,
        "5": change_company_name,
        "6": display_department_list,
        "7": display_employee_list,
        "8": set_current_department,
        "9": change_department_name,
        "10": add_position,
        "11": remove_position,
        "12": change_position_salary,
        "13": add_employee_to_department,
        "14": remove_employee_from_department,
        "15": set_employee_position,
        "16": display_position,
        "17": display_department_employee
    }

    while True:
        clear_terminal()
        
        department_name = getattr(selected_department, "name", None)

        company.display_company_status()
        print(f"Current selected department: {department_name}")
        print("\nChoose an action:")
        print("0. Stop Program")
        print("1. Add Department")
        print("2. Remove Department")
        print("3. Hire Employee")
        print("4. Fire Employee")
        print("5. Change Company Name")
        print("6. Display Department List")
        print("7. Display Employee List")
        print("8. Set Current Department")
        if selected_department is not None:
            print("\nDepartment Method")
            print("9. Change Department Name")
            print("10. Add Position")
            print("11. Remove Position")
            print("12. Change Position Salary")
            print("13. Add Employee to this Department")
            print("14. Remove Employee from this Department")
            print("15. Set Employee Position inside this Department")
            print("16. Display Department Available Position")
            print("17. Display Department Available Employee")

        choice = input("\nEnter your choice: ")

        if selected_department is None and choice in ["9", "10", "11", "12", "13", "14", "15", "16", "17"]:
            print("Invalid Choice")
        elif choice in choice_functions:
            choice_functions[choice]()
        elif choice == "0":
            stop_input = input("Type 'yes' to stop program: ").lower()
            if stop_input == 'yes':
                print("Program Ended")
                break
            else:
                print("Operation canceled")
        else:
            print("Invalid Choice")

        input("\nPress Enter to continue...")
        clear_terminal()


if __name__ == "__main__":
    main()