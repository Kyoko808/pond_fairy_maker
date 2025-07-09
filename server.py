import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random

app = Flask(__name__, static_folder='.')
CORS(app) # Enable CORS for all routes

# Configure your API key here
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=API_KEY)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        # Placeholder for actual image generation logic if a suitable Gemini model becomes available
        # For now, returning a placeholder and a message about the current limitation
        print(f"Attempting to generate image with prompt: {prompt}")
        placeholder_image_url = "https://via.placeholder.com/300x400?text=Fairy+Image+Placeholder"
        
        return jsonify({
            'image_url': placeholder_image_url,
            'message': 'Image generation with Gemini API for direct text-to-image is not yet fully supported in this manner. A placeholder image is shown.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_gemini_models')
def list_gemini_models():
    try:
        models = genai.list_models()
        available_models = []
        for m in models:
            available_models.append({
                'name': m.name,
                'display_name': m.display_name,
                'description': m.description,
                'input_token_limit': m.input_token_limit,
                'output_token_limit': m.output_token_limit,
                'supported_generation_methods': m.supported_generation_methods
            })
        return jsonify(available_models)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_fairy_text', methods=['POST'])
def generate_fairy_text():
    try:
        # Define a list of diverse themes to ensure variety
        themes = [
            "忘れられた書斎の埃", "古い機械の心臓部", "真夜中のキッチンの静寂", 
            "複雑な数式の中に宿る論理", "夏の終わりの夕暮れ", "捨てられたおもちゃの記憶",
            "海底に沈んだ都市の響き", "プログラムのバグから生まれた歪み", "雨上がりのアスファルトの匂い",
            "誰かの夢の残り香", "古い地図のインク"
        ]
        # Pick a random theme for this request
        selected_theme = random.choice(themes)

        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        
        # The prompt now dynamically includes the random theme
        prompt = f"""
        **Theme: "{selected_theme}"**

        Based on the theme above, generate a unique profile for a fairy.
        The fairy's name and characteristics should be directly inspired by the provided theme.
        **Do not use common, generic words like "葦 (reed)" or "沼 (swamp)" unless the theme directly implies it.**

        The profile must include:
        - A creative Japanese name.
        - Its Katakana reading.
        - A corresponding English alias, written in Katakana.
        - A unique physical feature.
        - A characteristic behavior.
        - A specific appearance location.
        - A symbolic meaning.

        Format the output strictly as follows, with each field on a new line:
        Name: [Japanese Name]
        Reading: [Katakana Reading]
        Alias: [Katakana English Alias]
        Feature: [Feature description]
        Behavior: [Behavior description]
        Location: [Location description]
        Symbolism: [Symbolism description]
        """

        # Set temperature to 1.0 for more creative and less repetitive responses
        generation_config = genai.types.GenerationConfig(temperature=1.0)
        
        response = model.generate_content(prompt, generation_config=generation_config)
        generated_text = response.text

        # Parse the generated text
        lines = generated_text.strip().split('\n')
        fairy_data = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                fairy_data[key.strip().lower()] = value.strip()

        return jsonify(fairy_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)