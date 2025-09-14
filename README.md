# GMU Quiz Land

A comprehensive quiz platform for George Mason University with admin and student interfaces.

## Features

### Admin Features
- 🔐 Secure admin authentication
- 📊 Dashboard with quiz statistics
- ➕ Create quizzes with customizable settings
- ⏱️ Two timer modes: per-question or overall time
- 📝 Add multiple choice questions
- 📈 View detailed quiz results and analytics
- 🗑️ Delete quizzes

### Student Features
- 🎓 Browse available quizzes
- ⏰ Real-time timer functionality
- 📱 Responsive design for all devices
- 📊 Instant results with detailed feedback
- 🎯 Score tracking and performance analysis

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - Admin login: `admin@gmu.edu` / `admin123`

## Usage

### For Admins
1. Login with admin credentials
2. Create a new quiz from the dashboard
3. Set quiz parameters (title, number of questions, timer mode)
4. Add questions with multiple choice options
5. View results and analytics

### For Students
1. Browse available quizzes on the home page
2. Enter your name to start a quiz
3. Answer questions within the time limit
4. View your results and performance

## Technical Details

- **Framework:** Flask
- **Database:** SQLite (easily configurable for PostgreSQL/MySQL)
- **Frontend:** Bootstrap 5 with custom CSS
- **Authentication:** Flask-Login
- **Timer:** JavaScript with server-side validation

## Database Schema

- **Users:** Admin authentication
- **Quizzes:** Quiz metadata and settings
- **Questions:** Individual quiz questions
- **Attempts:** Student quiz attempts
- **Answers:** Individual question responses

## Configuration

The application uses environment variables for configuration:
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string

## Security Features

- Admin-only access to quiz creation
- Server-side timer validation
- Secure password hashing
- Session management

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

This project is created for educational purposes at G M University.
