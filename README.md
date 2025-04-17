# Blockstak-news-api 
# FastAPI Backend

This project is a backend API built using [FastAPI](https://fastapi.tiangolo.com/), leveraging Pydantic for data validation and SQLAlchemy for ORM.

---

## Requirements

- Python 3.9 or higher

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-fastapi-project.git
cd your-fastapi-project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
- pip install --upgrade pip
- pip install -r requirements.txt

# Set environment variables
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mypassword

# Run the project
uvicorn app.main:app --reload
