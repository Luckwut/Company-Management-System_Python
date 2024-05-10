from typing import Dict, List, Optional
import secrets
import os

class Company:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.department_list: List[Department] = []
        self.employee_list: List[Employee] = []
    
    def add_department(self, department_name: str) -> str:
        for department in self.department_list:
            if department.name == department_name:
                return f"'{department_name}' sudah menjadi department"
        self.department_list.append(Department(department_name, self))
        return f"'{department_name}' department telah dibuat"

    def remove_department(self, department_name: str) -> str:
        for department in self.department_list:
            if department.name == department_name:
                self.department_list.remove(department)
                for employee in self.employee_list:
                    if employee.department == department_name:
                        employee.department = None
                        employee.position = None
                        employee.salary = 0
                return f"'{department_name}' department telah dihapus"
        return f"Tidak menemukan '{department_name}' sebagai department"

    def hire_employee(self, employee_name: str) -> str:
        self.employee_list.append(Employee(employee_name, self))
        return f"'{employee_name}' telah direkrut"

    def fire_employee(self, employee_name: str) -> str:
        similar_employees = [index for index, employee in enumerate(self.employee_list) if employee.name == employee_name]
        
        if not similar_employees:
            return f"Tidak menemukan {employee_name} sebagai pegawai"
        
        if len(similar_employees) == 1:
            self.employee_list.pop(similar_employees[0])
            return f"'{employee_name}' telah dipecat dari perusahaan ini"
        
        while True:
            print("Ditemukan pegawai dengan nama yang sama:")
            for index in similar_employees:
                employee = self.employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Department: {employee.department} | Position: {employee.position}")
            try:
                input_index = input("Masukkan indeks pegawai yang akan dihapus atau ketik 'cancel' untuk membatalkan: ")
                if input_index == "cancel":
                    return "Operation Canceled"
                
                input_index = int(input_index)
                if input_index in similar_employees:
                    self.employee_list.pop(input_index)
                    return f"'{employee_name}' telah dipecat dari perusahaan ini"
                
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
        return f"Nama Perusahaan telah diubah dari '{previous_name}' menjadi '{new_name}'"
    
    def display_department_list(self) -> str:
        if not self.department_list:
            return "Empty"
        
        displayed_text: str = ""
        for department in self.department_list:
            displayed_text += f"- Nama: {department.name}\n"
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

        print(f"Nama Perusahaan: {company_name}\nTotal Department: {company_department_total}\nTotal Pegawai: {company_employee_total}")


