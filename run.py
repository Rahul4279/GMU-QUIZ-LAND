#!/usr/bin/env python3
"""
GMU Quiz Land - Run Script
Simple script to start the Flask application
"""

from app import app

if __name__ == '__main__':
    print("🌐 Starting GMU Quiz Land...")
    print("📚 Admin Login: admin@gmu.edu / admin123")
    print("🔗 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
