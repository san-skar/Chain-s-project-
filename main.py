import json
import copy
from tabulate import tabulate

def print_library_data(library_data, students_data):
    library_data_list = []
    library_data_copy = copy.deepcopy(library_data)
    for book in library_data_copy:
        library_book_info = [book]
        for info in library_data_copy[book]:
            if info == "book_issued_to":
                book_issued_to = []
                for id in library_data_copy[book][info]:
                    book_issued_to.append(students_data[id]["name"])
                library_data_copy[book][info] = book_issued_to
            library_book_info.append(library_data_copy[book][info])
        library_data_list.append(library_book_info)
    print(tabulate(library_data_list, headers = ["Book", "Available Count", "Book issued to", "Total Count"], tablefmt="grid"))

def print_student_database(students_data):
    students_data_list = []
    for id in students_data:
        students_data_list.append([id, students_data[id]["name"]])
    print(tabulate(students_data_list, headers = ["id", "name"], tablefmt="grid"))

def add_new_book_to_the_library(library_data):
    book_name = input("Enter book name you want to add: ")
    if book_name in library_data:
        print("Book is already present in library!! You may want to edit it")
        return
    total_count = input("Enter total count of book: ")
    library_data[book_name] = {
        "available_count": str(total_count),
        "book_issued_to": [],
        "total_count": str(total_count),
      }
    with open("library.json", "w") as library:
        library.write(json.dumps(library_data, indent=4))
    print("Book successfully added to library data.")

def issue_book_to_a_student(library_data, students_data):
    book_name = input("Enter book name you want to give to a student: ")
    if book_name not in library_data:
        print("This book is not present in our library database")
        return
    if int(library_data[book_name]["available_count"]) <= 0:
        print(f"No {book_name} book left. All are given to differnt students.")
        return
    student_id = input("Enter Student id: ")
    if student_id not in students_data:
        print("This student id is not present in our database. Please add them in database first.")
        return
    library_data[book_name]["available_count"] = int(library_data[book_name]["available_count"]) - 1
    list_of_students_book_issued_to = library_data[book_name]["book_issued_to"]
    if student_id in list_of_students_book_issued_to:
        print("This book is already present with the student. Please ask him/her to return the book first")
        return
    list_of_students_book_issued_to.append(student_id)
    library_data[book_name]["book_issued_to"] = list_of_students_book_issued_to
    with open("library.json", "w") as library:
      library.write(json.dumps(library_data, indent=4))
    print(f"{book_name} book successfully issued to student {student_id}")

def delete_book_from_the_library(library_data):
    book_name = input("Enter book name you want to delete: ")
    if book_name not in library_data:
        print("This book is already not present in library")
        return
    del library_data[book_name]
    with open("library.json", "w") as library:
      library.write(json.dumps(library_data, indent=4))
    print(f'{book_name} book is successfully deleted from the library database')

def add_new_student_to_database(students_data):
    student_id = input("Enter student id you want to add: ")
    if student_id in students_data:
        print("This student id is already present in our database")
        return
    student_name = input("Enter student name: ")
    students_data[student_id] = {"name": student_name}
    with open("students.json", "w") as students:
      students.write(json.dumps(students_data, indent=4))
    print("Student successfully added to student database")

def delete_student_from_the_database(students_data):
    student_id = input("Enter student id you want to delete: ")
    if student_id not in students_data:
        print("This student id is already not present in our database")
        return
    del students_data[student_id]
    with open("students.json", "w") as students:
      students.write(json.dumps(students_data, indent=4))
    print("Student successfully deleted from student database")

def return_borrowed_book(library_data):
    book_name = input("Enter book name student wants to return: ")
    if book_name not in library_data:
        print("This book is not present in our database")
        return
    student_id = input("Enter Student id: ")
    if student_id not in library_data[book_name]["book_issued_to"]:
        print("This student has never borrow book from our library according to our database")
        return
    library_data[book_name]["available_count"] = str(int(library_data[book_name]["available_count"]) + 1)
    new_list_of_students_book_issued_to = []
    for id in library_data[book_name]["book_issued_to"]:
        if id != student_id:
            new_list_of_students_book_issued_to.append(id)
    library_data[book_name]["book_issued_to"] = new_list_of_students_book_issued_to
    with open("library.json", "w") as library:
      library.write(json.dumps(library_data, indent=4))
    print(f"{book_name} book successfully returned by the student {student_id}")

def main():
    print(" *****  WELCOME TO LIBRARY MANAGEMENT SYSTEM!!  ***** ")
    # get library data
    with open("library.json") as library:
        library_data = library.read()
    library_data = json.loads(library_data)

    # get students data
    with open("students.json") as students:
        students_data = students.read()
    students_data = json.loads(students_data)

    while True:
        # Get input from the user.
        print()
        print()
        print("press 1 to show library data")
        print("press 2 to show students data")
        print("press 3 to add new book to the library")
        print("press 4 to issue book to the student")
        print("press 5 to delete book from the library")
        print("press 6 to add new student to student database")
        print("press 7 to delete student from student database")
        print("press 8 if student wants to return a book")
        print("press q to exit")
        user_input = input("Enter your choice: ")
        print()
        print()

        # Check if the user wants to quit.
        if user_input == 'q':
            break
        elif user_input == '1':
            print_library_data(library_data, students_data)
        elif user_input == '2':
            print_student_database(students_data)
        elif user_input == '3':
            add_new_book_to_the_library(library_data)
        elif user_input == '4':
            issue_book_to_a_student(library_data, students_data)
        elif user_input == '5':
            delete_book_from_the_library(library_data)
        elif user_input == '6':
            add_new_student_to_database(students_data)
        elif user_input == '7':
            delete_student_from_the_database(students_data)
        elif user_input == '8':
            return_borrowed_book(library_data)

if __name__ == "__main__":
    main()
