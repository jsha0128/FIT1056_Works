import json
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.next_lesson_id = 1 
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # The logic here remains the same, but the source of the Course class has changed.
                # TODO: For each dictionary in data['students'], create a StudentUser object and append to self.students.
                for student_dict in data.get('students', []):
                    student = StudentUser(student_dict['user_id'], student_dict['name'])
                    student.enrolled_course_ids = student_dict.get('enrolled_course_ids', [])
                    self.students.append(student)
                # TODO: Do the same for teachers (creating TeacherUser objects).
                for teacher_dict in data.get('teachers', []):
                    teacher = TeacherUser(teacher_dict['user_id'], teacher_dict['name'])
                    self.teachers.append(teacher)
                # TODO: Do the same for courses (creating Course objects).
                for course_dict in data.get('courses', []):
                    course = Course(course_dict['course_id'], course_dict['title'], course_dict['teacher_id'])
                    self.courses.append(course)
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # The logic here remains the same.
        # TODO: Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [vars(s) for s in self.students],
            "teachers": [vars(t) for t in self.teachers],
            "courses": [vars(c) for c in self.courses]
        }
        # Convert self.students, self.teachers, and self.courses into lists of dictionaries.
        # Write the result to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        pass

import csv
import datetime

def record_payment(self, student_id, amount, method):
    """Adds a payment record to the finance log."""
    # TODO: Find the student to ensure they exist.
    # Create a payment dictionary with student_id, amount, method, and a timestamp.
    payment_record = {
        "student_id": student_id,
        "amount": amount,
        "method": method,
        "timestamp": datetime.datetime.now().isoformat()
    }
    # TODO: Append the record to self.finance_log and save the data.
    self.finance_log.append(payment_record)
    self._save_data()
    print(f"Payment of {amount} for student {student_id} recorded.")

def get_payment_history(self, student_id):
    """Returns a list of all payments for a given student."""
    # TODO: Use a list comprehension to filter self.finance_log
    # and return only the records that match the student_id.
    return [p for p in self.finance_log if p['student_id'] == student_id]

def export_report(self, kind, out_path):
    """Exports a log to a CSV file."""
    print(f"Exporting {kind} report to {out_path}...")
    # TODO: Use an if/elif block to select the correct data list based on 'kind'.
    if kind == "finance":
        data_to_export = self.finance_log
        headers = ["student_id", "amount", "method", "timestamp"]
    elif kind == "attendance":
        data_to_export = self.attendance_log # Assuming this exists from PST2
        headers = ["student_id", "course_id", "timestamp"]
    else:
        print("Error: Unknown report type.")
        return

    # TODO: Use Python's 'csv' module to write the data.
    # Open the file, create a csv.DictWriter, write the header, then write all the rows.
    # with open(out_path, 'w', newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames=headers)
    #     writer.writeheader()
    #     writer.writerows(data_to_export)
    with open(out_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_to_export)
    print("Export complete.")