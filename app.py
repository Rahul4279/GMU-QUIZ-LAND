from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from ai_question_generator import NVIDIAQuestionGenerator, SimpleQuestionGenerator
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///gmu_quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please log in to access this page.'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    num_questions = db.Column(db.Integer, nullable=False)
    duration_mode = db.Column(db.String(20), nullable=False)  # 'per_question' or 'overall'
    duration_seconds = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', backref='quiz', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    order = db.Column(db.Integer, nullable=False)

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    current_question = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    answers = db.relationship('Answer', backref='attempt', lazy=True, cascade='all, delete-orphan')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, is_admin=True).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    return render_template('admin/dashboard.html', quizzes=quizzes)

@app.route('/admin/create-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        num_questions = int(request.form['num_questions'])
        duration_mode = request.form['duration_mode']
        duration_value = int(request.form['duration_value'])
        
        # Convert duration to seconds
        duration_seconds = duration_value * 60
        
        quiz = Quiz(
            title=title,
            num_questions=num_questions,
            duration_mode=duration_mode,
            duration_seconds=duration_seconds
        )
        db.session.add(quiz)
        db.session.commit()
        
        return redirect(url_for('add_questions', quiz_id=quiz.id))
    
    return render_template('admin/create_quiz.html')

@app.route('/admin/add-questions/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def add_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        # Clear existing questions
        Question.query.filter_by(quiz_id=quiz_id).delete()
        
        for i in range(quiz.num_questions):
            question_text = request.form[f'question_{i+1}']
            option_a = request.form[f'option_a_{i+1}']
            option_b = request.form[f'option_b_{i+1}']
            option_c = request.form[f'option_c_{i+1}']
            option_d = request.form[f'option_d_{i+1}']
            correct_answer = request.form[f'correct_{i+1}']
            
            question = Question(
                quiz_id=quiz_id,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer,
                order=i+1
            )
            db.session.add(question)
        
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_questions.html', quiz=quiz)

@app.route('/admin/delete-quiz/<int:quiz_id>')
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/quiz-results/<int:quiz_id>')
@login_required
def quiz_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    attempts = Attempt.query.filter_by(quiz_id=quiz_id, is_completed=True).order_by(Attempt.end_time.desc()).all()
    return render_template('admin/quiz_results.html', quiz=quiz, attempts=attempts)

# Student Routes
@app.route('/')
def index():
    return render_template('student/index.html')

@app.route('/student/quizzes')
def student_quizzes():
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    return render_template('student/quizzes.html', quizzes=quizzes)

@app.route('/student/start-quiz/<int:quiz_id>', methods=['GET', 'POST'])
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if request.method == 'POST':
        student_name = request.form['student_name']
        
        # Create new attempt
        attempt = Attempt(
            quiz_id=quiz_id,
            student_name=student_name,
            start_time=datetime.utcnow()
        )
        db.session.add(attempt)
        db.session.commit()
        
        session['attempt_id'] = attempt.id
        return redirect(url_for('take_quiz', quiz_id=quiz_id))
    
    return render_template('student/start_quiz.html', quiz=quiz)

@app.route('/student/take-quiz/<int:quiz_id>')
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    attempt_id = session.get('attempt_id')
    
    if not attempt_id:
        return redirect(url_for('student_quizzes'))
    
    attempt = Attempt.query.get(attempt_id)
    if not attempt or attempt.is_completed:
        return redirect(url_for('student_quizzes'))
    
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.order).all()
    
    if attempt.current_question >= len(questions):
        # Quiz completed
        return redirect(url_for('student_quiz_results', quiz_id=quiz_id))
    
    current_q = questions[attempt.current_question]
    
    return render_template('student/take_quiz.html', 
                         quiz=quiz, 
                         question=current_q, 
                         question_num=attempt.current_question + 1,
                         total_questions=len(questions),
                         attempt=attempt)

@app.route('/student/submit-answer', methods=['POST'])
def submit_answer():
    attempt_id = session.get('attempt_id')
    if not attempt_id:
        return jsonify({'error': 'No active attempt'}), 400
    
    attempt = Attempt.query.get(attempt_id)
    if not attempt or attempt.is_completed:
        return jsonify({'error': 'Attempt not found or completed'}), 400
    
    data = request.get_json()
    question_id = data.get('question_id')
    selected_answer = data.get('selected_answer')
    
    if not question_id or not selected_answer:
        return jsonify({'error': 'Missing data'}), 400
    
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 400
    
    # Check if answer is correct
    is_correct = selected_answer == question.correct_answer
    
    # Save answer
    answer = Answer(
        attempt_id=attempt_id,
        question_id=question_id,
        selected_answer=selected_answer,
        is_correct=is_correct
    )
    db.session.add(answer)
    
    # Update attempt
    attempt.current_question += 1
    if is_correct:
        attempt.score += 1
    
    # Check if quiz is completed
    quiz = Quiz.query.get(attempt.quiz_id)
    if attempt.current_question >= quiz.num_questions:
        attempt.is_completed = True
        attempt.end_time = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'success': True, 'is_correct': is_correct})

