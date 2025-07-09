import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json

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
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        prompt = """
        Generate a unique profile for a "swamp fairy" (沼の妖精).
        The profile should include:
        - A creative Japanese name (e.g., 靄の精, 思ひ雫).
        - A corresponding English alias, written in Katakana (e.g., ヘイズ・スプライト, オモイシズク).
        - A unique physical feature.
        - A characteristic behavior.
        - A specific appearance location (not necessarily a physical swamp, but a "spiritual swamp" like a deep hobby, a forgotten place, etc.).
        - A symbolic meaning.

        Format the output strictly as follows, with each field on a new line:
        Name: [Japanese Name]
        Alias: [Katakana English Alias]
        Feature: [Feature description]
        Behavior: [Behavior description]
        Location: [Location description]
        Symbolism: [Symbolism description]

        Example:
        Name: 思ひ雫
        Alias: オモイシズク
        Feature: 深い藍色を帯びた、水滴のような形をした半透明の生命体。
        Behavior: 何かに深く没頭している人間（＝沼の主）の傍に、いつの間にか現れる。
        Location: 深夜の書斎、モニターの光だけが灯るPCデスク周り。
        Symbolism: 「創造的な没入」と「尽きることのない探求心」。
        """
        response = model.generate_content(prompt)
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
