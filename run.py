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
TXT_GREEN = "\033[32m"  # Console color:green

SYSTEM_NAME = 24 * " " + " TAPE ROTATION MANAGEMENT SYSTEM " + 23 * " "
WELCOME_MSG = (
    "\tThis CLI System is designed to manage and oversee the tape rotation \n"
    "\tschedule across different media types, including BRMS, DAILY, WEEKLY,\n"
    "\tand MONTHLY. It is tailored for IT department use, facilitating \n"
    "\tthe monitoring and control of backup tape storage locations, \n"
    "\twhether onsite, offsite, or retired.")

# Classes


class Menu:
    """
    Menu class with its methods and attributes
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
        self.headers = ["#", "Menu"]

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
            print("Numerical value expected. Try again..")
            return None

    def valid_usr_input(self):
        """
        Validate user input
        """
        while True:
            user_choice = get_numeric_input(
                "Enter your choice from the Menu: ")
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
            print(f"Your selection: {self.data[0][0]} {self.data[0][1]}")
            tape = Tape(get_numeric_input(
                "\nEnter the number of the tape to be moved: "))
            tape.move_with_rules(g_sheet, usr_input)
            continue_question()

        # 2  - Move tape onsite
        elif usr_input == 2:
            print(f"Your selection: {self.data[1][0]} {self.data[1][1]}")
            tape = Tape(get_numeric_input(
                "\nEnter the number of the tape to be moved: "))
            tape.move_with_rules(g_sheet, usr_input)
            continue_question()

        # 3  - Move tape to retired media pool
        elif usr_input == 3:
            print(f"Your selection: {self.data[2][0]} {self.data[2][1]}")
            tape = Tape(get_numeric_input(
                "\nEnter the number of the tape to be moved: "))
            tape.move_with_rules(g_sheet, usr_input)
            continue_question()

        # 4  - Display all tapes stored offsite
        elif usr_input == 4:
            print(f"Your selection: {self.data[3][0]} {self.data[3][1]}")
            print(g_sheet.disp_all_wrksht_val("Offsite"))
            continue_question()

        # 5  - Display all tapes stored onsite
        elif usr_input == 5:
            print(f"Your selection: {self.data[4][0]} {self.data[4][1]}")
            print(g_sheet.disp_all_wrksht_val("Onsite"))
            continue_question()

        # 6  - Display all retired tapes
        elif usr_input == 6:
            print(f"Your selection: {self.data[5][0]} {self.data[5][1]}")
            print(g_sheet.disp_all_wrksht_val("Retired"))
            continue_question()

        # 7  - Lookup
        elif usr_input == 7:
            print(f"Your selection: {self.data[6][0]} {self.data[6][1]}")
            tape = get_numeric_input("\nPlease enter tape number: ")
            lookup = GoogleSpreadsheet()
            workbooks = ["Offsite", "Onsite", "Retired"]
            for workbook in workbooks:
                results = lookup.lookup_results(workbook, tape)
                if results:
                    print(results)
            continue_question()

        #  8  - Exit
        elif usr_input == 8:
            print(f"Your selection: {self.data[7][0]} {self.data[7][1]}.")
            # Terminates the program in a fancy way using countdown
            countdwn_exit(3)
        else:
            print("No assigned function for given input")
            continue_question()


class Tape():
    """
    Tape class with its methods and attributes
    """

    def __init__(self, tape_number, tape_type=None):
        self.t_number = tape_number
        self.t_type = tape_type

    def get_types(self):
        """
        Get tape types
        """
        tape_types = ["BRMS", "DAILY", "WEEKLY", "MONTHLY"]
        return tape_types

    def get_and_val_t_type(self):
        """
        Validate user entry for tape type
        """
        while True:
            user_type = int(
                get_numeric_input(
                    f"\nEnter the type of "
                    f"{self.t_number} tape (options above): "))
            if 1 <= user_type <= len(self.get_types()):
                return user_type
            else:
                print("Invalid input. Try again..")
                time.sleep(1.5)

    def move_with_rules(self, g_sheet, menu_option):
        """
        Will move tape from one worksheet to other based on rules
        and Menu option sleected.
        1) Moving tapes to Onsite worksheet is allowed from any other worksheet
        2) Moving to Retired worksheet is possible only from Onsite worksheet
        3) Moving to Offsite worksheet is possible only from Onsite worksheet
        """
        current_date = get_current_date()
        # Rules based on what Menu option provided
        if (menu_option == 1):
            worksheet_seq = ["Offsite", "Onsite", "Retired"]
        elif (menu_option == 2):
            worksheet_seq = ["Onsite", "Offsite", "Retired"]
        elif (menu_option == 3):
            worksheet_seq = ["Retired", "Onsite", "Offsite"]
        else:
            print("Given Menu option is uknown")
        # Check if the tape is already in the destination location.
        # If it is, no action is needed.
        print(f"Checking {worksheet_seq[0]} tapes..")
        seq0_tapes = g_sheet.find_all_cells(worksheet_seq[0], self.t_number)
        if not seq0_tapes:
            seq1_tapes = g_sheet.find_all_cells(
                worksheet_seq[1], self.t_number)
            seq2_tapes = g_sheet.find_all_cells(
                worksheet_seq[2], self.t_number)
            print(f"Checking {worksheet_seq[1]} tapes..")
            if seq1_tapes:
                # Check if the tape is in worksheet_seq[1].
                # If it is move tape data from worksheet_seq[1] to
                # worksheet_seq[0]
                self.move_from_to_worksheet(
                    g_sheet, worksheet_seq[1], worksheet_seq[0], seq1_tapes)
            elif seq2_tapes:
                # Check if the tape is worksheet_seq[2].
                # If it is print message that this operation is not allowed
                print(f"Checking {worksheet_seq[2]} tapes.. \n")
                if (menu_option == 2):
                    # In case if Menu option 2 was provided
                    # Move tape data from 'Retired' to 'Onsite'
                    self.move_from_to_worksheet(
                        g_sheet, worksheet_seq[2], worksheet_seq[0],
                        seq2_tapes)
                else:
                    print("This move is not allowed! \n"
                          f"Tape {self.t_number} is {worksheet_seq[2]}. \n"
                          f"Only '{worksheet_seq[1]}' tapes can be moved to "
                          f"'{worksheet_seq[0]}'")
            else:
                if (menu_option == 2):
                    # In case if Menu option 2 was provided
                    print(f"Tape number {self.t_number} is not in the tape set"
                          "\nThis new tape will be added to the pool. \n"
                          "Please provide more details.. \n"
                          "\nAvailable media types: ")
                    tape_types = self.get_types()
                    # Display tape types
                    for i in range(len(tape_types)):
                        print(f"[{i + 1}] - {tape_types[i]}")
                    # Get and validate user entry for tape type
                    user_type = self.get_and_val_t_type()
                    # Get String value of the tape type
                    self.t_type = tape_types[user_type - 1]

                    # Open Google Sheet and append row
                    wrksheet = g_sheet.open_worksheet(worksheet_seq[0])
                    wrksheet.append_row(
                        [self.t_number, self.t_type, current_date])
                    print("Data entered successfully!\n")
                else:
                    print("\nThis move is not allowed! \n")
                    print(
                        f"Tape number {self.t_number} is not in the tape set\n"
                        f"This new tape should initially be moved to the "
                        f"'{worksheet_seq[1]}' location \n")
        else:
            print(
                f"Nothing to do. Tape {
                    self.t_number} is already '{
                    worksheet_seq[0]}'!\n")

    def move_from_to_worksheet(
            self,
            g_sheet,
            from_wrksht,
            to_wrksht,
            tape_cells):
        """
        Move tape data from one Google Sheet to another.
        """
        wrksheet = g_sheet.open_worksheet(from_wrksht)
        all_records = wrksheet.get_all_values()
        # Reverse iterator to remove records from the bottom of Google Sheet
        # ..to avoid removing process issues
        # (not all records removes in regular iterator order)
        for t_row in reversed(tape_cells):
            row_num = t_row.row
            # Copy values to temp variable
            # e.g.['3408', 'BRMS', '08/03/2024']
            temp_record = all_records[row_num - 1]
            # Change current date
            temp_record[2] = get_current_date()
            wrksheet.delete_rows(row_num)
            g_sheet.open_worksheet(to_wrksht).append_row(temp_record)
            print(f"The tape {self.t_number} has been moved from "
                  f"'{from_wrksht}' to '{to_wrksht}' successfully! \n")


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
        """
        Opens worksheet
        """
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
        headers = all_records[0]  # Get first element of the list
        # Slice table, skip the first element of the list
        data = all_records[1:]
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
        user_input = input(prompt + "\n")
        # https://docs.python.org/3/library/stdtypes.html#str.isdigit
        if user_input.isdigit():
            return user_input
        else:
            print("Please eneter only numbers without any spaces. Try again..")
            time.sleep(1.5)


def continue_question():
    """
    If user wants to proceed it will print Menu on screen
    If 'n' select program will terminate
    """
    while True:
        # Convert input to lower case
        answer = input("\nWould you like to continue [y/n]?: ").lower()
        if (answer == "y"):
            menu_deploy()
        elif (answer == "n"):
            countdwn_exit(3)
        else:
            print("Invalid key entered. Try again..")


def menu_deploy():
    """
    Prints Menu on screen
    """
    # Render menu
    menu = Menu()
    print("\n" + menu.render_menu() + "\n")
    # Get valid user's menu input
    usr_input = menu.valid_usr_input()
    menu.process_input(usr_input)


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
    print("\nTerminating the program")
    for i in range(sec, 0, -1):
        print(i)
        time.sleep(1)
    print("Bye Bye!")
    # Delay 2 sec https://docs.python.org/3/library/time.html#time.sleep
    time.sleep(2)
    return sys.exit()  # https://docs.python.org/3/library/sys.html#sys.exit


def main():
    """
    This is where all flow begins
    """
    # Variables
    # Welcome screen
    print(TXT_GREEN)  # Use console font color green
    print_welcome_screen()
    menu_deploy()


main()
