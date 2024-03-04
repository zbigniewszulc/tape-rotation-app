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

SYSTEM_NAME = "TAPE ROTATION MANAGEMENT SYSTEM"
WELCOME_MSG = ("This CLI System is designed to manage and oversee the tape rotation \n"
    "schedule across different media types, including BRMS, DAILY, WEEKLY, and MONTHLY. \n"
    "It is tailored for IT department use, facilitating the monitoring and control of \n"
    "backup tape storage locations, whether onsite, offsite, or retired.")

def print_menu():
    data = [
        [1, "Engineer"],
        [2, "Designer"],
        [3, "Writer"]
    ]
    headers = ["#","Menu"]
    table = tabulate(data, headers=headers, tablefmt="simple")
    print(table)

def main():
    print(SYSTEM_NAME)
    print(WELCOME_MSG)
    print_menu()

main()
