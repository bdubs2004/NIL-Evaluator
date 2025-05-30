import os
from flask import Flask, request, render_template
import vertexai
from vertexai.preview.generative_models import GenerativeModel

# Initialize Vertex AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
vertexai.init(project="finalproject-458201", location="us-central1")  # Replace with your actual project ID
model = GenerativeModel(model_name="gemini-1.5-flash")

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Get form input
    name = request.form.get("name")
    school = request.form.get("school")
    sport = request.form.get("sport")

    # Build the prompt
    prompt = (
        f"Estimate the NIL value for an athlete named {name}, who plays {sport} at {school}.\n"
        f"Consider the school's athletic profile, the popularity of the sport, media exposure, "
        f"and general NIL market trends. Provide:\n"
        f"- A dollar value estimate\n"
        f"- A brief rationale\n"
        f"- A breakdown of the valuation by exposure potential, performance expectations, and brand appeal."
    )

    # Get response from Gemini
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.75,
            "max_output_tokens": 2048,
        },
    )

    return render_template("response.html", name=name, response=response.text.strip())

if __name__ == "__main__":
    app.run(debug=True)
