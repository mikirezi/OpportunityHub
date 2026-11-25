from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="")
API_KEY = os.getenv("HIMALAYS_API_KEY")

@app.route("/")
def home():
    return app.send_static_file("index.html")
@app.route("/api/jobs")
def get_jobs():
    keyword = request.args.get("q", "")
    country = request.args.get("country", "")
    employment_type = request.args.get("employment_type", "")
    seniority = request.args.get("seniority", "")
    sort = request.args.get("sort", "relevant")                            
    url = "https://himalayas.app/jobs/api/search"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "q": keyword,
        "sort": sort
    }
    if country:
       params["country"] = country
    if employment_type:
       params["employment_type"] = employment_type
    if seniority:
       params["seniority"] = seniority
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
            )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException:
        return jsonify({
            "error": "unable to fetch jobs right now."
            }), 500
if __name__ == "__main__":
    app.run(debug=True)