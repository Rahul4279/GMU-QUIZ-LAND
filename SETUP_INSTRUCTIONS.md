# GMU Quiz Land - Setup Instructions

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```
OR
```bash
python run.py
```

### 3. Access the Application
- **URL:** http://localhost:5000
- **Admin Login:** admin@gmu.edu / admin123

### 4. Add Demo Data (Optional)
```bash
python demo_data.py
```

## 📁 Project Structure

```
GMU LIB QUIZ/
├── app.py                 # Main Flask application
├── run.py                 # Simple run script
├── demo_data.py           # Demo data generator
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── SETUP_INSTRUCTIONS.md  # This file
└── templates/             # HTML templates
    ├── base/
    │   └── base.html      # Base template with Bootstrap
    ├── admin/             # Admin interface templates
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── create_quiz.html
    │   ├── add_questions.html
    │   └── quiz_results.html
    └── student/           # Student interface templates
        ├── index.html
        ├── quizzes.html
        ├── start_quiz.html
        ├── take_quiz.html
        └── quiz_results.html
```

## 🎯 Features Implemented

### ✅ Admin Features
- [x] Secure login system
- [x] Dashboard with quiz management
- [x] Create quizzes with custom settings
- [x] Two timer modes (per-question / overall)
- [x] Add multiple choice questions
- [x] View detailed results and analytics
- [x] Delete quizzes

### ✅ Student Features
- [x] Browse available quizzes
- [x] Real-time timer functionality
- [x] Responsive design
- [x] Instant results with feedback
- [x] Score tracking

### ✅ Technical Features
- [x] Flask web framework
- [x] SQLite database
- [x] Bootstrap 5 styling
- [x] JavaScript timers
- [x] Server-side validation
- [x] Session management

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional):
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///gmu_quiz.db
```

### Database
- Default: SQLite (gmu_quiz.db)
- Automatically created on first run
- Admin user created automatically

## 🎮 How to Use

### For Admins:
1. Login with admin@gmu.edu / admin123
2. Click "Create New Quiz"
3. Set quiz parameters
4. Add questions and answers
5. View results from dashboard

### For Students:
1. Go to http://localhost:5000
2. Browse available quizzes
3. Enter name and start quiz
4. Answer questions within time limit
5. View results and performance

## 🐛 Troubleshooting

### Common Issues:

1. **Port already in use:**
   - Change port in app.py: `app.run(port=5001)`

2. **Database errors:**
   - Delete gmu_quiz.db and restart

3. **Import errors:**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

4. **Admin login not working:**
   - Check if admin user was created (should happen automatically)
   - Try running demo_data.py to reset database

## 📱 Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🔒 Security Notes
- Change default admin password in production
- Use environment variables for secret keys
- Consider using PostgreSQL for production
- Enable HTTPS in production

## 📞 Support
This is a demo application for GMU. For issues, check the code comments and Flask documentation.
