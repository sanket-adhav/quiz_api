# Quiz API

A simple backend API for creating and taking quizzes using FastAPI and SQLite.

---

## Features

### Quiz Management

- Create a quiz with a title.
- Add questions with multiple options (one correct answer).
- Delete a quiz or a question.

### Quiz Taking

- Get all questions for a quiz (without showing correct answers).
- Submit answers and get the score.

### Tech Stack

- Python 3.13.
- FastAPI
- SQLAlchemy
- SQLite (for database)
- Uvicorn (ASGI server)

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd quiz_api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the API

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see Swagger UI and test all endpoints.

---

## API Endpoints

### Health Check

```bash
GET /health
```

### Create Quiz

```json
POST /quizzes
Body: { "title": "General Knowledge Quiz" }
```

### Add Question to Quiz

```json
POST /quizzes/{quiz_id}/questions
Body: {
  "text": "Who is the Prime Minister of India?",
  "options": [
    {"text": "Narendra Modi", "is_correct": true},
    {"text": "Rahul Gandhi", "is_correct": false}
  ]
}
```

### Get Questions (without answers)

```bash
GET /quizzes/{quiz_id}/questions
```

### Submit Quiz

```json
POST /quizzes/{quiz_id}/submit
Body: [
  { "question_id": 1, "option_id": 1 },
  { "question_id": 2, "option_id": 3 }
]
```

### Delete Quiz

```bash
DELETE /quizzes/{quiz_id}
```

### Delete Question

```bash
DELETE /questions/{question_id}
```

---

## Notes

- Option IDs are internal and increment automatically.
- Correct answers are never returned in the "Get Questions" endpoint.
- Scores are returned as:

```json
{ "score": 1, "total": 1 }
```

---

## License

This project is open-source.
