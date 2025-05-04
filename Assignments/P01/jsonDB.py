import json
import os
from rich import print

class JsonDB:
    """
    Base class for a simple JSON "database."

    Attributes:
        filepath (str): Path to the JSON file on disk.
        data (list): The loaded JSON data (expected to be a list of dicts).
    """

    def __init__(self, filepath):
        """
        Initialize the DB with a path to the JSON file.
        """
        self.filepath = filepath
        self.data = []
        self._load_data()

    def _load_data(self):
        """
        Internal helper to load JSON data from the file into self.data.
        Handle exceptions and set self.data appropriately if file is missing/corrupted.
        """
        if not os.path.exists(self.filepath):
            self.data = []
            return
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                if not isinstance(self.data, list):
                    raise ValueError("JSON data must be a list of records.")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Could not load data: {e}")
            self.data = []

    def _save_data(self):
        """
        Internal helper to save self.data back to the JSON file.
        """
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def _generate_id(self):
        """
        Generate a new unique integer ID for a record.
        """
        if not self.data:
            return 1
        existing_ids = [record.get("id", 0) for record in self.data if isinstance(record, dict)]
        return max(existing_ids, default=0) + 1

    def create(self, record):
        """
        Insert a new record into self.data.
        """
        if not isinstance(record, dict):
            raise ValueError("Record must be a dictionary.")
        if "id" not in record:
            record["id"] = self._generate_id()
        self.data.append(record)
        self._save_data()
        return record

    def read(self, **filters):
        """
        Read/search the database.
        Return a list of matching records.
        """
        results = []
        for record in self.data:
            if all(record.get(k) == v for k, v in filters.items()):
                results.append(record)
        return results

    def update(self, record_id, updated_data):
        """
        Update an existing record by 'id'.
        """
        for record in self.data:
            if record.get("id") == record_id:
                record.update(updated_data)
                self._save_data()
                return record
        raise ValueError(f"Record with id={record_id} not found.")

    def delete(self, record_id):
        """
        Remove a record by its 'id'.
        """
        for i, record in enumerate(self.data):
            if record.get("id") == record_id:
                removed = self.data.pop(i)
                self._save_data()
                return removed
        raise ValueError(f"Record with id={record_id} not found.")