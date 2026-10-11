
import json
import os

DATA_FILE = "students.json"

SUBJECTS = [
    "DBMS",
    "DMS",
    "OS",
    "OOPS",
    "BEFA"
]

PASS_MARK = 35


# Load student records from the JSON file
def load_students():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read student data.")
        return []


# Save student records to the JSON file
def save_students(students):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(students, file, indent=4)
    except OSError:
        print("Error: Unable to save student records.")


# Read and validate integer input
def get_integer(prompt, minimum, maximum):
    while True:
        try:
            value = int(input(prompt))

            if minimum <= value <= maximum:
                return value

            print(f"Enter a value between {minimum} and {maximum}.")

        except ValueError:
            print("Invalid input. Enter a whole number.")


# Calculate total, percentage, grade, and result
def calculate_result(marks):
    total = sum(marks.values())
    percentage = total / len(SUBJECTS)

    passed = all(marks[s] >= PASS_MARK for s in SUBJECTS)

    if not passed:
        grade = "F"
        result = "FAIL"
    else:
        result = "PASS"

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        else:
            grade = "E"

    return total, percentage, grade, result


# Display one student's result
def display_student(student):
    total, percentage, grade, result = calculate_result(
        student["marks"]
    )

    print("\n" + "=" * 45)
    print("         STUDENT RESULT")
    print("=" * 45)
    print("Roll Number :", student["roll"])
    print("Name        :", student["name"])

    for subject in SUBJECTS:
        print(f"{subject:<20}: {student['marks'][subject]}")

    print("-" * 45)
    print(f"Total       : {total}/{len(SUBJECTS) * 100}")
    print(f"Percentage  : {percentage:.2f}%")
    print("Grade       :", grade)
    print("Result      :", result)
    print("=" * 45)


# Add a new student
def add_student(students):
    print("\n--- Add Student ---")

    roll = input("Enter roll number: ").strip()

    if not roll:
        print("Roll number cannot be empty.")
        return

    if any(s["roll"].lower() == roll.lower() for s in students):
        print("A student with this roll number already exists.")
        return

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    marks = {}

    for subject in SUBJECTS:
        marks[subject] = get_integer(
            f"Enter {subject} marks (0-100): ", 0, 100
        )

    student = {
        "roll": roll,
        "name": name,
        "marks": marks
    }

    students.append(student)
    save_students(students)

    print("Student added successfully!")
    display_student(student)


# Display all student records
def view_students(students):
    if not students:
        print("No student records found.")
        return

    print("\n--- All Student Records ---")
    print(
        f"{'Roll':<12}{'Name':<20}"
        f"{'Total':<10}{'Percent':<12}{'Grade':<8}{'Result'}"
    )
    print("-" * 75)

    for student in students:
        total, percentage, grade, result = calculate_result(
            student["marks"]
        )

        print(
            f"{student['roll']:<12}"
            f"{student['name'][:19]:<20}"
            f"{total:<10}"
            f"{percentage:.2f}%{'':<5}"
            f"{grade:<8}{result}"
        )


# Search for a student
def search_student(students):
    roll = input("Enter roll number to search: ").strip()

    for student in students:
        if student["roll"].lower() == roll.lower():
            display_student(student)
            return

    print("Student not found.")


# Update an existing student's marks
def update_marks(students):
    roll = input("Enter roll number to update: ").strip()

    for student in students:
        if student["roll"].lower() == roll.lower():
            print("Enter the updated marks:")

            for subject in SUBJECTS:
                student["marks"][subject] = get_integer(
                    f"{subject} (0-100): ", 0, 100
                )

            save_students(students)
            print("Marks updated successfully!")
            display_student(student)
            return

    print("Student not found.")


# Delete a student record
def delete_student(students):
    roll = input("Enter roll number to delete: ").strip()

    for student in students:
        if student["roll"].lower() == roll.lower():
            confirm = input(
                f"Delete {student['name']}'s record? (yes/no): "
            ).strip().lower()

            if confirm == "yes":
                students.remove(student)
                save_students(students)
                print("Student record deleted.")
            else:
                print("Deletion cancelled.")

            return

    print("Student not found.")


# Main menu
def main():
    students = load_students()

    while True:
        print("\n===== STUDENT MARKS MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Marks")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_marks(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
