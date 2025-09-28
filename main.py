from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas

app = FastAPI(title="Quiz API", version="0.1")

# Create tables
Base.metadata.create_all(bind=engine)

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check
@app.get("/health")
def health():
    return {"message": "API is running"}

# Create quiz
@app.post("/quizzes")
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(get_db)):
    db_quiz = models.Quiz(title=quiz.title)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return {"id": db_quiz.id, "title": db_quiz.title}

# Add question to quiz
@app.post("/quizzes/{quiz_id}/questions")
def add_question(quiz_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db_question = models.Question(text=question.text, quiz_id=quiz_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for opt in question.options:
        db_option = models.Option(text=opt.text, is_correct=opt.is_correct, question_id=db_question.id)
        db.add(db_option)
    db.commit()
    return {"question_id": db_question.id, "text": db_question.text}

# Get questions (without answers)
@app.get("/quizzes/{quiz_id}/questions")
def get_questions(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    result = []
    for q in db_quiz.questions:
        result.append({
            "question_id": q.id,
            "text": q.text,
            "options": [{"id": o.id, "text": o.text} for o in q.options]
        })
    return result

# Submit answers
@app.post("/quizzes/{quiz_id}/submit")
def submit_quiz(quiz_id: int, answers: list[schemas.Answer], db: Session = Depends(get_db)):
    score = 0
    for ans in answers:
        option = db.query(models.Option).filter(models.Option.id == ans.option_id,
                                               models.Option.question_id == ans.question_id).first()
        if option and option.is_correct:
            score += 1
    total = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).count()
    return {"score": score, "total": total}

@app.delete("/quizzes/{quiz_id}")
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    db.delete(quiz)
    db.commit()
    return {"message": f"Quiz {quiz_id} deleted successfully"}

@app.delete("/questions/{question_id}")
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"message": f"Question {question_id} deleted successfully"}
