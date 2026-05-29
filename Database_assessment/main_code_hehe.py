# ============================================================
# Study Guide Application
# Author: [Your Name]
# Date: [Date]
# Description: A quiz program that helps students study.
#              Questions are stored in a SQLite database.
#              Users can add, delete, and quiz themselves.
# ============================================================

import sqlite3  # Built-in Python library for SQLite databases
import random   # Used to shuffle questions during a quiz

# ── Constants ────────────────────────────────────────────────
# Using constants instead of "magic numbers" so values are
# easy to find and change in one place.

DATABASE_FILE   = "study_guide.db"   # Name of the database file
MIN_ANSWER_LEN  = 1                   # Minimum characters for a valid answer
MAX_QUESTION_LEN = 200                # Maximum characters allowed in a question
MIN_QUIZ_QUESTIONS = 1                # Smallest number of questions for a quiz


# ── Database Setup ───────────────────────────────────────────

def connect_to_database():
    """
    Opens a connection to the SQLite database file.
    Returns the connection object so other functions can use it.
    """
    connection = sqlite3.connect(DATABASE_FILE)
    return connection


def create_tables(connection):
    """
    Creates the database tables if they don't already exist.

    Tables:
      categories  – stores topic categories (e.g. 'Maths', 'Science')
      questions   – stores each question, its answer, and which category it belongs to
    """
    cursor = connection.cursor()

    # Create the categories table first because questions refer to it
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT    NOT NULL UNIQUE
        )
    """)

    # Create the questions table with a foreign key to categories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            question_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT    NOT NULL,
            answer_text   TEXT    NOT NULL,
            category_id   INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    connection.commit()  # Save the changes to the database


def add_sample_data(connection):
    """
    Adds a small set of starter questions so the app works straight away.
    Only runs when the database is brand new (no categories yet).
    """
    cursor = connection.cursor()

    # Check if any categories already exist — don't add duplicates
    cursor.execute("SELECT COUNT(*) FROM categories")
    count = cursor.fetchone()[0]

    if count > 0:
        return  # Data already exists, nothing to do

    # Insert the sample category
    cursor.execute("INSERT INTO categories (category_name) VALUES (?)", ("General Knowledge",))
    sample_category_id = cursor.lastrowid  # Get the ID that was just created

    # Sample questions to get the user started
    sample_questions = [
        ("What is the capital of New Zealand?",   "Wellington"),
        ("What is 7 multiplied by 8?",             "56"),
        ("What gas do plants absorb from the air?", "Carbon dioxide"),
        ("Who wrote Romeo and Juliet?",             "Shakespeare"),
    ]

    # Insert all sample questions using executemany (more efficient than a loop)
    cursor.executemany(
        "INSERT INTO questions (question_text, answer_text, category_id) VALUES (?, ?, ?)",
        [(q, a, sample_category_id) for q, a in sample_questions]
    )

    connection.commit()
    print("✔  Sample questions have been loaded into the database.\n")


# ── Category Functions ───────────────────────────────────────

def get_all_categories(connection):
    """
    Returns a list of all categories from the database.
    Each item is a tuple: (category_id, category_name)
    """
    cursor = connection.cursor()
    cursor.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
    return cursor.fetchall()


def display_categories(connection):
    """
    Prints all available categories to the screen with a number next to each.
    Returns the list so the caller can use it (e.g. let the user pick one).
    """
    categories = get_all_categories(connection)

    if not categories:
        print("  No categories found. Please add a category first.")
        return []

    print("\n  Available categories:")
    for index, (cat_id, cat_name) in enumerate(categories, start=1):
        print(f"    {index}. {cat_name}")
    return categories


def add_category(connection):
    """
    Asks the user to type a new category name and saves it to the database.
    Rejects blank names and names that already exist.
    """
    print("\n── Add Category ──────────────────────────────")

    while True:
        new_name = input("  Enter category name (or 'cancel' to go back): ").strip()

        if new_name.lower() == "cancel":
            print("  Cancelled.")
            return

        # Validation: name must not be empty
        if len(new_name) == 0:
            print("  Category name cannot be blank. Please try again.")
            continue

        # Try to insert; catch the error if the name already exists (UNIQUE constraint)
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (new_name,))
            connection.commit()
            print(f"  ✔  Category '{new_name}' added successfully.")
            break

        except sqlite3.IntegrityError:
            # This happens when the UNIQUE constraint is violated
            print(f"  The category '{new_name}' already exists. Try a different name.")


def pick_category(connection, prompt="  Choose a category number: "):
    """
    Displays the list of categories and asks the user to choose one.
    Returns the chosen category_id, or None if the user cancels.
    """
    categories = display_categories(connection)

    if not categories:
        return None

    while True:
        user_input = input(prompt + "(or 'cancel'): ").strip()

        if user_input.lower() == "cancel":
            return None

        # Check the input is a valid integer
        if not user_input.isdigit():
            print("  Please enter a number from the list.")
            continue

        choice_index = int(user_input) - 1  # Convert to 0-based index

        if 0 <= choice_index < len(categories):
            chosen_category_id = categories[choice_index][0]
            return chosen_category_id
        else:
            print(f"  Please enter a number between 1 and {len(categories)}.")


# ── Question Functions ───────────────────────────────────────

def get_questions_by_category(connection, category_id):
    """
    Returns all questions that belong to a specific category.
    Each item is a tuple: (question_id, question_text, answer_text)
    """
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT question_id, question_text, answer_text
        FROM   questions
        WHERE  category_id = ?
        ORDER BY question_id
        """,
        (category_id,)
    )
    return cursor.fetchall()


