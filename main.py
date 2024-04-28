import requests
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load JSON data from file
try:
    response = requests.get('https://backend-oj59.onrender.com/get')
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
    query = request.form['query'].lower()  # Convert query to lowercase for case-insensitive search
    filtered_items = [item for item in json_data if any(query in value.lower() for value in item.values())]
    count = len(filtered_items)

    return render_template('search_results.html', query=query, results=filtered_items, count=count)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
