# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    # Notice: This code does not need to change. It doesn't care where the Course class lives.
    # It only talks to the manager.
    # TODO: Call a method on the manager to get the day's lessons and print them.
    roster = manager.get_daily_roster(day)
    if not roster:
        print("No lessons scheduled for this day.")
        return
    print(f"{'Course':<30} {'Teacher':<20} {'Time':<10} {'Room':<10}")
    print("-" * 70)
    for lesson in roster:
        print(f"{lesson['course_name']:<30} {lesson['teacher_name']:<20} {lesson['start_time']:<10} {lesson['room']:<10}")

def switch_course(manager, student_id, from_course_id, to_course_id):
    # TODO: Implement the logic to switch a student by calling methods on the manager.
   manager.switch_student_course(student_id, from_course_id, to_course_id)

def check_in_student(manager, student_id, course_id):
    manager.check_in(student_id, course_id)

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.
    
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        # TODO: Create a menu for the new PST3 functions.
        print("1. View Daily Roster")
        print("2. Check in a Student")
        print("3. Switch Student Course")
        print("Q. Quit")
        # Get user input and call the appropriate view function, passing 'manager' to it.
        choice = input("Enter choice: ").strip()
        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice == '2':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = int(input("Enter course ID: "))
                check_in_student(manager, student_id, course_id)
            except ValueError:
                print("Invalid input. Please enter a number")
        elif choice == '3':
            try:
                student_id = int(input("Enter student ID: "))
                from_course_id = int(input("Enter current course ID: "))
                to_course_id = int(input("Enter new course ID: "))
                switch_course(manager, student_id, from_course_id, to_course_id)
            except ValueError:
                print("Invalid input. Please enter a number")
        elif choice.lower() == 'q':
            print("Exiting Application")
            break
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()