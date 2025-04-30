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

if __name__ == "__main__":
    with open("NESGames.json") as f:
        jdata = json.load(f)

    # print the length of the list
    print(len(jdata))

    # print the tenth game in the list
    print(jdata[10])

    # add id to each game
    for i,NESGames in enumerate(jdata):
        # print(NESGames.keys())
        NESGames['id'] = i
        print(NESGames)