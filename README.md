### PrathamNathani_News-Summary-API

# Features
- User registration & JWT authentication
- Fetch latest news headlines (summarized)
- Search news articles by keyword (summarized)
- Save and view favorite articles
- Uses free Hugging Face AI model (`sshleifer/distilbart-cnn-12-6`) to generate summaries
  

# Create and activate virtual environment:
python -m venv venv
venv\Scripts\activate   # Windows
         OR
source venv/bin/activate  # Mac/Linux

# Install dependencies:
  pip install -r requirements.txt

# Create .env file:
  NEWSAPI_KEY = your_real_api_key_here

# Apply Migrations
  python manage.py makemigrations
  python manage.py migrate

# Run Server
  python manage.py runserver


