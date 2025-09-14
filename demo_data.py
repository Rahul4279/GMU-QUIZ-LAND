#!/usr/bin/env python3
"""
GMU Quiz Land - Demo Data Script
Adds sample quizzes and questions to the database
"""

from app import app, db, Quiz, Question, User

def create_demo_data():
    with app.app_context():
        # Create sample quizzes
        quiz1 = Quiz(
            title="General Knowledge Quiz",
            num_questions=5,
            duration_mode="per_question",
            duration_seconds=60  # 1 minute per question
        )
        db.session.add(quiz1)
        db.session.flush()  # Get the ID
        
        # Add questions for quiz 1
        questions1 = [
            {
                "question_text": "What is the capital of France?",
                "option_a": "London",
                "option_b": "Paris",
                "option_c": "Berlin",
                "option_d": "Madrid",
                "correct_answer": "B"
            },
            {
                "question_text": "Which planet is known as the Red Planet?",
                "option_a": "Venus",
                "option_b": "Mars",
                "option_c": "Jupiter",
                "option_d": "Saturn",
                "correct_answer": "B"
            },
            {
                "question_text": "What does HTML stand for?",
                "option_a": "HyperText Markup Language",
                "option_b": "High Tech Modern Language",
                "option_c": "Home Tool Markup Language",
                "option_d": "Hyperlink and Text Markup Language",
                "correct_answer": "A"
            },
            {
                "question_text": "Who painted the Mona Lisa?",
                "option_a": "Vincent van Gogh",
                "option_b": "Pablo Picasso",
                "option_c": "Leonardo da Vinci",
                "option_d": "Michelangelo",
                "correct_answer": "C"
            },
            {
                "question_text": "What is the largest ocean on Earth?",
                "option_a": "Atlantic Ocean",
                "option_b": "Indian Ocean",
                "option_c": "Pacific Ocean",
                "option_d": "Arctic Ocean",
                "correct_answer": "C"
            }
        ]
        
        for i, q_data in enumerate(questions1, 1):
            question = Question(
                quiz_id=quiz1.id,
                question_text=q_data["question_text"],
                option_a=q_data["option_a"],
                option_b=q_data["option_b"],
                option_c=q_data["option_c"],
                option_d=q_data["option_d"],
                correct_answer=q_data["correct_answer"],
                order=i
            )
            db.session.add(question)
        
        # Create second quiz
        quiz2 = Quiz(
            title="Programming Fundamentals",
            num_questions=4,
            duration_mode="overall",
            duration_seconds=300  # 5 minutes total
        )
        db.session.add(quiz2)
        db.session.flush()
        
        # Add questions for quiz 2
        questions2 = [
            {
                "question_text": "Which programming language is known for its use in web development?",
                "option_a": "Python",
                "option_b": "JavaScript",
                "option_c": "C++",
                "option_d": "Java",
                "correct_answer": "B"
            },
            {
                "question_text": "What is the result of 2 + 2 * 3 in most programming languages?",
                "option_a": "8",
                "option_b": "12",
                "option_c": "6",
                "option_d": "10",
                "correct_answer": "A"
            },
            {
                "question_text": "Which of the following is NOT a programming paradigm?",
                "option_a": "Object-Oriented",
                "option_b": "Functional",
                "option_c": "Procedural",
                "option_d": "Linear",
                "correct_answer": "D"
            },
            {
                "question_text": "What does API stand for?",
                "option_a": "Application Programming Interface",
                "option_b": "Advanced Programming Interface",
                "option_c": "Automated Programming Interface",
                "option_d": "Application Process Interface",
                "correct_answer": "A"
            }
        ]
        
        for i, q_data in enumerate(questions2, 1):
            question = Question(
                quiz_id=quiz2.id,
                question_text=q_data["question_text"],
                option_a=q_data["option_a"],
                option_b=q_data["option_b"],
                option_c=q_data["option_c"],
                option_d=q_data["option_d"],
                correct_answer=q_data["correct_answer"],
                order=i
            )
            db.session.add(question)
        
        # Commit all changes
        db.session.commit()
        print("✅ Demo data created successfully!")
        print("📚 Created 2 sample quizzes:")
        print("   - General Knowledge Quiz (5 questions, 1 min per question)")
        print("   - Programming Fundamentals (4 questions, 5 min total)")

if __name__ == '__main__':
    create_demo_data()
