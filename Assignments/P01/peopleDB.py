class PeopleDB(JsonDB):
    """
    Specialized DB class for handling 'user' records in JSON format.
    """
    def __init__(self, filepath):
        super().__init__(filepath)

    def find_by_name(self, first_name=None, last_name=None):
        """
        Convenience method to query people by first/last name.
        """
        # Possibly call self.read() or do custom logic here.
        pass

    def create_person(self, person_data):
        """
        A more domain-specific create method.
        Might validate the user structure, e.g., checking phone, SSN formats, etc.
        Then call self.create(...) from the base class.
        """
        pass

    # Optionally override or extend the base CRUD methods if needed
    # e.g., custom validation, special indexing, etc.