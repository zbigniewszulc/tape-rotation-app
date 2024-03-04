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

SYSTEM_NAME = 24 * " " + " TAPE ROTATION MANAGEMENT SYSTEM " + 23 * " "
WELCOME_MSG = ("This CLI System is designed to manage and oversee the tape rotation schedule\n"
    "across different media types, including BRMS, DAILY, WEEKLY, and MONTHLY. \n"
    "It is tailored for IT department use, facilitating the monitoring and control of \n"
    "backup tape storage locations, whether onsite, offsite, or retired.")

def print_welcome_screen():
    print(80 * "=")
    print(SYSTEM_NAME)
    print(80 * "=")
    print(WELCOME_MSG)
    print(80 * "-" + "\n")

def print_menu():
    data = [
        [1, "Move tape offsite"],
        [2, "Move tape onsite"],
        [3, "Move tape to retired media pool"],
        [4, "Display all tapes stored offsite"],
        [5, "Display all tapes stored onsite"],
        [6, "Display all retired tapes"],
        [7, "Lookup"],
        [8, "Exit"]
    ]
    headers = ["#","Menu"]
    table = tabulate(data, headers=headers, tablefmt="simple")
    print(table)

def main():
    print_welcome_screen()
    print_menu()

main()
