import json
import os
import re
from rich import print
from jsonDB import JsonDB
from datetime import datetime, timezone

class PeopleDB(JsonDB):
    """
    Specialized DB class for handling 'user' records in JSON format.
    Each record is a dictionary with a single key 'user' pointing to user info.
    """

    def __init__(self, filepath):
        super().__init__(filepath)

    def find_by_name(self, first_name=None, last_name=None):
        """
        Search for users by nested first/last name in record['user']['name'].
        Case-insensitive. Matches either or both.
        """
        results = []
        for record in self.data:
            user = record.get("user", {})
            name = user.get("name", {})
            match = True
            if first_name and name.get("first", "").lower() != first_name.lower():
                match = False
            if last_name and name.get("last", "").lower() != last_name.lower():
                match = False
            if match:
                results.append(record)
        return results

    def create_person(self, person_data):
        """
        Validate the nested user record and create it.
        """
        if "user" not in person_data or not isinstance(person_data["user"], dict):
            raise ValueError("Record must contain a 'user' key with a dictionary value.")

        user = person_data["user"]
        required_fields = ["email", "name", "SSN", "phone"]
        for field in required_fields:
            if field not in user:
                raise ValueError(f"Missing required user field: {field}")

        if not self._validate_ssn(user["SSN"]):
            raise ValueError("Invalid SSN format. Expected format: XXX-XX-XXXX")

        if not self._validate_phone(user["phone"]):
            raise ValueError("Invalid phone format. Expected format: (XXX)-XXX-XXXX")

        return self.create(person_data)

    def _validate_ssn(self, ssn):
        """
        Validate SSN format: XXX-XX-XXXX
        """
        return bool(re.fullmatch(r"\d{3}-\d{2}-\d{4}", ssn))

    def _validate_phone(self, phone):
        """
        Validate phone format: (XXX)-XXX-XXXX
        """
        return bool(re.fullmatch(r"\(\d{3}\)-\d{3}-\d{4}", phone))

    def find_by_city(self, city_name):
        """
        Search for users by city.
        """
        results = []
        for record in self.data:
            city = record.get("user", {}).get("location", {}).get("city", "").lower()
            if city == city_name.lower():
                results.append(record)
        return results

    def generate_emails(self):
        """
        Return a list of all user emails.
        """
        return [record["user"]["email"] for record in self.data if "email" in record["user"]]
    
    def filter_by_registration_date(self, since=None, until=None):
        """
        Filter users who registered within a given date range.
        `since` and `until` should be datetime objects.
        Returns a list of matching records.
        """
        results = []
        for record in self.data:
            ts = record.get("user", {}).get("registered")
            if ts is None:
                continue
            reg_date = datetime.fromtimestamp(ts, tz=timezone.utc)
            if (since and reg_date < since) or (until and reg_date > until):
                continue
            results.append(record)
            return results

    def filter_by_age(self, min_age=None, max_age=None):
        """
        Filter users by age range.
        Age is calculated based on current UTC date and user's dob.
        Returns a list of matching records.
        """
        now = datetime.now(tz=timezone.utc)
        results = []
        for record in self.data:
            dob_ts = record.get("user", {}).get("dob")
            if dob_ts is None:
                continue
            dob = datetime.fromtimestamp(dob_ts, tz=timezone.utc)
            age = (now - dob).days // 365
            if (min_age is not None and age < min_age) or (max_age is not None and age > max_age):
                continue
            results.append(record)
        return results