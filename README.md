# Het of De

Het of De provides people learning Dutch a quick way to look up the article of a noun, along with some examples of basic grammar rules that result from the article type.

## Live Site
[hetofde.com](https://www.hetofde.com)

## Features
- Enables users to quickly look up the article of Dutch nouns
- Provides examples of grammar implications of articles:
  - Definite articles
  - Demonstrative pronouns
  - Indefinite articles + adjective endings
  - Relative pronouns
- Has a grammar guide to explain the rules of Dutch grammar related to definite articles along with examples

## Tech Stack
**Frontend**
- React with React Router
- Deployed on Render

**Backend**
- Flask REST API with Flask-CORS
- SQLite database with nouns and related data
- Gunicorn production server
- Deployed on Render

**Data Processing**
- Python script to parse Wiktextract JSONL data
- Rule-based article classification logic

## Data Source
Full credit to [kaikki.org](https://www.kaikki.org) and Tatu Ylonen for the Dutch dictionary dataset.

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/HetofDe.git
cd HetofDe
```

### 2. Backend Setup
```bash
# Create virtual environment to avoid conflicts
python -m venv venv

# Activate on Windows
venv\Scripts\activate

#Activate on Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. (Optional) Database Setup
This step is optional, as the database is included in the repo. If you need to regenerate the database for whatever reason, follow these steps.

Download the Dutch dictionary data from [kaikki.org](https://kaikki.org/dictionary/Dutch/):
```bash
# Download nl-extract.jsonl and place it in the root directory
python parse_json.py
```
This will create `dutch_nouns.db` with Dutch nouns and related data

### 4. Frontend Setup
```bash
cd frontend
npm install
```

### 5. Environment Variables
Create a `.env` file in the `frontend/` directory:
```
REACT_APP_API_URL=http://localhost:5000
```

## Running Locally

### Start the Backend
```bash
# From root directory, with venv activated
python flask_app.py
```
Backend runs on `http://localhost:5000`

### Start the Frontend
```bash
# From frontend/ directory
npm start
```
Frontend runs on `http://localhost:3000`

## Known Limitations
- Database contains 135k+ common Dutch nouns but may not include very recent slang, highly technical terms, or plural forms of nouns
- Article classification is rule-based and sourced from Wiktextract tags as well as diminutive rules; edge cases may exist
- Homonyms may only display the definition and article of the most common occurence of the homonym
- Single-word nouns only