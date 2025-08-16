BudgetBuddy - Personal Finance Tracker
A modern desktop application built with Python to help you manage your personal finances with an AI-powered chatbot assistant.

Features
Income & Expense Tracking: Easily add and monitor your financial transactions
Goal Setting: Set financial goals and track your progress
Visual Progress Bars: See how close you are to achieving your goals
AI Chatbot: Get personalized financial advice using Groq AI
Expense History: Keep track of all your spending
Modern UI: Clean, dark-themed interface using CustomTkinter

Prerequisites
Before running this application, make sure you have:

Python 3.8 or higher installed
A Groq API key (free at https://groq.com)
Installation
Clone the repository:
bash
git clone https://github.com/yourusername/budgetbuddy.git
cd budgetbuddy
Install required packages:
bash
pip install -r requirements.txt
Set up environment variables:
Copy .env.example to .env
Get your free API key from Groq
Replace your_groq_api_key_here with your actual API key
Optional - Add a logo:
Place a logo.png file in the same directory as Budgetbuddy.py
The app will work without it (uses an emoji instead)
Usage
Run the application:

bash
python Budgetbuddy.py
How to Use:
Set Your Income: Click "Edit Income" to enter your monthly/weekly income
Add Expenses: Click "Add Expenses" to log your spending
Create Goals: Click "🎯 Goals" to set savings targets
Track Progress: Watch your goal progress bars fill up as you save
Get AI Advice: Click "🤖 Chatbot" for personalized financial tips
File Structure
budgetbuddy/
│
├── Budgetbuddy.py      # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (you create this)
├── .env.example       # Example environment file
├── logo.png          # Optional app logo
└── README.md         # This file
Dependencies
CustomTkinter: Modern UI framework
Pillow: Image processing
Groq: AI chatbot functionality
python-dotenv: Environment variable management
Getting Your Groq API Key
Go to groq.com
Sign up for a free account
Navigate to the API section
Generate a new API key
Copy it to your .env file
Contributing
Feel free to fork this project and submit pull requests for any improvements!

License
This project is open source and available under the MIT License.

Troubleshooting
App won't start?

Make sure all dependencies are installed: pip install -r requirements.txt
Check that your .env file exists and has the correct API key
Chatbot not working?

Verify your Groq API key is correct
Check your internet connection
Visual issues?

The app is designed for 1920x1280 resolution
Try adjusting the window size in the code if needed
