import os
from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)

def create_comic_story(idea, genre, audience, panels):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it in your environment variables.")

    client = genai.Client(api_key=api_key)
    prompt = f"""
You are ComicCraft, a friendly AI comic-story creator.
Create an original comic outline from the user's idea.

Idea: {idea}
Genre: {genre}
Target audience: {audience}
Number of panels: {panels}

Return:
1. A catchy comic title.
2. A short one-sentence summary.
3. Exactly {panels} panels. For each panel include:
   - Panel number
   - Visual description (what the artist should draw)
   - Character dialogue or narration
Keep it suitable for the selected audience, original, clear, and fun.
Do not copy existing copyrighted characters or stories.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.8)
    )
    return response.text or "Sorry, I couldn't generate a story. Please try again."

@app.route("/", methods=["GET", "POST"])
def index():
    story = None
    error = None
    form = {"idea": "", "genre": "Fantasy", "audience": "All ages", "panels": "4"}
    if request.method == "POST":
        form["idea"] = request.form.get("idea", "").strip()
        form["genre"] = request.form.get("genre", "Fantasy")
        form["audience"] = request.form.get("audience", "All ages")
        form["panels"] = request.form.get("panels", "4")
        if len(form["idea"]) < 5:
            error = "Please enter a story idea with at least 5 characters."
        else:
            try:
                panel_count = int(form["panels"])
                if panel_count not in (4, 6, 8):
                    raise ValueError()
                story = create_comic_story(form["idea"], form["genre"], form["audience"], panel_count)
            except ValueError:
                error = "Please choose 4, 6, or 8 panels."
            except Exception as exc:
                app.logger.exception("Comic generation failed")
                error = str(exc) if "GEMINI_API_KEY" in str(exc) else "Story generation failed. Check your Gemini API key and try again."
    return render_template("index.html", story=story, error=error, form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
