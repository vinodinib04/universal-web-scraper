# Universal Web Scraper

A production-ready web scraper system.

## 🚀 Features
- Takes any website/blog URL as input.
- Automatically finds related URLs.
- Extracts title, content (in Markdown), and classifies content type.
- Outputs standardized JSON.
- Simple frontend UI.

## ⚡ Usage
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the backend:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

3. Open frontend:
    Open `http://localhost:8000/static/index.html` in browser.

## ⚡ Deploy
1. Serve the app with Gunicorn in production:
    ```bash
    gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    ```

2. Configure NGINX as reverse proxy (optional).
