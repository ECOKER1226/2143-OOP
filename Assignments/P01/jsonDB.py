import json
from rich import print

class JsonDB:
    """
    Base class for a simple JSON "database."

    Attributes:
        filepath (str): Path to the JSON file on disk.
        data (any): The loaded JSON data (e.g., list, dict).
    """
    def __init__(self, filepath):
        """Initialize the DB with a path to the JSON file."""
        self.filepath = filepath
        self.data = None
        self._load_data()

    def _load_data(self):
        """Load JSON data from the file into self.data."""
        try:
            with open(self.filepath, 'r') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    def _save_data(self):
        """Save self.data back to the JSON file."""
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def create(self, record):
        """Insert a new record into self.data."""
        if not isinstance(self.data, list):
            self.data = []
        self.data.append(record)
        self._save_data()
        return record

    def read(self, **filters):
        """Search the database using provided filters."""
        if not isinstance(self.data, list):
            return []

        results = [record for record in self.data if all(record.get(k) == v for k, v in filters.items())]
        return results if results else None

    def update(self, record_id, updated_data):
        """Update an existing record by some identifier."""
        if not isinstance(self.data, list):
            return None
        
        for record in self.data:
            if record.get("id") == record_id:
                record.update(updated_data)
                self._save_data()
                return record
        return None

    def delete(self, record_id):
        """Remove a record by its identifier."""
        if not isinstance(self.data, list):
            return None
        
        for record in self.data:
            if record.get("id") == record_id:
                self.data.remove(record)
                self._save_data()
                return record
        return None

if __name__ == "main":
    db = JsonDB("random_people.10000.json")

    print("Initial Data:", db.read())

    db.create({"id": 1, "name": "Alice", "email": "alice@example.com"})
    db.create({"id": 2, "name": "Bob", "email": "bob@example.com"})
    print("After Insertions:", db.read())

    db.update(2, {"email": "updated_bob@example.com"})
    print("After Update:", db.read())

    db.delete(1)
    print("After Deletion:", db.read())