import json
from rich import print
from jsonDB import JsonDB
from peopleDB import PeopleDB

if __name__ == "main":
    db = PeopleDB("random_people.10000.json")

    print("Find by first name:", db.find_by_name(first_name="Katherine"))
    print("Find by last name:", db.find_by_name(last_name="Smith"))
    print("Find by email:", db.find_by_email("teresa.smith@example.com"))
    print("Find by phone:", db.find_by_phone("(654)-537-3357"))
    print("Find by state:", db.find_by_location(state="Texas"))