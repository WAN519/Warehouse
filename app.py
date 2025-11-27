import json
from flask import Flask, jsonify
from PromotionAdvisor import PromotionAdvisor
from SalesAnalyzer import SalesAnalyzer

# Assuming Flask is installed: pip install flask

# 1. Initialize Flask application
app = Flask(__name__)

# 2. Initialize your advisor (it loads the API Key)
try:
    # Attempt to initialize the AI advisor
    advisor = PromotionAdvisor()
except EnvironmentError as e:
    print(f"Flask Server failed to initialize PromotionAdvisor: {e}")
    # Set to None if initialization fails
    advisor = None


@app.route('/api/report', methods=['GET'])
def get_promotion_report():
    """
    API endpoint: Generates the promotion report and returns it in JSON format.
    """
    if advisor is None:
        return jsonify({"error": "Advisor not initialized due to missing API Key."}), 500

    try:
        # Initialize the Sales Analyzer to fetch product data
        Analyzer = SalesAnalyzer()
        # In a real application: data should be fetched from your database (e.g., via SalesAnalyzer)
        data_from_db = Analyzer.test()

        # 1. Call the AI suggestion generator
        suggestions_markdown = advisor.get_suggestions(data_from_db)

        # 2. Construct the JSON response package
        response_data = {
            "products": data_from_db,  # Raw data (for frontend charts)
            "suggestions": suggestions_markdown  # AI generated Markdown suggestions
        }

        # 3. Return JSON response
        # jsonify automatically converts Python dicts to JSON strings
        return jsonify(response_data)

    except Exception as e:
        print(f"--- Fatal Backend Error ---: {e}")
        return jsonify({
            "error": "A critical server error occurred during data processing.",
            "details": str(e),
            "suggestions": "Backend Error: Check server console for SalesAnalyzer or PromotionAdvisor issues."
        }), 500


@app.route('/')
def serve_index():
    """
    Serve the frontend HTML file (for a real application).
    """
    # Assuming index.html is in the same directory as app.py
    return open('index.html', 'r', encoding='utf-8').read()


if __name__ == '__main__':
    # Run the Flask server
    print("--- Starting Flask Server on http://127.0.0.1:5000 ---")
    app.run(debug=True)