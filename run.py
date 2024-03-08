# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Import modules, packages or libraries

# https://docs.python.org/3/library/sys.html
import sys                      

# https://docs.python.org/3/library/time.html
import time   

# https://docs.python.org/3/library/datetime.html
from datetime import datetime

# https://docs.gspread.org/en/latest/index.html
import gspread      

# https://google-auth.readthedocs.io/en/master/reference/modules.html
from google.oauth2.service_account import Credentials  

# https://pypi.org/project/tabulate/
from tabulate import tabulate   

# Declare constant variables
TXT_GREEN = "\033[32m" # Console color:green 

SYSTEM_NAME = 24 * " " + " TAPE ROTATION MANAGEMENT SYSTEM " + 23 * " "
WELCOME_MSG = ("This CLI System is designed to manage and oversee the tape rotation schedule\n"
    "across different media types, including BRMS, DAILY, WEEKLY, and MONTHLY. \n"
    "It is tailored for IT department use, facilitating the monitoring and control of \n"
    "backup tape storage locations, whether onsite, offsite, or retired.")

# Classes
class Menu:
    """
    Menu class with its methods
    """
    def __init__(self, data, headers):
        self.data = data
        self.headers = headers  

    def render_menu(self):
        """
        Render menu in form of table
        """
        table_format = "simple"
        table = render_table(self.data, self.headers, table_format)
        return table
    
    def get_valid_selection(self, user_choice):
        """
        Validate menu option selected
        """
        # Number of options in Menu
        num_of_opt = len(self.data)
        # Exception handling - user input validation. Errors expected 
        try:
            # Attempt to convert user choice to integer
            choice_int = int(user_choice) 
            if 1 <= choice_int <= num_of_opt:
                return choice_int
            else:
                print("Please select menu option from 1 to 8.")
                return None
        except ValueError:
            # Raise custom exception 
            print ("Numerical value expected. Try again..")
            return None
    
    def valid_usr_input(self):
        """
        Validate user input
        """
        while True:
            user_choice = get_numeric_input("Enter your choice from the Menu: ")
            validated_choice = self.get_valid_selection(user_choice)
            if validated_choice:
                return validated_choice
            
    # Menu options
    def process_input(self, usr_input):
        """
        Manage flow based on user selection from the Menu
        """
        g_sheet = GoogleSpreadsheet()

        # 1  - Move tape offsite
        if usr_input == 1:
            print(f"\nYour selection: {self.data[0][0]} {self.data[0][1]}")
            
        # 2  - Move tape onsite
        elif usr_input == 2:
            print(f"\nYour selection: {self.data[1][0]} {self.data[1][1]}")
            current_date = get_current_date()
            tape = get_numeric_input("Enter the number of the tape to be moved: ")
            tape_types = ["BRMS", "DAILY", "WEEKLY", "MONTHLY"]
            print("Type of tapes available: ")
            for i  in range(len(tape_types)):
                print(f"[{i+1}] - {tape_types[i]}")
            
            # Validate user entry for tape type
            while True:
                user_type = int(get_numeric_input(f"Enter the type of {tape} tape: "))
                if 1 <= user_type <= len(tape_types):
                    break
                else:
                    print("Invalid input. Try again..")  
            
            tape_type = tape_types[user_type-1] # Get String value of the tape type
            wrksheet = g_sheet.open_worksheet("Onsite")
            wrksheet.append_row([tape, tape_type, current_date])
        
        # 3  - Move tape to retired media pool
        elif usr_input == 3:
            print(f"\nYour selection: {self.data[2][0]} {self.data[2][1]}")
  
        
        # 4  - Display all tapes stored offsite
        elif usr_input == 4:
            print(f"\nYour selection: {self.data[3][0]} {self.data[3][1]}")
            print(g_sheet.disp_all_wrksht_val("Offsite"))
        
        # 5  - Display all tapes stored onsite
        elif usr_input == 5:
            print(f"\nYour selection: {self.data[4][0]} {self.data[4][1]}")
            print(g_sheet.disp_all_wrksht_val("Onsite"))
        
        # 6  - Display all retired tapes
        elif usr_input == 6:
            print(f"\nYour selection: {self.data[5][0]} {self.data[5][1]}")
            print(g_sheet.disp_all_wrksht_val("Retired"))
        
        # 7  - Lookup
        elif usr_input == 7:
            print(f"\nYour selection: {self.data[6][0]} {self.data[6][1]}")
            tape=get_numeric_input("Please enter tape number: ")
            lookup = GoogleSpreadsheet()
            workbooks = ["Offsite", "Onsite", "Retired"]
            for workbook in workbooks:
                results = lookup.lookup_results(workbook, tape)
                if results:
                    print(results)

        #  8  - Exit        
        elif usr_input == 8:
            print(f"\nYour selection: {self.data[7][0]} {self.data[7][1]}.")
            print("Terminating the program")
            # Terminates the program in a fancy way using countdown
            countdwn_exit(3)
        else:
            print("No assigned function for given input")

