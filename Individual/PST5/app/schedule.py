import json
import logging
import datetime
import csv
from app.student import StudentUser
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course
from app.admin_utils import init_logger, backup_data

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
                # TODO: Load students, teachers, and courses as before.
                self.students = [StudentUser(**s) for s in data.get("students", [])]
                self.teachers = [TeacherUser(**t) for t in data.get("teachers", [])]
                self.courses = [Course(**c) for c in data.get("courses", [])]

                # TODO: Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
                self.attendance_log = data.get("attendance", [])
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


    def register_new_student(self, name, instrument):
        """Registers a new student and assigns them a unique ID."""
        next_student_id = len(self.students) + 1
        new_student = StudentUser(name=name, id=next_student_id, instrument=instrument)
        self.students.append(new_student)
        self._save_data()
        logging.info(f"New student registered: {new_student.name} (ID: {new_student.id})")
        return new_student
    
    def update_student(self, student_id, name=None, instrument=None):
        """Updates an existing student's details."""
        student = self.find_student_by_id(student_id)
        if not student:
            print("Error: Student not found.")
            return None

        # Update student attributes if new values are provided
        if name:
            student.name = name
        if instrument:
            student.instrument = instrument

        self._save_data()
        logging.info(f"Student updated: {student.name} (ID: {student.id})")
        return student
    
    def unregister_student(self, student_id):
        """Unregisters a student by their ID"""
        student = self.find_student_by_id(student_id)
        if student:
            self.students.remove(student)
            self._save_data()
            logging.info(f"Student unregistered: {student.name} (ID: {student.id})")
            return True
        return False
    
    def register_new_teacher(self, name, speciality):   
        """Registers a new teacher and assigns them a unique ID."""
        next_teacher_id = len(self.teachers) + 1
        new_teacher = TeacherUser(name=name, id=next_teacher_id, speciality=speciality)
        self.teachers.append(new_teacher)
        self._save_data()
        logging.info(f"New teacher registered: {new_teacher.name} (ID: {new_teacher.id})")
        return new_teacher
    
    def update_teacher(self, teacher_id, name=None, speciality=None):
        """Updates an existing teacher's details."""
        teacher = self.find_teacher_by_id(teacher_id)
        if not teacher:
            print("Error: Teacher not found.")
            return None

        # Update teacher attributes if new values are provided
        if name:
            teacher.name = name
        if speciality:
            teacher.speciality = speciality

        self._save_data()
        logging.info(f"Teacher updated: {teacher.name} (ID: {teacher.id})")
        return teacher
    
    def unregister_teacher(self, teacher_id):
        """Unregisters a teacher by their ID"""
        teacher = self.find_teacher_by_id(teacher_id)
        if teacher:
            self.teachers.remove(teacher)
            self._save_data()
            logging.info(f"Teacher unregistered: {teacher.name} (ID: {teacher.id})")
            return True
        return False
    
    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": student_id, "course_id": course_id, "timestamp": timestamp}
        
        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # This will now correctly save the attendance log.
        logging.info(f"Student {student.name} checked into course {course.name} at {timestamp}")
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True
    
    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course
        return None
    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None
    
    def find_teacher_by_id(self, teacher_id):
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def get_daily_roster(self, day):
        roster = []
        for course in self.courses:
            if course.day.lower() == day.lower():
                teacher = self.find_teacher_by_id(course.teacher_id)
                roster.append({
                    "course_name": course.name,
                    "teacher_name": teacher.name if teacher else "Unknown",
                    "enrolled_students": [self.find_student_by_id(sid) for sid in course.enrolled_student_ids]
                })
        return roster
    
    def get_available_days(self):
        """Returns a sorted list of unique days with scheduled courses."""
        return sorted({course.day for course in self.courses})
    
    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Switches a student's enrolled course"""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student or not from_course or not to_course:
            print("Error: Invalid student or course ID")
            return False
        if from_course_id not in student.enrolled_courses:
            print(f"Error: Student {student.name} is not enrolled in {from_course.name}")
            return False
        if to_course_id in student.enrolled_courses:
            print(f"Error: Student {student.name} is already enrolled in {to_course.name}")
            return False

        # Remove student from the old course
        from_course.remove_student(student_id)
        # Add student to the new course
        to_course.add_student(student_id)
        self._save_data()
        logging.info(f"Student {student.name} switched from {from_course.name} to {to_course.name}")
        print(f"Successfully switched {student.name} from {from_course.name} to {to_course.name}")
        return True

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
        logging.info(f"Payment recorded: {payment_record}")
        print(f"Payment of {amount} for student {student_id} recorded.")

    def get_payment_history(self, student_id):
        """Returns a list of all payments for a given student."""
        # TODO: Use a list comprehension to filter self.finance_log
        finance_log = getattr(self, 'finance_log', [])
        if not finance_log:
            print("No finance log found.")
            return []
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