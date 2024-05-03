import requests
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load JSON data from file
try:
    response = requests.get('https://backend-jobsman.up.railway.app/get')
    response.raise_for_status()  # Raise an exception for bad status codes
    json_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    json_data = None


# Route to render the search form
@app.route('/')
def search_form():
    return render_template('search_form.html')


@app.route('/search', methods=['POST'])
def search():
    query_string = request.form['query']
    queries = [q.strip() for q in query_string.replace(',', '+').split('+')]

    locations = []
    query_terms = []
    for query in queries:
        if ',' in query:
            locs = [loc.strip() for loc in query.split(',')]
            locations.extend(locs)
        else:
            query_terms.append(query)

    filtered_items = json_data[:]
    for query in query_terms:
        filtered_items = [item for item in filtered_items if any(query.lower() in value.lower() for value in item.values())]
    for loc in locations:
        filtered_items = [item for item in filtered_items if any(loc.lower() in value.lower() for value in item.values())]

    count = len(filtered_items)

    return render_template('search_results.html', query=query_string, results=filtered_items, count=count)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