@app.route('/student/quiz-results/<int:quiz_id>')
def student_quiz_results(quiz_id):
    attempt_id = session.get('attempt_id')
    if not attempt_id:
        return redirect(url_for('student_quizzes'))
    
    attempt = Attempt.query.get(attempt_id)
    if not attempt:
        return redirect(url_for('student_quizzes'))
    
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.order).all()
    answers = Answer.query.filter_by(attempt_id=attempt_id).all()
    
    # Clear session
    session.pop('attempt_id', None)
    
    return render_template('student/quiz_results.html', 
                         quiz=quiz, 
                         attempt=attempt, 
                         questions=questions, 
                         answers=answers)

# AI Question Generation Routes
@app.route('/admin/ai-create-quiz', methods=['GET', 'POST'])
@login_required
def ai_create_quiz():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        topic = request.form.get('topic')
        num_questions = int(request.form.get('num_questions', 10))
        difficulty = request.form.get('difficulty', 'medium')
        quiz_title = request.form.get('quiz_title', f'AI Quiz: {topic}')
        duration_mode = request.form.get('duration_mode', 'per_question')
        duration_value = int(request.form.get('duration_value', 30))
        
        if not topic:
            flash('Please enter a topic for the quiz.', 'error')
            return render_template('admin/ai_create_quiz.html')
        
        try:
            # Generate questions using AI
            generator = NVIDIAQuestionGenerator()
            questions_data = generator.generate_questions(topic, num_questions, difficulty)
            
            # If AI generation fails, use simple generator for testing
            if not questions_data:
                flash('AI generation failed. Using sample questions for testing.', 'warning')
                simple_generator = SimpleQuestionGenerator()
                questions_data = simple_generator.generate_questions(topic, num_questions, difficulty)
            
            if not questions_data:
                flash('Failed to generate questions. Please try again.', 'error')
                return render_template('admin/ai_create_quiz.html')
            
            # Create the quiz
            quiz = Quiz(
                title=quiz_title,
                num_questions=len(questions_data),
                duration_mode=duration_mode,
                duration_seconds=duration_value
            )
            db.session.add(quiz)
            db.session.flush()  # Get the quiz ID
            
            # Add questions to the quiz
            for i, q_data in enumerate(questions_data):
                question = Question(
                    quiz_id=quiz.id,
                    question_text=q_data['question'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_answer=q_data['correct_answer'],
                    order=i + 1
                )
                db.session.add(question)
            
            db.session.commit()
            flash(f'AI Quiz "{quiz_title}" created successfully with {len(questions_data)} questions!', 'success')
            return redirect(url_for('admin_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating AI quiz: {str(e)}', 'error')
            return render_template('admin/ai_create_quiz.html')
    
    return render_template('admin/ai_create_quiz.html')

@app.route('/admin/generate-questions', methods=['POST'])
@login_required
def generate_questions():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    topic = data.get('topic')
    num_questions = data.get('num_questions', 10)
    difficulty = data.get('difficulty', 'medium')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        generator = NVIDIAQuestionGenerator()
        questions = generator.generate_questions(topic, num_questions, difficulty)
        
        # If AI generation fails, use simple generator for testing
        if not questions:
            simple_generator = SimpleQuestionGenerator()
            questions = simple_generator.generate_questions(topic, num_questions, difficulty)
        
        return jsonify({'questions': questions})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize database and create admin user
def create_tables():
    db.create_all()
    
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(email='admin@gmu.edu').first()
    if not admin:
        admin = User(email='admin@gmu.edu', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@gmu.edu / admin123")

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    
    app.run(debug=True)
