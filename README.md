# Flashcards Web Application  

## Introduction  

This project is developed as part of my third-semester project submission. It is a web-based flashcard application designed to facilitate learning and self-assessment through interactive flashcards. Users can create and manage flashcard decks, take quizzes based on their flashcards, and track their progress. The platform also includes a feature to convert PDFs into flashcards for efficient study material management.  

## Features  

- **User Authentication**: Secure login and registration system.  
- **Flashcard Decks**: Create, edit, and manage categorized flashcard decks.  
- **Quiz Mode**: Take quizzes based on flashcards with automatic result evaluation.  
- **PDF Import**: Convert PDFs into flashcards using text extraction.  
- **Interactive UI**: Smooth animations and transitions for an engaging user experience.  
- **Progress Tracking**: Track learning performance and quiz results over time.  

## Technology Stack  

- **Backend**: Django, Python  
- **Frontend**: HTML, CSS, Bootstrap, JavaScript  
- **Database**: SQLite3
- **Libraries**: PyPDF2 (for PDF extraction), Matplotlib (for result visualization), OpenAI API (for text processing and formatting)  

## Installation and Setup  

### Prerequisites  
Ensure that Python is installed on your system.  

### Steps  

1. Clone the repository:  
   ```sh
   git clone https://github.com/Zayf24/DECKIT
   cd flashcards-project
   ```  
2. Create a virtual environment and activate it:  
   ```sh
   python -m venv env  
   source env/bin/activate  # macOS/Linux  
   env\Scripts\activate  # Windows  
   ```  
3. Install project dependencies:  
   ```sh
   pip install -r requirements.txt  
   ```  
4. Apply database migrations:  
   ```sh
   python manage.py migrate  
   ```  
5. **Configure OpenAI API Key**  
   The PDF-to-Deck feature requires an OpenAI API key. Open `pdftodeck.py` and replace `<your-api-key>` with your actual OpenAI API key:  
   ```python
   openai.api_key = "<your-api-key>"
   ```  

6. Start the development server:  
   ```sh
   python manage.py runserver  
   ```  

## Future Enhancements  

- AI-generated flashcards for automated content creation.  
- Advanced analytics for detailed performance tracking.  
- Mobile-friendly progressive web application (PWA) for improved accessibility.  

This project demonstrates the integration of interactive learning tools with a user-friendly interface, ensuring an effective study experience.
