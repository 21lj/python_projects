# from flask import Flask, jsonify

# app = Flask(__name__)

# @app.route('/')
# def health_check():
#     return jsonify({
#         "status": "healthy",
#         "service": "URL Shortener API"
#     })

# @app.route('/api/health')
# def api_health():
#     return jsonify({
#         "status": "ok",
#         "message": "URL Shortener API is running"
#     })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify, redirect, abort
from storage import url_store
from utils import generate_code, is_valid_url
from datetime import datetime

app = Flask(__name__)

BASE_URL = "http://localhost:5000"

@app.route("/")
def health_check():
    return jsonify({"message": "URL Shortener running"}), 200

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url or not is_valid_url(original_url):
        return jsonify({"error": "Invalid or missing URL"}), 400

    code = generate_code()
    while code in url_store:
        code = generate_code()

    url_store[code] = {
        "original_url": original_url,
        "created_at": datetime.utcnow(),
        "clicks": 0
    }

    return jsonify({"short_url": f"{BASE_URL}/{code}"}), 201

@app.route("/<code>", methods=["GET"])
def redirect_url(code):
    if code not in url_store:
        abort(404)

    url_store[code]["clicks"] += 1
    return redirect(url_store[code]["original_url"], code=302)

@app.route("/api/stats/<code>", methods=["GET"])
def stats(code):
    entry = url_store.get(code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "original_url": entry["original_url"],
        "created_at": entry["created_at"].isoformat(),
        "clicks": entry["clicks"]
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
