# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Import modules, packages or libraries
import gspread 
from google.oauth2.service_account import Credentials
from tabulate import tabulate

# Declare constant variables
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('tape_rotation')

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
    def __init__(self):
        self.data = [
            [1, "- Move tape offsite"],
            [2, "- Move tape onsite"],
            [3, "- Move tape to retired media pool"],
            [4, "- Display all tapes stored offsite"],
            [5, "- Display all tapes stored onsite"],
            [6, "- Display all retired tapes"],
            [7, "- Lookup"],
            [8, "- Exit"]
        ]
        self.headers = ["#","Menu"]   

    def print_menu(self, tablefmt):
        """
        Display menu
        """
        self.tablefmt=tablefmt
        table = tabulate(self.data, self.headers, self.tablefmt)
        return table
    
    def get_selection(self):
        """
        Return menu option selected
        """
        choice = input("Enter your choice from the Menu: ")
        return choice
    
    def validate_selection(self, user_choice):
            """
            Validate menu option selected
            """
            # Exception handling - user input validation. Errors expected 
            try:
                # Attempt to convert user choice to integer
                choice_int = int(user_choice)

                if (1 <= choice_int <= 8):
                    return True
                else:
                    raise ValueError(f"Valid menu options are: 1 through 8.")
                
            except ValueError as e:
                print(f"Your entry: '{user_choice}'. Error: {e}.. Try again!")    
                return False


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

def main():
    """
    This is where all flow begins
    """
    # Variables
    menu = Menu()

    print(TXT_GREEN) # Use console font color green
    print_welcome_screen()
    print(menu.print_menu("simple"))
    print("\n")
    
    while True:
        user_choice = menu.get_selection()
        if menu.validate_selection(user_choice):
            break # Exit the loop if a valid menu option was entered
    

main()
