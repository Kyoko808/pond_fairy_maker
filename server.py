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
            "自然界の神秘", "都市の片隅", "人間の感情", "時間の流れ", "日常の魔法",
            "夢と幻想", "科学と技術", "物語の断片", "宇宙の広がり", "生命の循環"
        ]
        # Pick a random theme for this request
        selected_theme = random.choice(themes)

        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        
        # Prompt is now entirely in Japanese with strict instructions.
        prompt = f"""
        **お題：「{selected_theme}」**

        上記のお題に完全に基づいて、ユニークな妖精のプロフィールを生成してください。
        妖精の名前と特徴は、必ず指定されたお題から着想を得てください。

        【生成ルール】
        - **回答はすべて日本語で記述してください。**
        - **名前の後に括弧書きでローマ字表記を追加しないでください。**
        - 「葦」や「沼」のような、お題と直接関係のない一般的な単語は避けてください。
        - 創造的で多様な表現を心がけてください。

        以下のフォーマットに厳密に従って、各項目を改行して出力してください。

        名前： [創造的な日本語名]
        読み： [カタカナでの読み]
        別名： [英語の別名をカタカナで]
        特徴： [ユニークな物理的特徴]
        習性： [特徴的な習性]
        出現場所： [具体的な出現場所]
        象徴： [象徴的な意味]
        """

        generation_config = genai.types.GenerationConfig(temperature=1.2, top_p=0.95)
        
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