class Department:
    def __init__(self, name: str, company: Company) -> None:
        self.name: str = name
        self.company: Company = company
        self.position_list: Dict[str, int] = {}
        self.department_employee_list: List[Employee] = []

    def add_position(self, position_name: str, position_salary: int) -> str:
        if position_name in self.position_list:
            return f"{position_name} sudah menjadi position"
        self.position_list[position_name] = position_salary
        return f"'{position_name}' ditambahkan sebagai position baru"

    def remove_position(self, position_name: str) -> str:
        if position_name in self.position_list:
            self.position_list.pop(position_name)
            for employee in self.department_employee_list:
                if employee.position == position_name:
                    employee.position = None
                    employee.salary = 0
            return f"'{position_name}' dihapus dari position"
        return f"Tidak menemukan '{position_name}' sebagai position"
        
    def change_position_salary(self, position_name: str, new_salary: int) -> str:
        if position_name in self.position_list:
            self.position_list[position_name] = new_salary
            for employee in self.department_employee_list:
                if employee.position == position_name:
                    employee.salary = new_salary
            return f"Mengubah gaji position '{position_name}' menjadi ${new_salary}"
        return f"Tidak menemukan '{position_name}' sebagai position"

    def add_employee(self, employee_name: str) -> str:
        similar_employees = [index for index, employee in enumerate(self.company.employee_list) if employee.name == employee_name and not employee.department == self.name]

        if not similar_employees:
            return f"Tidak menemukan {employee_name} sebagai pegawai di Perusahaan '{self.company.name}'"
        
        if len(similar_employees) == 1:
            employee = self.company.employee_list[similar_employees[0]]
            employee.department = self.name
            employee.position = None
            employee.salary = 0
            self.department_employee_list.append(self.company.employee_list[similar_employees[0]])
            return f"'{employee_name}' ditambahkan ke departemen ini"
        
        while True:
            print("Ditemukan pegawai dengan nama yang sama:")
            for index in similar_employees:
                employee = self.company.employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Department: {employee.department}")
            try:
                input_index = input("Masukkan indeks pegawai yang akan dihapus atau ketik 'cancel' untuk membatalkan: ")
                if input_index == "cancel":
                    return "Operation Canceled"
                
                input_index = int(input_index)
                if input_index in similar_employees:
                    employee = self.company.employee_list[input_index]
                    employee.department = self.name
                    employee.position = None
                    employee.salary = 0
                    self.department_employee_list.append(self.company.employee_list[input_index])
                    return f"'{employee_name}' ditambahkan ke departemen ini"
                
                print("Invalid Index")
            except ValueError:
                print("Invalid Input")

    def remove_employee(self, employee_name: str) -> str:
        similar_employees = [index for index, employee in enumerate(self.department_employee_list) if employee.name == employee_name]

        if not similar_employees:
            return f"Tidak menemukan {employee_name} sebagai pegawai di Perusahaan '{self.company.name}'"

        if len(similar_employees) == 1:
            employee = self.department_employee_list[similar_employees[0]]
            employee.department = None
            employee.position = None
            employee.salary = 0
            self.department_employee_list.pop(similar_employees[0])
            return f"'{employee_name}' dihapus dari departemen ini"
        
        while True:
            print("Ditemukan pegawai dengan nama yang sama:")
            for index in similar_employees:
                employee = self.department_employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Position: {employee.position}")
            try:
                input_index = input("Masukkan indeks pegawai yang akan dihapus atau ketik 'cancel' untuk membatalkan: ")
                if input_index == "cancel":
                    return "Operation Canceled"
                
                input_index = int(input_index)
                if input_index in similar_employees:
                    employee = self.department_employee_list[input_index]
                    employee.department = None
                    employee.position = None
                    employee.salary = 0
                    self.department_employee_list.pop(input_index)
                    return f"'{employee_name}' dihapus dari departemen ini"
                    
                print("Invalid Index")
            except ValueError:
                print("Invalid Input")

    def set_employee_position(self, employee_name: str, new_position: str) -> str:
        if new_position not in self.position_list:
            return f"Tidak menemukan '{new_position}' sebagai position"

        similar_employees = [index for index, employee in enumerate(self.department_employee_list) if employee.name == employee_name]

        if not similar_employees:
            return f"Tidak menemukan {employee_name} sebagai pegawai di Perusahaan '{self.company.name}'"

        if len(similar_employees) == 1:
            employee = self.department_employee_list[similar_employees[0]]
            employee.position = new_position
            employee.salary = self.position_list.get(new_position)
            return f"'{employee_name}' position diatur menjadi '{new_position}'"
        
        while True:
            print("Ditemukan pegawai dengan nama yang sama:")
            for index in similar_employees:
                employee = self.department_employee_list[index]
                print(f"{index}: {employee.name} | Id: {employee.employee_Id} | Position: {employee.position}")
            try:
                input_employee_index = input("Masukkan indeks pegawai yang akan dihapus atau ketik 'cancel' untuk membatalkan: ")
                if input_employee_index == "cancel":
                    return "Operation Canceled"

                input_employee_index = int(input_employee_index)
                if input_employee_index in similar_employees:
                    employee = self.department_employee_list[input_employee_index]
                    employee.position = new_position
                    employee.salary = self.position_list.get(new_position)
                    return f"'{employee_name}' position diatur menjadi '{new_position}'"

                print("Invalid Index")
            except ValueError:
                print("Invalid Input")

    def change_department_name(self, new_name: str) -> str:
        previous_name = self.name
        self.name = new_name
        return f"Merubah nama Department ini dari '{previous_name}' menjadi '{new_name}'"

    def display_position(self) -> str:
        if not self.position_list:
            return "Empty"
        return "\n".join(f"- Position: {position} | Gaji: ${salary}" for position, salary in self.position_list.items())
    
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
        return f"Employee > Name: {self.name} | ID: {self.employee_Id} | Department: {self.department} | Bekerja sebagai {self.position} dengan Gaji ${self.salary}"


