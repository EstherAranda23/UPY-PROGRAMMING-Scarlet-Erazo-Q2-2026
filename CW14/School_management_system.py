# Classwork 14 - Error Handling: School Management System

#PROCESS: Required Data Structures

users = {
    'jperez':   {'password': '1234', 'rol': 'student',     'name': 'Juan Pérez'},
    'dromo':    {'password': '1234', 'rol': 'student',     'name': 'Daniela Romo'},
    'mjuarez':  {'password': '1234', 'rol': 'student',     'name': 'Mauricio Juárez'},
    'mlopez':   {'password': '1234', 'rol': 'student',     'name': 'María López'},
    'euc':      {'password': '1234', 'rol': 'student',     'name': 'Ernesto Uc'},
    'cbalam':   {'password': '1234', 'rol': 'student',     'name': 'Carlos Balam'},
    'jpedrozo': {'password': '1234', 'rol': 'professor',   'name': 'Jorge Pedrozo'},
    'dgamboa':  {'password': '1234', 'rol': 'coordinator', 'name': 'Didier Gamboa'},
}

subjects = (
    "Discrete Mathematics",
    "Programming",
    "English II",
    "Differential Calculus",
    "Probability and Statistics",
    "Computer and Server Architecture",
    "Socio-Emotional Skills and Conflict Management"
)

notes = {
    'jperez': {
        'Discrete Mathematics': 8.5, 'Programming': 9.2, 'English II': 9.0,
        'Differential Calculus': 7.8, 'Probability and Statistics': 8.3,
        'Computer and Server Architecture': 6.8,
        'Socio-Emotional Skills and Conflict Management': 9.5
    },
    'dromo': {
        'Discrete Mathematics': 9.0, 'Programming': 6.7, 'English II': 9.4,
        'Differential Calculus': 6.2, 'Probability and Statistics': 9.1,
        'Computer and Server Architecture': 6.5,
        'Socio-Emotional Skills and Conflict Management': 9.8
    },
    'mjuarez': {
        'Discrete Mathematics': 7.5, 'Programming': 8.0, 'English II': 8.5,
        'Differential Calculus': 7.0, 'Probability and Statistics': 7.8,
        'Computer and Server Architecture': 6.2,
        'Socio-Emotional Skills and Conflict Management': 8.9
    },
    'mlopez': {
        'Discrete Mathematics': 9.5, 'Programming': 9.8, 'English II': 9.2,
        'Differential Calculus': 9.0, 'Probability and Statistics': 9.6,
        'Computer and Server Architecture': 9.4,
        'Socio-Emotional Skills and Conflict Management': 10.0
    },
    'euc': {
        'Discrete Mathematics': 8.2, 'Programming': 6.9, 'English II': 8.8,
        'Differential Calculus': 6.0, 'Probability and Statistics': 6.4,
        'Computer and Server Architecture': 8.1,
        'Socio-Emotional Skills and Conflict Management': 9.0
    },
    'cbalam': {
        'Discrete Mathematics': 8.8, 'Programming': 9.0, 'English II': 8.5,
        'Differential Calculus': 6.6, 'Probability and Statistics': 8.9,
        'Computer and Server Architecture': 8.7,
        'Socio-Emotional Skills and Conflict Management': 9.2
    },
}

#INPUT: Login loop with error handling
logged_in = False
while not logged_in:
    try:
        username = input("User: ").strip()
        password = input("Password: ").strip()

        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

        if username not in users:
            raise ValueError(f"User '{username}' not found.")

        if users[username]['password'] != password:
            raise ValueError("Incorrect password.")

        logged_in = True

    except ValueError as e:
        print(f"Login error: {e} Please try again.")

# PROCESS: Read role and user info
try:
    rol  = users[username]['rol']
    name = users[username]['name']
    print(f"Bienvenid@!, {name} ({rol})")
    print("=" * 30)

    #STUDENT
    if rol == 'student':
        print("  School Report")
        print("=" * 30)

        if username not in notes:
            raise KeyError(f"No grades found for user '{username}'.")

        aprobadas = set()
        for subject in subjects:
            grade = notes[username][subject]
            print(f"{subject[:24]:<24}: {grade}")
            if grade >= 8.0:
                aprobadas.add(subject)

        pendientes = set(subjects) - aprobadas
        print()
        print(f"Approved : {aprobadas}")
        print(f"Pending  : {pendientes}")

    #PROFESSOR 
    elif rol == 'professor':
        grading = True
        while grading:
            print("  Students")
            print("=" * 30)
            for user, info in users.items():
                if info['rol'] == 'student':
                    print(f"  User: {user:<10} | Student: {info['name']}")
            print()

            student_user = input("Student to grade (username, or ENTER to exit): ").strip()
            if student_user == "":
                grading = False
                continue

            if student_user not in users or users[student_user]['rol'] != 'student':
                print(f"Error: '{student_user}' is not a valid student username.")
                continue

            print()
            for subject in subjects:
                print(subject)
            print()

            subject_to_grade = input("Subject to grade: ").strip()
            if subject_to_grade not in subjects:
                print(f"Error: '{subject_to_grade}' is not a valid subject.")
                continue

            try:
                new_grade = float(input("New grade: ").strip())
                if not (0.0 <= new_grade <= 10.0):
                    raise ValueError("Grade must be between 0.0 and 10.0.")
            except ValueError as e:
                print(f"Grade error: {e}")
                continue

            print(f"\nDo you confirm (yes/no)?")
            print(f"{subject_to_grade}: {notes[student_user][subject_to_grade]} ==> {new_grade}")
            confirm = input().strip().lower()

            if confirm == "yes":
                notes[student_user][subject_to_grade] = new_grade
                print("Grade updated!")
            else:
                print("Change cancelled.")

    #COORDINATOR
    elif rol == 'coordinator':
        print("=" * 30)
        print("  Professors")
        print("=" * 30)
        for user, info in users.items():
            if info['rol'] == 'professor':
                print(f"  User: {user:<10} | Professor: {info['name']}")

        print()
        print("=" * 30)
        print("  Students")
        print("=" * 30)
        for user, info in users.items():
            if info['rol'] == 'student':
                print(f"  User: {user:<10} | Student: {info['name']}")

        print()
        print("=" * 30)
        print("  Records")
        print("=" * 30)
        header = f"{'SUBJECTS':<16}"
        for user in notes:
            header += f" | {user:<6}"
        print(header)
        print("-" * len(header))
        for subject in subjects:
            row = f"{subject[:14]:<16}"
            for user in notes:
                row += f" | {notes[user][subject]:<6}"
            print(row)

    else:
        raise ValueError(f"Unknown role: '{rol}'")

#OUTPUT: Error handling 
except KeyError as e:
    print(f"Data error: missing key {e}")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")