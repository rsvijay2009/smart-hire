# HR Candidate Filter

A Flask-based web application to assist HR teams in filtering and shortlisting job candidates based on job requirements and resumes.

## Features
- Upload job descriptions and candidate resumes (PDF/text).
- Extract skills, experience, and qualifications using NLP (spaCy).
- Match candidates to job requirements with a weighted scoring system.
- Display ranked candidates with match scores and details.
- Store candidate data in SQLite for historical access.

## Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hr_candidate_filter
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_md
   ```

4. **Set environment variables**:
   Create a `.env` file with:
   ```plaintext
   SECRET_KEY=your-secure-secret-key
   ```

5. **Run the application**:
   ```bash
   python run.py
   ```
   Access at `http://127.0.0.1:5000`.

## Testing
Run unit tests with:
```bash
pytest
```

## Deployment
For production, use Gunicorn:
```bash
gunicorn -w 4 "app:create_app()"
```
Deploy on Heroku, AWS, or Render.

## Project Structure
```
hr_candidate_filter/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── data/
├── tests/
├── .env
├── requirements.txt
├── run.py
├── README.md
```

## Customization
- Update `app/data/skills.json` to add job-specific skills.
- Adjust scoring weights in `app/services/nlp_service.py`.
- Extend `extract_qualifications` for additional criteria.

## Limitations
- Supports text-based PDFs only (add OCR for scanned PDFs).
- NLP accuracy depends on spaCy model and skills list.
- Experience extraction is heuristic-based.

For support, contact the xAI community: https://community.x.ai/