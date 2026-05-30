# GitHub Repository Analyzer

A full-stack web application to analyze GitHub repositories, providing insights into health, popularity, and activity.

## Features
- **Repo Analysis:** Enter any GitHub URL to get detailed stats.
- **Health Score:** Custom algorithm to calculate repository health based on stars, forks, issues, contributors, and recent activity.
- **Language Distribution:** Visual breakdown of programming languages used.
- **History Tracking:** Analysis history stored in SQLite.
- **Clean Architecture:** Modular code structure for scalability.
- **Responsive UI:** Modern dashboard built with vanilla CSS and Chart.js.

## Tech Stack
- **Backend:** Python FastAPI
- **Database:** SQLite (SQLAlchemy ORM)
- **Data Analysis:** Pandas
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Chart.js
- **API:** GitHub REST API

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd github-repo-analyzer
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token (Optional but recommended)
   DATABASE_URL=sqlite:///./github_analyzer.db
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Deployment on Render

1. **Create a Web Service:**
   - Connect your GitHub repository to Render.
2. **Environment:**
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Environment Variables:**
   - Add `GITHUB_TOKEN` (optional) and `DATABASE_URL` (use a persistent disk or external DB for production history).
   - Note: Render's free tier has ephemeral storage. For persistent SQLite, use [Render Blueprints](https://render.com/docs/blueprints) with a Disk.

## License
MIT
