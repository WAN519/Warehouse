import json
from flask import Flask, jsonify
from flask_cors import CORS  # 导入 CORS，确保前端能访问
import os
import sys

from SalesAnalyzer import SalesAnalyzer
from PromotionAdvisor import PromotionAdvisor

# --- Flask  init ---
app = Flask(__name__)
# start CORS make front can access
CORS(app)

try:
    # init AI
    advisor = PromotionAdvisor()
    print("PromotionAdvisor 初始化成功 (连接 Gemini API)。")
except EnvironmentError as e:
    print(f"Flask Server failed to initialize PromotionAdvisor: {e}", file=sys.stderr)
    advisor = None
except Exception as e:
    print(f"Flask Server failed to initialize PromotionAdvisor: {e}", file=sys.stderr)
    advisor = None


@app.route('/api/report', methods=['GET'])
def get_promotion_report():
    """
    API endpoint: Generates the promotion report and returns it in JSON format.
    """
    # Check AI start status
    if advisor is None:
        return jsonify({"error": "Advisor not initialized due to missing API Key or other startup error."}), 500

    try:

        # get data
        Analyzer = SalesAnalyzer()

        data_from_db = Analyzer.format_data_for_ai()

        if data_from_db is None:
            # if connect database error
            return jsonify({
                "error": "Database retrieval failed.",
                "details": "SalesAnalyzer could not fetch valid product data."
            }), 503  # Service Unavailable


        # get suggestions from AI
        suggestions_markdown = advisor.get_suggestions(data_from_db)

        # 3. create JSON respones
        response_data = {
            "products": data_from_db,  # orignal data (for chart)
            "suggestions": suggestions_markdown  # AI report
        }

        # return response_data
        return jsonify(response_data)

    except Exception as e:
        print(f"--- Fatal Backend Error ---: {e}", file=sys.stderr)
        return jsonify({
            "error": "A critical server error occurred during data processing.",
            "details": str(e),
            "suggestions": "Backend Error: Check server console for SalesAnalyzer or PromotionAdvisor issues."
        }), 500


@app.route('/')
def serve_index():
    """
    Serve the frontend HTML file
    """
    try:
        return open('index.html', 'r', encoding='utf-8').read()
    except FileNotFoundError:
        return "Error: index.html not found.", 404


if __name__ == '__main__':
    print("--- Starting Flask Server on http://127.0.0.1:5000 ---")
    # start api
    app.run(debug=True)