def get_all_questions(connection):
    """
    Returns every question from the database, joined with its category name.
    Each item is: (question_id, question_text, answer_text, category_name)
    """
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT q.question_id,
               q.question_text,
               q.answer_text,
               c.category_name
        FROM   questions  q
        JOIN   categories c ON q.category_id = c.category_id
        ORDER BY c.category_name, q.question_id
        """
    )
    return cursor.fetchall()


def view_all_questions(connection):
    """
    Displays every question and answer in the database, grouped by category.
    Useful for reviewing or checking what's stored.
    """
    print("\n── All Questions in Database ─────────────────")
    all_questions = get_all_questions(connection)

    if not all_questions:
        print("  No questions found. Add some questions first!")
        return

    current_category = None  # Track which category we're printing under

    for q_id, q_text, a_text, cat_name in all_questions:
        # Print a heading whenever the category changes
        if cat_name != current_category:
            print(f"\n  [{cat_name}]")
            current_category = cat_name

        print(f"    ID {q_id}: {q_text}")
        print(f"           Answer: {a_text}")


def add_question(connection):
    """
    Guides the user through adding a new question to the database.
    Asks for: the category, the question text, and the answer.
    Validates all inputs before saving.
    """
    print("\n── Add Question ──────────────────────────────")

    # Step 1: Choose a category (or add one first)
    print("  First, choose a category for this question.")
    category_id = pick_category(connection)
    if category_id is None:
        print("  Cancelled.")
        return

    # Step 2: Enter the question text
    while True:
        question_text = input("  Enter the question: ").strip()

        if len(question_text) == 0:
            print("  Question cannot be blank.")
            continue
        if len(question_text) > MAX_QUESTION_LEN:
            print(f"  Question is too long (max {MAX_QUESTION_LEN} characters).")
            continue
        break  # Valid input — move on

    # Step 3: Enter the answer
    while True:
        answer_text = input("  Enter the answer: ").strip()

        if len(answer_text) < MIN_ANSWER_LEN:
            print("  Answer cannot be blank.")
            continue
        break  # Valid input

    # Step 4: Save to database
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO questions (question_text, answer_text, category_id) VALUES (?, ?, ?)",
        (question_text, answer_text, category_id)
    )
    connection.commit()
    print("  ✔  Question added successfully!")


def delete_question(connection):
    """
    Lets the user remove a question by entering its ID.
    Shows all questions first so the user can find the right ID.
    Asks for confirmation before deleting.
    """
    print("\n── Delete Question ───────────────────────────")
    view_all_questions(connection)

    # Check there's actually something to delete
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]

    if total_questions == 0:
        return  # Nothing to delete

    while True:
        user_input = input("\n  Enter the ID of the question to delete (or 'cancel'): ").strip()

        if user_input.lower() == "cancel":
            print("  Cancelled.")
            return

        # Validate that the input is a number
        if not user_input.isdigit():
            print("  Please enter a valid number.")
            continue

        question_id = int(user_input)

        # Check that this ID actually exists in the database
        cursor.execute("SELECT question_text FROM questions WHERE question_id = ?", (question_id,))
        result = cursor.fetchone()

        if result is None:
            print(f"  No question found with ID {question_id}. Please try again.")
            continue

        # Confirm before deleting so the user doesn't accidentally remove things
        print(f"\n  You are about to delete: \"{result[0]}\"")
        confirm = input("  Are you sure? Type 'yes' to confirm: ").strip().lower()

        if confirm == "yes":
            cursor.execute("DELETE FROM questions WHERE question_id = ?", (question_id,))
            connection.commit()
            print("  ✔  Question deleted.")
        else:
            print("  Deletion cancelled.")
        return


# ── Quiz Functions ───────────────────────────────────────────

def run_quiz(connection):
    """
    Runs a quiz session.
    The user can choose to quiz on all categories or just one.
    Questions are shown in random order. The score is shown at the end.
    Answers are checked case-insensitively.
    """
    print("\n── Start Quiz ────────────────────────────────")
    print("  Quiz all categories or just one?")
    print("    1. All categories")
    print("    2. Choose a specific category")

    # Ask the user which mode they want
    while True:
        mode_input = input("  Enter 1 or 2: ").strip()
        if mode_input in ("1", "2"):
            break
        print("  Please enter 1 or 2.")

    # Fetch the right set of questions based on the user's choice
    if mode_input == "1":
        # All categories — get every question
        raw_questions = get_all_questions(connection)
        # Each item: (question_id, question_text, answer_text, category_name)
        questions = [(q_text, a_text) for _, q_text, a_text, _ in raw_questions]

    else:
        # Specific category — ask the user to pick one
        category_id = pick_category(connection)
        if category_id is None:
            print("  Quiz cancelled.")
            return
        raw_questions = get_questions_by_category(connection, category_id)
        # Each item: (question_id, question_text, answer_text)
        questions = [(q_text, a_text) for _, q_text, a_text in raw_questions]

    # Make sure there are enough questions to run a quiz
    if len(questions) < MIN_QUIZ_QUESTIONS:
        print("  Not enough questions in this category. Please add some first!")
        return

    # Shuffle so questions appear in a different order every time
    random.shuffle(questions)

    # ── Run the quiz ─────────────────────────────
    score         = 0
    total         = len(questions)
    question_number = 1

    print(f"\n  Starting quiz — {total} question(s). Type your answer and press Enter.\n")

    for question_text, correct_answer in questions:
        print(f"  Q{question_number}/{total}: {question_text}")
        user_answer = input("  Your answer: ").strip()

        # Compare answers, ignoring upper/lower case differences
        if user_answer.lower() == correct_answer.lower():
            print("  ✔  Correct!\n")
            score += 1
        else:
            print(f"  ✘  Wrong. The correct answer was: {correct_answer}\n")

        question_number += 1

    # ── Show final score ─────────────────────────
    percentage = (score / total) * 100
    print("─" * 48)
    print(f"  Quiz complete!  Score: {score}/{total}  ({percentage:.0f}%)")

    # Give encouraging feedback based on score
    if percentage == 100:
        print("  🎉 Perfect score! Outstanding!")
    elif percentage >= 80:
        print("  😊 Great work! Keep it up!")
    elif percentage >= 50:
        print("  👍 Good effort — review the ones you missed.")
    else:
        print("  📖 Keep studying — you'll get there!")
    print("─" * 48)


# ── Main Menu ────────────────────────────────────────────────

def display_menu():
    """
    Prints the main menu options to the screen.
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║           STUDY GUIDE APPLICATION       ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Start a Quiz                        ║")
    print("║  2. Add a Question                      ║")
    print("║  3. Delete a Question                   ║")
    print("║  4. Add a Category                      ║")
    print("║  5. View All Questions                  ║")
    print("║  6. Quit                                ║")
    print("╚══════════════════════════════════════════╝")


