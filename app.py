# app.py
from flask import request, jsonify
import ctalapi
import snippetsapi
from shops import create_app

app = create_app()  # This creates the Flask app and registers the shop blueprint

# Register other blueprints
app.register_blueprint(ctalapi.cta_l_api)
app.register_blueprint(snippetsapi.snippets)


countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


def _find_next_id():
    return max(country["id"] for country in countries) + 1


@app.get("/countries")
def get_countries():
    return jsonify(countries)


@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415
