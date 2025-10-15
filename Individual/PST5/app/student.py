from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, id, name, instrument=None, enrolled_course_ids=None):
        super().__init__(id, name)
        self.instrument = instrument 
        self.enrolled_course_ids = enrolled_course_ids if enrolled_course_ids is not None else []