def get_menu_choice():
    """
    Asks the user to pick a menu option.
    Returns a valid integer between 1 and 6.
    Keeps asking until valid input is given.
    """
    MENU_MIN = 1
    MENU_MAX = 6

    while True:
        user_input = input("  Enter your choice: ").strip()

        # Make sure the input is a whole number
        if not user_input.isdigit():
            print(f"  Please enter a number between {MENU_MIN} and {MENU_MAX}.")
            continue

        choice = int(user_input)

        if MENU_MIN <= choice <= MENU_MAX:
            return choice
        else:
            print(f"  Please enter a number between {MENU_MIN} and {MENU_MAX}.")


def main():
    """
    Entry point for the application.
    Sets up the database and runs the main menu loop
    until the user chooses to quit.
    """
    print("\nWelcome to the Study Guide!")

    # Set up the database connection and create tables if needed
    connection = connect_to_database()
    create_tables(connection)
    add_sample_data(connection)   # Only adds data if the database is empty

    # ── Main loop ────────────────────────────────
    running = True

    while running:
        display_menu()
        choice = get_menu_choice()

        if choice == 1:
            run_quiz(connection)

        elif choice == 2:
            add_question(connection)

        elif choice == 3:
            delete_question(connection)

        elif choice == 4:
            add_category(connection)

        elif choice == 5:
            view_all_questions(connection)

        elif choice == 6:
            print("\n  Goodbye! Good luck with your studies! 👋\n")
            running = False

    # Always close the database connection cleanly when the program ends
    connection.close()


# ── Run the program ──────────────────────────────────────────
# This block only runs when the file is executed directly,
# not when it is imported as a module by another file.
if __name__ == "__main__":
    main()