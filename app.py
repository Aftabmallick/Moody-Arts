# app.py
from flask import Flask, request, jsonify
import openai
import random
import dotenv
from flask_cors import CORS
# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Set your OpenAI API key
dotenv.load_dotenv()

def generate_image_prompt(mood):
    """Generate an art prompt based on the detected mood, with a diverse set of ideas for each mood."""
    prompt_dict = {
        "calm": [
            "A tranquil library with soft, golden lighting and cozy armchairs, perfect for reading.",
            "A gentle rain falling on a quiet city street, illuminated by warm street lights.",
            "A Zen garden with smooth stones, flowing water, and bamboo plants, emanating serenity.",
            "A person meditating by a quiet river, surrounded by soothing, soft colors."
        ],
        "melancholic": [
            "An empty theater with velvet curtains, dim lighting, and a single spotlight casting shadows.",
            "A lone figure walking through a misty forest at dusk, with dark, moody colors.",
            "A rainy window with water droplets streaming down, evoking a sense of reflection.",
            "An old, dusty attic filled with forgotten memories and vintage objects, in muted tones."
        ],
        "energized": [
            "A bustling city street with neon signs, fast-paced pedestrians, and vibrant graffiti.",
            "A mountain climber at sunrise, surrounded by breathtaking views and bright colors.",
            "A colorful abstract painting with bold strokes and high-energy patterns.",
            "A lively dance floor with people moving, colorful lights, and an electric atmosphere."
        ],
        "reflective": [
            "A dimly lit study with a vintage desk, open notebook, and a single candle burning.",
            "An art gallery with minimalist paintings, where a person is deeply contemplating.",
            "A starry night sky over a quiet desert, with someone gazing thoughtfully at the stars.",
            "An old bookstore with cozy corners, filled with books and an atmosphere of nostalgia."
        ]
    }

    # Select a random prompt from the list corresponding to the detected mood
    return random.choice(prompt_dict.get(mood, ["Very High Quality Image"]))

@app.route('/generate_moodscape', methods=['POST'])
def generate_moodscape():
    data = request.json
    user_text = data.get("text", "")
    mood = f"Generate a beautiful image based on my feelings: {user_text}"
    
    # Step 2: Generate the art prompt based on the detected mood
    art_prompt = generate_image_prompt(mood)
    print(user_text,mood,art_prompt)
    # Step 3: Generate the image with DALL-E using the art prompt
    try:
        response = openai.images.generate(
        model="dall-e-3",
        prompt=art_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
        )
        image_url = response.data[0].url
    except Exception as e:
        return jsonify({"error": f"Error generating image: {e}"}), 500

    # Return the mood, prompt, and image URL
    return jsonify({
        "mood": mood,
        "prompt": art_prompt,
        "image_url": image_url
    })

if __name__ == "__main__":
    app.run()