def main():
    def clear_terminal(): # Clear Terminal
        os.system('cls' if os.name == 'nt' else 'clear')
    
    company_name = input("Masukkan nama perusahaan: ")
    while not isinstance(company_name, str) or not company_name.strip():
        print("Input tidak valid. Silakan masukkan nama perusahaan yang valid.")
        company_name = input("Masukkan nama perusahaan: ")
        clear_terminal()

    company: Company = Company(company_name)
    selected_department: Optional[Department] = None

    def add_department(): # Choice 1
        department_name = input("Masukkan nama Departemen: ")
        print(company.add_department(department_name))

    def remove_department(): # Choice 2
        if not company.department_list:
            print("Departemen kosong")
        else:
            print(company.display_department_list())
            department_name = input("Masukkan nama Departemen yang akan dihapus: ")
            print(company.remove_department(department_name))

    def hire_employee(): # Choice 3
        employee_name = input("Masukkan nama Pegawai yang akan direkrut: ")
        print(company.hire_employee(employee_name))

    def fire_employee(): # Choice 4
        if not company.employee_list:
            print("Pegawai kosong")
        else:
            print("\nDaftar Pegawai:")
            print(company.display_employee_list())
            employee_name = input("Masukkan nama Pegawai yang akan dipecat: ")
            print(company.fire_employee(employee_name))

    def change_company_name(): # Choice 5
        new_company_name = input("Masukkan nama baru untuk Perusahaan: ")
        print(company.change_company_name(new_company_name))

    def display_department_list(): # Choice 6
        print("\nDaftar Departemen:")
        print(company.display_department_list())

    def display_employee_list(): # Choice 7
        print("\nDaftar Pegawai:")
        print(company.display_employee_list())

    def set_current_department(): # Choice 8
        if not company.department_list:
            print("Departemen kosong")
        else:
            print("\nDaftar Departemen:")
            print(company.display_department_list())
            set_department = input("Masukkan nama Departemen yang akan dipilih: ")
            nonlocal selected_department
            selected_department = company.get_department(set_department)
            if selected_department is None:
                print("Departemen tidak valid")

    def change_department_name(): # Choice 9
        new_department_name = input("Masukkan nama untuk Departemen ini: ")
        print(selected_department.change_department_name(new_department_name))

    def add_position(): # Choice 10
        position_name = input("Masukkan nama Posisi: ")
        try:
            position_salary = int(input(f"Masukkan Gaji untuk Posisi '{position_name}': "))
            print(selected_department.add_position(position_name, position_salary))
        except ValueError:
            print("Input tidak valid. Diperlukan bilangan bulat")

    def remove_position(): # Choice 11
        if not selected_department.position_list:
            print("Posisi kosong")
        else:
            print("\nDaftar Posisi:")
            print(selected_department.display_position())
            position_name = input("Masukkan nama Posisi yang akan dihapus: ")
            print(selected_department.remove_position(position_name))

    def change_position_salary(): # Choice 12
        if not selected_department.position_list:
            print("Posisi kosong")
        else:
            print("\nDaftar Posisi:")
            print(selected_department.display_position())
            position_name = input("Masukkan nama Posisi: ")
            try:
                position_salary = int(input(f"Masukkan Gaji baru untuk Posisi '{position_name}': "))
                print(selected_department.change_position_salary(position_name, position_salary))
            except ValueError:
                print("Input tidak valid. Diperlukan bilangan bulat")

    def add_employee_to_department(): # Choice 13
        if not company.employee_list:
            print("Pegawai Perusahaan kosong")
        else:
            print("\nDaftar Pegawai Perusahaan:")
            print(company.display_employee_list(selected_department.name))
            employee_name = input("Masukkan nama Pegawai yang akan ditambahkan ke Departemen ini: ")
            print(selected_department.add_employee(employee_name))

    def remove_employee_from_department(): # Choice 14
        if not selected_department.department_employee_list:
            print("Pegawai Departemen kosong")
        else:
            print("\nDaftar Pegawai Departemen:")
            print(selected_department.display_department_employee())
            employee_name = input("Masukkan nama Pegawai yang akan dihapus dari Departemen ini: ")
            print(selected_department.remove_employee(employee_name))

    def set_employee_position(): # Choice 15
        if not selected_department.department_employee_list:
            print("Pegawai Departemen kosong")
        elif not selected_department.position_list:
            print("Posisi kosong")
        else:
            print("Pegawai Departemen:")
            print(selected_department.display_department_employee())
            print("Posisi Tersedia:")
            print(selected_department.display_position())
            employee_name = input("Masukkan nama Pegawai: ")
            new_position = input("Masukkan Posisi untuk Pegawai ini: ")
            print(selected_department.set_employee_position(employee_name, new_position))

    def display_position(): # Choice 16
        print("\nDaftar Posisi:")
        print(selected_department.display_position())

    def display_department_employee(): # Choice 17
        print("\nDaftar Pegawai Departemen:")
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
        print(f"Departemen terpilih saat ini: {department_name}")
        print("\nPilih tindakan:")
        print("0. Keluar dari Program")
        print("1. Tambah Departemen")
        print("2. Hapus Departemen")
        print("3. Rekrut Pegawai")
        print("4. Pecat Pegawai")
        print("5. Ubah Nama Perusahaan")
        print("6. Tampilkan Daftar Departemen")
        print("7. Tampilkan Daftar Pegawai")
        print("8. Tetapkan Departemen Saat Ini")
        if selected_department is not None:
            print("\nMetode Departemen")
            print("9. Ubah Nama Departemen")
            print("10. Tambah Posisi")
            print("11. Hapus Posisi")
            print("12. Ubah Gaji Posisi")
            print("13. Tambah Pegawai ke Departemen ini")
            print("14. Keluarkan Pegawai dari Departemen ini")
            print("15. Tetapkan Posisi Pegawai di Departemen ini")
            print("16. Tampilkan Posisi Tersedia dalam Departemen")
            print("17. Tampilkan Pegawai Tersedia dalam Departemen")

        choice = input("\nMasukkan pilihan Anda: ")

        if selected_department is None and choice in ["9", "10", "11", "12", "13", "14", "15", "16", "17"]:
            print("Pilihan tidak valid")
        elif choice in choice_functions:
            choice_functions[choice]()
        elif choice == "0":
            stop_input = input("Ketik 'ya' untuk menghentikan program: ").lower()
            if stop_input == 'ya':
                print("Program berhenti")
                break
            else:
                print("Operation canceled")
        else:
            print("Pilihan tidak valid")

        input("\nTekan Enter untuk melanjutkan...")
        clear_terminal()


if __name__ == "__main__":
    main()