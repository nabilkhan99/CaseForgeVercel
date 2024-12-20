# GP Portfolio Review Generator

A tool for generating and managing GP portfolio reviews.

## Project Structure
- `/Frontend` - Next.js frontend application
- `/Backend` - FastAPI backend application

## Getting Started

### Frontend
bash
cd Frontend/gp-portfolio-frontend
npm install
npm run dev
```

### Backend
bash
cd Backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Running the Application

To run the application, start both the frontend and backend servers. The frontend will be available at `http://localhost:3000`, and the backend will be available at `http://localhost:8000`.




