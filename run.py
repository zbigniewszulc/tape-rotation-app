# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Import modules, packages or libraries
import gspread 
from google.oauth2.service_account import Credentials
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
    
    def get_selection(self):
        """
        Return menu option selected
        """
        choice = input("Enter your choice from the Menu: ")
        return choice
    
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
        while True:
            user_choice = self.get_selection()
            validated_choice = self.get_valid_selection(user_choice)
            if validated_choice:
                return validated_choice
            
    # Menu options       
    def display_all_tapes(self, worksheet):
        print(f"Fetching data for: {worksheet} tapes")
        spreadsheet = GoogleSpreadsheet()
        wrksheet = spreadsheet.open_worksheet(worksheet)
        all_records = wrksheet.get_all_values()
        headers = all_records[0] # Get first element of the list
        data = all_records[1:] # Slice table, skip the first element of the list
        table_format = "psql"
        table = render_table(data, headers, table_format) 
        return table

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

def render_table(data, headers, tablefmt):
    table = tabulate(data, headers, tablefmt)
    return table

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

    print(TXT_GREEN) # Use console font color green
    print_welcome_screen()
    print(menu.render_menu())
    print("\n")
    # Get valid user's menu input
    usr_input = menu.valid_usr_input()
    print(f"You have selected: {usr_input}")

    print(menu.display_all_tapes("Offsite"))

main()