class GoogleSpreadsheet():
    """
    Google spreadsheet class with its attributes and methods
    """
    def __init__(self):
        self.SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]
        self.CREDS = Credentials.from_service_account_file('creds.json')
        self.SCOPED_CREDS = self.CREDS.with_scopes(self.SCOPE)
        self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
        self.SHEET = self.GSPREAD_CLIENT.open("tape_rotation")

    def open_worksheet(self, worksheet):
        return self.SHEET.worksheet(worksheet)
    
    def get_headers(self, worksheet):
        """
        Returns list of headers of worksheet  
        """
        wrksheet = self.open_worksheet(worksheet)
        headers = wrksheet.row_values(1)
        return headers
    
    def find_all_cells(self, worksheet, tape):
        """
        Find all entries of provided tape number in worksheet. 
        Returns list of objects, e.g. [<Cell R4C1 '5544'>, <Cell R5C1 '5544'>] 
        """
        wrksheet = self.open_worksheet(worksheet)
        cell_list = wrksheet.findall(tape, in_column=1)
        return cell_list
    
    def disp_all_wrksht_val(self, worksheet):
        """
        Fetch and return all values in worksheet in form of table 
        """
        print(f"\nFetching data for: {worksheet} tapes")
        wrksheet = self.open_worksheet(worksheet)
        all_records = wrksheet.get_all_values()
        headers = all_records[0] # Get first element of the list
        data = all_records[1:] # Slice table, skip the first element of the list
        if (len(data)) > 0:
            table_format = "psql"
            table = render_table(data, headers, table_format) 
            return table
        else:
            return "There are no records for " + worksheet + " tapes yet"
    
    def lookup_results(self, worksheet, tape):
        print(f"\nSearching {worksheet} tapes for: {tape}")
        results = self.find_all_cells(worksheet, tape)
        print(f"Lookup results: {len(results)} entries found")
        if len(results) != 0:
            rows = []
            all_row_val = []
            # Get row number (from object property) and append to 'rows' list
            for result in results:
                rows.append(result.row)
            # Get all rows values and append to all_row_val list    
            for row in rows:
                wrksheet = self.open_worksheet(worksheet)
                all_row_val.append(wrksheet.row_values(row))
            headers = self.get_headers(worksheet)
            table = (render_table(all_row_val, headers, "psql"))
            return table
        else: 
            return len(results)

# Functions
def print_welcome_screen():
    """
    Display program introduction message 
    """
    print(80 * "=")
    print(SYSTEM_NAME)
    print(80 * "=")
    print(WELCOME_MSG)
    print(80 * "-" + "\n")

def get_current_date():
    return datetime.now().strftime("%d/%m/%Y")    

def get_numeric_input(prompt):
    """
    It takes user numeric input from user. Allows to set own prompt
    """
    while True:
        user_input = input(prompt)
        # https://docs.python.org/3/library/stdtypes.html#str.isdigit
        if user_input.isdigit():    
            return user_input 
        else:
            print("Only numeric input allowed. Try again..")

def render_table(data, headers, tablefmt):
    """
    Render table using tabulate module
    """
    table = tabulate(data, headers, tablefmt)
    return table

def countdwn_exit(sec):
    """
    It terminates the program using built in sys and time module
    """
    for i in range(sec, 0, -1):
        print(i)
        time.sleep(1)
    print("Bye Bye!")   
    # Delay 2 sec https://docs.python.org/3/library/time.html#time.sleep
    time.sleep(2)
    return sys.exit() # https://docs.python.org/3/library/sys.html#sys.exit

def main():
    """
    This is where all flow begins
    """
    # Variables
    # Data to build Menu
    menu_headers = ["#","Menu"]
    menu_data = [
            [1, "- Move tape offsite"],
            [2, "- Move tape onsite"],
            [3, "- Move tape to retired media pool"],
            [4, "- Display all tapes stored offsite"],
            [5, "- Display all tapes stored onsite"],
            [6, "- Display all retired tapes"],
            [7, "- Lookup"],
            [8, "- Exit"]
        ]
    menu = Menu(menu_data, menu_headers)

    # Welcome screen
    print(TXT_GREEN) # Use console font color green
    print_welcome_screen()

    # Render menu
    print(menu.render_menu())
    print("\n")

    # Get valid user's menu input
    usr_input = menu.valid_usr_input()
    menu.process_input(usr_input)


main()
