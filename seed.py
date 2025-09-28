from database import SessionLocal, Base, engine
from models import Quiz, Question, Option

# Create tables if not exists
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def add_quiz(title, questions):
    # Check if quiz exists
    quiz = db.query(Quiz).filter_by(title=title).first()
    if quiz:
        print(f"Quiz '{title}' already exists, skipping...")
        return
    quiz = Quiz(title=title)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    for q_text, options in questions:
        question = Question(text=q_text, quiz_id=quiz.id)
        db.add(question)
        db.commit()
        db.refresh(question)
        for opt_text, is_correct in options:
            option = Option(text=opt_text, is_correct=is_correct, question_id=question.id)
            db.add(option)
        db.commit()
    print(f"Quiz '{title}' added successfully!")

# --- Seed quizzes ---
add_quiz("General Knowledge Quiz", [
    ("What is the capital of France?", [("Paris", True), ("London", False), ("Berlin", False)]),
    ("Which planet is known as the Red Planet?", [("Mars", True), ("Venus", False), ("Jupiter", False)])
])

add_quiz("Math Quiz", [
    ("What is 2 + 2?", [("3", False), ("4", True), ("5", False)]),
    ("What is 5 x 3?", [("15", True), ("10", False), ("20", False)])
])

db.close()
print("Seeding complete!")
