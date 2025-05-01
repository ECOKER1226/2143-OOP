import json
from rich import print
from jsonDB import JsonDB

class PeopleDB(JsonDB):
    """
    Specialized DB class for handling 'user' records in JSON format.
    """

    def __init__(self, filepath):
        super().__init__(filepath)

    def find_by_name(self, first_name=None, last_name=None):
        """Search for a person by first and/or last name."""
        filters = {}
        if first_name:
            filters["user.name.first"] = first_name
        if last_name:
            filters["user.name.last"] = last_name
        return self.read(**filters)

    def find_by_phone(self, phone):
        """Search for a person by phone number."""
        return self.read(user__phone=phone)

    def find_by_cell(self, cell):
        """Search for a person by cell number."""
        return self.read(user__cell=cell)

    def find_by_ssn(self, ssn):
        """Search for a person by SSN."""
        return self.read(user__SSN=ssn)

    def find_by_location(self, state=None, street=None, city=None, zip_code=None):
        """Search by state, street, city, or zip."""
        filters = {}
        if state:
            filters["user.location.state"] = state
        if street:
            filters["user.location.street"] = street
        if city:
            filters["user.location.city"] = city
        if zip_code:
            filters["user.location.zip"] = zip_code
        return self.read(**filters)

    def find_by_username(self, username):
        """Search for a person by username."""
        return self.read(user__username=username)

    def find_by_email(self, email):
        """Search for a person by email."""
        return self.read(user__email=email)

    def find_by_dob(self, min_age=None, max_age=None):
        """Search for people by age range."""
        from datetime import datetime

        current_timestamp = int(datetime.now().timestamp())
        matching_records = []

        for record in self.data:
            dob = record["user"]["dob"]
            age = (current_timestamp - dob) // (365 * 24 * 3600)
            
            if (min_age is None or age >= min_age) and (max_age is None or age <= max_age):
                matching_records.append(record)

        return matching_records

    def generate_username(self, first_name, last_name):
        """Generate a username based on first/last name."""
        return f"{first_name.lower()}{last_name.lower()}_{abs(hash(first_name+last_name)) % 10000}"

    def generate_secure_password(self, length=12):
        """Generate a random, secure password."""
        import secrets
        import string

        characters = string.ascii_letters + string.digits + string.punctuation
        password = []
        for _ in range(length):
            password.append(secrets.choice(characters))
        return ''.join(password)

    def verify_email_format(self, email):
        """Verify if an email is valid."""
        import re
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        match = re.match(email_pattern, email)
        return match is not None
    
    def create_person(self, person_data):
        """
        Validate and insert a new person record.
        Ensures required fields exist before calling create().
        """
        required_fields = ["user.name.first", "user.name.last", "user.email"]
        for field in required_fields:
            if not any(field in key for key in person_data.keys()):
                raise ValueError(f"Missing required field: {field}")
        return self.create(person_data)

if __name__ == "main":
    db = PeopleDB("random_people.10000.json")

    print("Find by first name:", db.find_by_name(first_name="Katherine"))
    print("Find by last name:", db.find_by_name(last_name="Smith"))
    print("Find by email:", db.find_by_email("teresa.smith@example.com"))
    print("Find by phone:", db.find_by_phone("(654)-537-3357"))
    print("Find by state:", db.find_by_location(state="Texas"))