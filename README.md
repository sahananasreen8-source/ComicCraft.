# ComicCraft — AI Comic Story Creator

A Flask web app that creates original comic scripts using Google's Gemini API.

## Features
- Enter a story idea
- Choose a genre, audience, and 4/6/8 panels
- Generate a comic title, summary, panel descriptions, and dialogue
- Copy the generated story

## Run locally
1. Install Python 3.11 or newer.
2. Open a terminal in this folder and run `pip install -r requirements.txt`.
3. Create a Gemini API key from Google AI Studio.
4. Set the `GEMINI_API_KEY` environment variable (never commit the key).
   - Windows PowerShell: `$env:GEMINI_API_KEY="YOUR_KEY"`
   - macOS/Linux: `export GEMINI_API_KEY="YOUR_KEY"`
5. Run `python app.py` and open `http://127.0.0.1:5000`.

## Deploy to GitHub and Render
1. Create a GitHub repository named `ComicCraft`.
2. Upload/push the files in this folder to that repository.
3. In Render, choose **New + → Web Service**, connect the repository.
4. Render should detect `render.yaml`; use build command `pip install -r requirements.txt` and start command `gunicorn app:app` if asked.
5. In Render Environment, add `GEMINI_API_KEY` with your secret API key.
6. Deploy and open the service URL.

## Important
- Do not upload your API key to GitHub or place it in source code.
- Gemini API usage may have quotas or charges depending on your account and current terms.
