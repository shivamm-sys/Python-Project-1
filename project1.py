import csv
import matplotlib.pyplot as plt

# Here we are making student class

class Student:
    def __init__(self, student_id, name, marks=None):
        self.id = student_id
        self.name = name
        self.marks = marks or {}

    def calculate_percentage(self):
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def calculate_grade(self):
        pct = self.calculate_percentage()
        if pct >= 90:
            return "A"
        elif pct >= 80:
            return "B"
        elif pct >= 70:
            return "C"
        elif pct >= 60:
            return "D"
        else:
            return "F"


# Here we make  Utility Functions


def calculate_gpa(student):
    if not student.marks:
        return 0
    total = 0
    for score in student.marks.values():
        if score >= 90:
            total += 4.0
        elif score >= 80:
            total += 3.0
        elif score >= 70:
            total += 2.0
        elif score >= 60:
            total += 1.0
        else:
            total += 0.0
    return total / len(student.marks)

def get_topper(students):
    return max(students.values(), key=lambda s: s.calculate_percentage(), default=None)

def plot_student_performance(student):
    if not student.marks:
        print("No marks to display.")
        return

    subjects = list(student.marks.keys())
    scores = list(student.marks.values())

    plt.figure(figsize=(8, 5))
    plt.bar(subjects, scores, color='skyblue')
    plt.title(f"{student.name}'s Performance")
    plt.xlabel("Subjects")
    plt.ylabel("Marks")
    plt.ylim(0, 100)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()


# Main Program Functions


students = {}

def add_student():
    sid = input("Enter student ID: ")
    name = input("Enter student name: ")
    if sid in students:
        print("Student ID already exists.")
        return
    students[sid] = Student(sid, name)
    print("Student added successfully.")

def update_marks():
    sid = input("Enter student ID: ")
    if sid not in students:
        print("Student not found.")
        return
    subject = input("Enter subject name: ")
    try:
        marks = float(input("Enter marks (0-100): "))
        if 0 <= marks <= 100:
            students[sid].marks[subject] = marks
            print("Marks updated.")
        else:
            print("Invalid marks range.")
    except ValueError:
        print("Please enter a valid number.")

def delete_student():
    sid = input("Enter student ID to delete: ")
    if sid in students:
        del students[sid]
        print("Student deleted.")
    else:
        print("Student not found.")

def view_summary():
    if not students:
        print("No student data available.")
        return
    for sid, student in students.items():
        print(f"\nID: {sid}")
        print(f"Name: {student.name}")
        print(f"Marks: {student.marks}")
        print(f"Percentage: {student.calculate_percentage():.2f}%")
        print(f"Grade: {student.calculate_grade()}")
        print(f"GPA: {calculate_gpa(student):.2f}")

def find_topper():
    topper = get_topper(students)
    if topper:
        print(f"\nTopper: {topper.name}")
        print(f"Percentage: {topper.calculate_percentage():.2f}%")
        print(f"Grade: {topper.calculate_grade()}")
    else:
        print("No students available.")

def export_csv():
    with open("students.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Marks"])
        for student in students.values():
            writer.writerow([student.id, student.name, student.marks])
    print("Data exported to students.csv")

def import_csv():
    try:
        with open("students.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row["ID"]
                name = row["Name"]
                marks = eval(row["Marks"])  # Use safe parsing in real apps
                students[sid] = Student(sid, name, marks)
        print("Data imported from students.csv")
    except FileNotFoundError:
        print("No existing CSV found.")

def visualize_student():
    sid = input("Enter student ID: ")
    if sid in students:
        plot_student_performance(students[sid])
    else:
        print("Student not found.")

def menu():
    print("""
===== Student Information System =====
1. Add Student
2. Update Marks
3. Delete Student
4. View Summary
5. Find Class Topper
6. Export to CSV
7. Import from CSV
8. Visualize Performance
0. Exit
""")

def main():
    import_csv()
    while True:
        menu()
        choice = input("Enter choice: ")
        if choice == '1':
            add_student()
        elif choice == '2':
            update_marks()
        elif choice == '3':
            delete_student()
        elif choice == '4':
            view_summary()
        elif choice == '5':
            find_topper()
        elif choice == '6':
            export_csv()
        elif choice == '7':
            import_csv()
        elif choice == '8':
            visualize_student()
        elif choice == '0':
            export_csv()
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()