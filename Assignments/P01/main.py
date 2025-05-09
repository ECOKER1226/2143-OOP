"""
  Author:           Ezekiel Coker
  Email:            erycoker23@my.msutexas.edu
  Label:            P01
  Title:            Json Database Project
  Course:           CMPS 2143
  Semester:         Spring 2025

  Description:
        This program implements a JSON-based database system for managing
        structured user records. The JsonDB class provides essential CRUD
        operations, handling file interactions and ensuring data integrity.
        Building on this, the PeopleDB subclass specializes in managing
        "people" data, allowing searches by attributes like name, phone,
        email, and location. With a modular design, the system is easy to
        maintain, extend, and test through if __name__ == "main":,
        working directly with real data in random_people.10000.json.

  Usage:
        - python main.py
        - Typing this in the terminal will allow you to access the menu.

  Files:
        main.py                     : main menu file
        jsonDB.py                   : parent class file
        peopleDB.py                 : child class file
        random_people.10000.json    : json file
"""

import json
import os
import re
import inquirer
from rich import print
from jsonDB import JsonDB
from peopleDB import PeopleDB
from datetime import datetime, timezone

DB_FILE = "people.json"

def main():
    db = PeopleDB(DB_FILE)

    def menu():
        while True:
            action = inquirer.prompt([
                inquirer.List(
                    "action",
                    message="Select an action",
                    choices=[
                        "Create person", "Find by name", "Find by city",
                        "Generate emails", "Generate usernames",
                        "Group by state", "Filter by age",
                        "Filter by registration date", "Exit"
                    ]
                )
            ])["action"]

            if action == "Create person":
                person = {}
                person["user"] = {
                    "name": {
                        "first": input("First name: "),
                        "last": input("Last name: "),
                        "title": input("Title: ")
                    },
                    "email": input("Email: "),
                    "SSN": input("SSN (format XXX-XX-XXXX): "),
                    "phone": input("Phone (format (XXX)-XXX-XXXX): "),
                    "username": input("Username: "),
                    "dob": int(datetime.strptime(input("DOB (YYYY-MM-DD): "), "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()),
                    "registered": int(datetime.now(tz=timezone.utc).timestamp()),
                    "location": {
                        "city": input("City: "),
                        "state": input("State: ")
                    }
                }
                db.create_person(person)
                print("Person created.\n")

            elif action == "Find by name":
                first = input("First name (optional): ")
                last = input("Last name (optional): ")
                print("Results:", db.find_by_name(first_name=first or None, last_name=last or None), "\n")

            elif action == "Find by city":
                city = input("City: ")
                print("Results:", db.find_by_city(city), "\n")

            elif action == "Generate emails":
                print("Emails:", db.generate_emails(), "\n")

            elif action == "Generate usernames":
                print("Usernames:", db.generate_usernames(), "\n")

            elif action == "Group by state":
                grouped = db.group_by_state()
                for state, users in grouped.items():
                    print(f"{state.title()}: {len(users)} users")
                print()

            elif action == "Filter by age":
                min_age = input("Min age (optional): ")
                max_age = input("Max age (optional): ")
                results = db.filter_by_age(
                    min_age=int(min_age) if min_age else None,
                    max_age=int(max_age) if max_age else None
                )
                print("Results:", results, "\n")

            elif action == "Filter by registration date":
                since = input("Registered after (YYYY-MM-DD, optional): ")
                until = input("Registered before (YYYY-MM-DD, optional): ")
                since_dt = datetime.strptime(since, "%Y-%m-%d").replace(tzinfo=timezone.utc) if since else None
                until_dt = datetime.strptime(until, "%Y-%m-%d").replace(tzinfo=timezone.utc) if until else None
                print("Results:", db.filter_by_registration_date(since=since_dt, until=until_dt), "\n")

            elif action == "Exit":
                break

    menu()

if __name__ == "__main__":
    main()